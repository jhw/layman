#!/usr/bin/env python

import boto3, datetime, json, os, sys, time, yaml

from botocore.exceptions import ClientError

def init_buildspec(config,
                   version="0.2"):    
    def init_install_phase(config):
        rtversions={"python": config["globals"]["runtime"]}
        commands=["mkdir -p build/python",
                  "pip install --upgrade pip"]
        for package in config["deps"]:
            if "repo" in package:
                host=package["repo"]["host"]
                if not host.endswith(".com"):
                    host+=".com"
                source="git+https://%s/%s/%s" % (host,
                                                 package["repo"]["owner"],
                                                 package["name"])
                if "version" in package:
                    source+="@%s" % package["version"]
            else:
                source=package["name"]
                if "version" in package:
                    source+="==%s" % package["version"]
            commands.append("pip install --upgrade --target build/python %s" % source)
        return {"runtime-versions": rtversions,
                "commands": commands}
    def init_postbuild_phase(config):
        commands=["echo \"%s\" > build/manifest.json" % json.dumps(config["deps"]).replace("\"", "\\\""),
                  'bash -c "if [ /"$CODEBUILD_BUILD_SUCCEEDING/" == /"0/" ]; then exit 1; fi"']
        return {"commands": commands}
    def init_phases(config):
        return {"install": init_install_phase(config),
                "post_build": init_postbuild_phase(config)}
    def init_artifacts(config):
        def timestamp():
            return datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
        return {"files": ["**/*"],
                "base-directory": "build",
                "name": "%s.zip" % timestamp()}
    return {"version": version,
            "phases": init_phases(config),
            "artifacts": init_artifacts(config)}

def update_project(cb, config, buildspec):

    source={"type": "NO_SOURCE",
            "buildspec": yaml.safe_dump(buildspec,
                                        default_flow_style=False)}
    print (cb.update_project(name=projectname,
                             source=source))

def run_build(cb, config):
    buildspec=init_buildspec(config)
    projectname="%s-layman-ci" % config["globals"]["app"]
    source={"type": "NO_SOURCE",
            "buildspec": yaml.safe_dump(buildspec,
                                        default_flow_style=False)}
    print (cb.update_project(name=projectname,
                             source=source))
    print (cb.start_build(projectName=projectname))

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
        run_build(boto3.client("codebuild"), config)
    except ClientError as error:
        print (error)
    except RuntimeError as error:
        print ("Error: %s" % str(error))
