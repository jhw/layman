### short [run-build]

- artifacts name is wrong
  - think u need name override

### medium

- avoid specifying runtime as "3.8" ?
- should runtime really be specified in config ?

### lambada

- bucket, codebuild project in stack.yaml need -lambada suffixes
  - see layman stack.yaml
- update bucket ref in scripts/delete_stack.py, list_artifacts.py

### medium

### done

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
