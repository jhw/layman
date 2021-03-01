#!/usr/bin/env bash

if [ $# -eq 0 ]
then
    echo "Please enter pipeline name"
    exit
fi

aws codepipeline start-pipeline-execution --name $1 --output table

