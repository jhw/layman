#!/usr/bin/env python

import boto3, json, os, sys, yaml

from botocore.exceptions import ClientError

DefaultDeps=yaml.safe_load("""
- name: pip
- name: awscli
""")

CodeBuildVersion= "0.2"

BuildSpec={"version": CodeBuildVersion,
           "phases": {},
           "env": {"variables": {}}}

StackNamePattern="%s-layman-ci"

"""
https://stackoverflow.com/questions/247770/how-to-retrieve-a-modules-path
"""

def load_path(path):
    import layman
    return "%s/%s" % (layman.__path__.__dict__["_path"][0], path)

StackTemplate=open(load_path("assets/stack.yaml")).read()

WebhookLambda=open(load_path("assets/webhook.py")).read()

def deploy_stack(cf, config,
                 stacknamepat=StackNamePattern,
                 stackbody=StackTemplate,
                 buildspec=BuildSpec,
                 webhook=WebhookLambda):
    def stack_exists(cf, stackname):
        stacknames=[stack["StackName"]
                    for stack in cf.describe_stacks()["Stacks"]]
        return stackname in stacknames
    def init_params(params, webhook):
        return {"AppName": params["globals"]["app"],
                "CodeBuildBuildSpec": yaml.safe_dump(buildspec),
                "WebhookUrl": params["slack"]["webhook"],
                "WebhookLambda": webhook}
        return fn(aws_format(modkwargs))
    def format_params(params):
        return [{"ParameterKey": k,
                 "ParameterValue": v}
                for k, v in params.items()]
    stackname=stacknamepat % config["globals"]["app"]
    action="update" if stack_exists(cf, stackname) else "create"
    fn=getattr(cf, "%s_stack" % action)
    params=init_params(config, webhook)
    fn(StackName=stackname,
       Parameters=format_params(params),
       TemplateBody=stackbody,
       Capabilities=["CAPABILITY_IAM"])
    waiter=cf.get_waiter("stack_%s_complete" % action)
    waiter.wait(StackName=stackname)

if __name__=="__main__":
    try:
        if len(sys.argv) < 2:
            raise RuntimeError("Please enter config")
        configfile=sys.argv[1]
        if not configfile.endswith("yaml"):
            raise RuntimeError("config must be a yaml file")
        if not os.path.exists(configfile):
            raise RuntimeError("config does not exist")
        config=yaml.safe_load(open(configfile).read())    
        deploy_stack(boto3.client("cloudformation"), config)
    except ClientError as error:
        print (error)
    except RuntimeError as error:
        print ("Error: %s" % str(error))
