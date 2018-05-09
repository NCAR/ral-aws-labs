def handler(event, context):
    """
    Lambda event handler to create an image from a netcdf file
    :param event: Contains details of the S3 put object (our netcdf file)
    :param context: Contains details of the lambda context (region, time limit, etc.)
    :return: None
    """
    import subprocess
    import os
    import boto3

    # Extract relevant values from the S3 event
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    # Download the object from S3
    print('downloading object s3://' + bucket + '/' + key)
    s3 = boto3.client('s3')
    s3.download_file(Bucket=bucket, Key=key, Filename='/tmp/data.nc')

    # Run the C++ application to create an image:
    #   Usage: nc2img <data_file> <field_name>
    #     Application will write /tmp/image.jpg
    #   Set LD_LIBRARY_PATH to find libraries in our zip file
    env = dict(os.environ)
    env['LD_LIBRARY_PATH'] = './home/ec2-user/netcdf/lib:./home/ec2-user/hdf5/lib:./home/ec2-user/zlib/lib'
    subprocess.run('./nc2img /tmp/data.nc T2', shell=True, env=env)

    # Upload the image to an S3 bucket
    s3.upload_file('/tmp/image.jpg', bucket, 'images/' + key + '-T2.jpg')
