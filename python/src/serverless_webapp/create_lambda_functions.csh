#! /bin/tcsh

zip forecasts.zip add_forecast.py get_forecasts.py
aws lambda create-function --function-name ${user}_add_forecast --runtime python3.6 --role arn:aws:iam::388228333291:role/serverless_role --handler add_forecast.handler --zip-file fileb://forecasts.zip
aws lambda create-function --function-name ${user}_get_forecasts --runtime python3.6 --role arn:aws:iam::388228333291:role/serverless_role --handler get_forecasts.handler --zip-file fileb://forecasts.zip
rm forecasts.zip
