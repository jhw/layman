#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter app name"
    exit
fi

aws s3 rm s3://$1-artifacts --recursive
aws cloudformation delete-stack --stack-name $1-layman-ci

