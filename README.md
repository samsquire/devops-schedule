# devops-schedule

This script uses ortools to order a tree work graph into a parallelisable runnable schedule.

```
[  # sequence of threads
[ ["task1", "task2"], ["task3", task4"], [] # sequence of run groups   ],

[ [], [], [] # sequence of run groups   ],
]
```

`task1` `task2` can run at the same time
`task3` `task4` can run at the same time
`task3` `task4` wait for `task1` `task2` to finish

With my [parallel-worker](https://github.com/samsquire/parallel-workers) repository is an example how to execute this structure in parallel.
