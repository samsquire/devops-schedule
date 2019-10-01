# devops-schedule

This script uses ortools to order a tree work graph into a parallelisable runnable schedule.

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
