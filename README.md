# devops-schedule

You have a directed acyclic graph of processes that you can execute as a child process and you want to process the work with maximum parallelism. This repository orders the work that can be carried out simultaneously and in parallel. See my parallel-workers repository for an example of how to process the output of this schedule with parallelism.

## scheduler.js

This script uses csp.js to order a tree work graph into a paralellisable runnable schedule.

## scheduler.py

This script uses ortools to order a tree work graph into a parallelisable runnable schedule.

# how to use

Call `parallelise_components` on a list of dicts that look like this; each has a `name`, `ancestors` and `successors`. Note that ancestors are immediate ancestors, not all.

```
    {
        "name": "@ansible/worker-provision/package",
        "successors": [
            "@ansible/worker-provision/validate"
        ],
        "ancestors": []
    },
    {
        "name": "@ansible/worker-provision/validate",
        "successors": [
            "@ansible/worker-provision/plan"
        ],
        "ancestors": [
            "@ansible/worker-provision/package"
        ]
    },
    {
        "name": "@ansible/worker-provision/plan",
        "successors": [
            "@ansible/worker-provision/run"
        ],
        "ancestors": [
            "@ansible/worker-provision/validate"
        ]
    },
    {
        "name": "@ansible/worker-provision/run",
        "successors": [
            "@ansible/worker-provision/test"
        ],
        "ancestors": [
            "@ansible/worker-provision/plan"
        ]
    }
```

# returns

```
    {
        "position": 0,
        "name": "@ansible/worker-provision/package",
        "successors": [
            "@ansible/worker-provision/validate"
        ],
        "ancestors": []
    },
    {
        "position": 1,
        "name": "@ansible/worker-provision/validate",
        "successors": [
            "@ansible/worker-provision/plan"
        ],
        "ancestors": [
            "@ansible/worker-provision/package"
        ]
    },
    {
        "position": 2,
        "name": "@ansible/worker-provision/plan",
        "successors": [
            "@ansible/worker-provision/run"
        ],
        "ancestors": [
            "@ansible/worker-provision/validate"
        ]
    },
    {
        "position": 3,
        "name": "@ansible/worker-provision/run",
        "successors": [
            "@ansible/worker-provision/test"
        ],
        "ancestors": [
            "@ansible/worker-provision/plan"
        ]
    }
```

# previous attempt output

```
[  # sequence of threads
[ ["task1", "task2"], ["task3", task4"], [] # sequence of run groups   ],

[ ["task8", "task9"], ["task10", "task11"], [] # sequence of run groups   ],
]
```

* `task1` `task2` can run at the same time
* `task3` `task4` can run at the same time
* `task3` `task4` wait for `task1` `task2` to finish
* `task8` `task9` run at the same time as `task1` `task2`
* `task8` `task9` can run at the same time

With my [parallel-worker](https://github.com/samsquire/parallel-workers) repository is an example how to execute this structure in parallel using python threads.
