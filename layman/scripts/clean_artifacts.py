#!/usr/bin/env python

import boto3, sys

from botocore.exceptions import ClientError

def list_s3(s3, bucket, prefix):
    paginator=s3.get_paginator("list_objects_v2")
    kwargs={"Bucket": bucket}
    if prefix!="*":
        kwargs["Prefix"]=prefix
    pages=paginator.paginate(**kwargs)
    for struct in pages:
        if "Contents" in struct:
            for obj in struct["Contents"]:
                print (obj["Key"])
                 s3.delete_object(Bucket=bucket,
                                  Key=obj["Key"])

if __name__=="__main__":
    try:
        if len(sys.argv) < 3:
            raise RuntimeError("Please enter bucket, prefix")
        bucket, prefix = sys.argv[1:3]
        list_s3(boto3.client("s3"), bucket, prefix)
    except ClientError as error:
        print (error)
    except RuntimeError as error:
        print ("Error: %s" % (str(error)))
