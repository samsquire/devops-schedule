from threading import Thread

work =   [{
        "position": 0,
        "name": "@ansible/machines/package",
        "successors": [
            "@ansible/machines/validate"
        ],
        "ancestors": []
    },
    {
        "position": 1,
        "name": "@ansible/machines/validate",
        "successors": [
            "@ansible/machines/plan"
        ],
        "ancestors": [
            "@ansible/machines/package"
        ]
    },
    {
        "position": 2,
        "name": "@ansible/machines/plan",
        "successors": [
            "@ansible/machines/run"
        ],
        "ancestors": [
            "@ansible/machines/validate"
        ]
    },
    {
        "position": 3,
        "name": "@ansible/machines/run",
        "successors": [
            "@ansible/machines/test",
			"@ansible/provision-workers"
        ],
        "ancestors": [
            "@ansible/machines/plan"
        ]
    },
	{
	"position": 4,
	"name": "@ansible/provision-workers",
	"successors": [
	  
	],
	"ancestors": [

	]
	},
		{
	"position": 5,
	"name": "@ansible/machines/test",
	"successors": [
	  
	],
	"ancestors": [
		"@ansible/machines/run"
	]
	}
]

class Worker(Thread):
	def __init__(self, threads, item):
		super(Worker, self).__init__()
		self.threads = threads
		self.item = item
		
	def run(self):
		for parent in item["ancestors"]:
			threads[parent].join()
		print("<- {}".format(self.item["name"]))

threads = {}
for item in work:
	threads[item["name"]] = Worker(threads, item)
for item in work:
	threads[item["name"]].start()

	