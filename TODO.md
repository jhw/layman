### short

### medium

### thoughts 

- more granularity in artifacts filename ?
- do you need webhooks for every single build event ?
- runtime declaration
  - should it really be in config ?
  - should it be listed as "3.8" ?

### done

- bucket, codebuild project in stack.yaml need -lambada suffixes
  - see layman stack.yaml
- update bucket ref in scripts/delete_stack.py, list_artifacts.py
- tagging
- print buildspec on creation
- artifacts name is wrong
  - think u need name override
- check artifacts
- bad python type
- start project
- update codebuild project
- generate buildspec
- replace `requirements.txt` with `manifest.json`
- add artifacts to stack
- source with blank buildspec
- test deploy/delete_stack.py
- github project
- deploy stack
- deploy_stack.py from pareto
