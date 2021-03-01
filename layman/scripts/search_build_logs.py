#!/usr/bin/env python

import boto3, re, sys, time

from botocore.exceptions import ClientError

if __name__=="__main__":
    try:
        if len(sys.argv) < 4:
            raise RuntimeError("Please enter project, window, query")
        project, window, query = sys.argv[1:4]
        project=project.split(".")[0] # just in case config specified
        if not re.search("^\\d+$", window):
            raise RuntimeError("window is invalid")
        window=int(window)
        loggroupname="/aws/codebuild/%s" % project
        starttime=int(1000*(time.time()-window))                
        kwargs={"logGroupName": loggroupname,
                "startTime": starttime,
                "interleaved": True}
        if query not in ["*", ""]:
            kwargs["filterPattern"]=query
        logs=boto3.client("logs")
        events=logs.filter_log_events(**kwargs)["events"]        
        for event in sorted(events,
                            key=lambda x: x["timestamp"]):
            print (re.sub("\\r|\\n", "", event["message"]))
    except ClientError as error:
        print (error)
    except RuntimeError as error:
        print ("Error: %s" % str(error))
