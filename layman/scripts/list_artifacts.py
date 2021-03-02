#!/usr/bin/env python

import boto3, sys

from botocore.exceptions import ClientError

def list_s3(s3, bucket):
    paginator=s3.get_paginator("list_objects_v2")
    kwargs={"Bucket": bucket}
    pages=paginator.paginate(**kwargs)
    for struct in pages:
        if "Contents" in struct:
            for obj in struct["Contents"]:
                print (obj["Key"])

if __name__=="__main__":
    try:
        if len(sys.argv) < 2:
            raise RuntimeError("Please enter app name")
        appname=sys.argv[1].split(".")[0] # just in case config file specified
        bucket="%s-layman-artifacts" % appname
        list_s3(boto3.client("s3"), bucket)
    except ClientError as error:
        print (error)
    except RuntimeError as error:
        print ("Error: %s" % (str(error)))
