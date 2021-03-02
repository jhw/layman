### short [run-build]

- generate buildspec and artifacts path
- replace `requirements.txt` with `manifest.json`
- update codebuild project
- run project
  - remove waiter code

### lambada

- bucket, codebuild project in stack.yaml need -lambada suffixes
  - see layman stack.yaml
- update bucket ref in scripts/delete_stack.py

### medium

### done

- add artifacts to stack
- source with blank buildspec
- test deploy/delete_stack.py
- github project
- deploy stack
- deploy_stack.py from pareto
