#!/bin/bash
# used for installing dependency of the aws lambda

dependency_list="AWSIoTPythonSDK jsonschema"
#------------------------------------------------------

for dependency in ${dependency_list}; do
# install dependency to local dir so that it can be packaged together with user code
# to be uploaded to aws lambda console
pip install ${dependency} --system -t .
done