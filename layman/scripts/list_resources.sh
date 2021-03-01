#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter app name"
    exit
fi

aws cloudformation describe-stack-resources --stack-name $1-layman-ci --query "StackResources[].{\"1.Timestamp\":Timestamp,\"2.LogicalId\":LogicalResourceId,\"3.PhysicalId\":PhysicalResourceId,\"4.Type\":ResourceType,\"5.Status\":ResourceStatus}"
