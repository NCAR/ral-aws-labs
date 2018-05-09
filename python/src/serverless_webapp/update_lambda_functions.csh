#! /bin/tcsh

zip forecasts.zip add_forecast.py get_forecasts.py
aws lambda update-function-code --function-name ${user}_add_forecast --zip-file fileb://forecasts.zip
aws lambda update-function-code --function-name ${user}_get_forecasts --zip-file fileb://forecasts.zip
rm forecasts.zip
