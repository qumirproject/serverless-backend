#!/bin/bash
fn_name="dummy"
rm $fn_name.zip
cd src
rm -r __pycache__
zip ../$fn_name.zip *
cd ..
aws lambda update-function-code --function-name $fn_name --zip-file fileb://$fn_name.zip