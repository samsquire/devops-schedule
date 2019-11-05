var csp = require('csp.js');

var data = [{
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
    }]
	
function parallelise_components(data) {
	var p = csp.DiscreteProblem();
	const variables = {}
	var domain = [];
	for (var k = 0 ; k < data.length ; k++) {
		domain.push(k);
	}
	for (var i = 0 ; i < data.length; i++) {
		var component = data[i];
		p.addVariable(component.name, domain);
	}
	for (var i = 0 ; i < data.length; i++) {
		var component = data[i];
		for (var j = 0 ; j < component.successors.length; j++) {
			p.addConstraint([component.name, component.successors[j]],
			function (component, successor) { return component < successor});
		}
		
		for (var j = 0 ; j < component.ancestors.length; j++) {
			p.addConstraint([component.name, component.ancestors[j]],
			function (component, ancestor) { return ancestor < component});
		}
		
	}
	var solution = p.getSolution();
	var answers = []
	for (var i = 0 ; i < data.length; i++) {
		answers.push(Object.assign({}, data[i]));
		answers[i].position = solution[answers[i].name]
	}
	return answers;
}

console.log(parallelise_components(data));