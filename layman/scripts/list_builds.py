#!/usr/bin/env python

import boto3, os, sys, time

from botocore.exceptions import ClientError

def list_builds(cb, appname):
    def get_builds(cb, appname):
        resp=cb.list_builds_for_project(projectName=appname)
        if ("ids" not in resp or
            resp["ids"]==[]):
            raise RuntimeError("no build ids found")
        return cb.batch_get_builds(ids=resp["ids"])["builds"]
    builds=get_builds(cb, appname)
    for build in builds:
        print ("%s\t%s\t%s\t%s\t%s" % (build["id"],
                                       build["startTime"].strftime("%H:%M:%S"),
                                       build["endTime"].strftime("%H:%M:%S") if "endTime" in build else "N/A",
                                       build["currentPhase"],
                                       build["buildStatus"]))
    
if __name__=="__main__":
    try:
        if len(sys.argv) < 2:
            raise RuntimeError("Please enter app name")
        appname=sys.argv[1].split(".")[0] # just in case config file specified
        list_builds(boto3.client("codebuild"), appname)
    except ClientError as error:
        print (error)
    except RuntimeError as error:
        print ("Error: %s" % (str(error)))

