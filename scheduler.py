import collections
from ortools.sat.python import cp_model
from pprint import pprint
 

def parallelise_components(component_data):
    """Schedule components for maximum paralellism"""
    model = cp_model.CpModel()
    
    component_vars = {}
    task_run = collections.namedtuple('task_run', 'start group')
    horizon = len(component_data)
    
    for component in component_data:
        suffix = component["name"]
        start_var = model.NewIntVar(0, horizon, 'start/' + suffix)
        group_var = model.NewIntVar(0, 100, 'group/' + suffix)
        component_vars[suffix] = task_run(start_var, group_var)
        
    parallel_group = collections.defaultdict(list)
    successor_lookup = {}
    for component in component_data:
        this_var = component_vars[component["name"]]
        
        for ancestor in component["ancestors"]:
            model.Add(component_vars[ancestor].start < this_var.start)
            # model.Add(component_vars[ancestor].group == this_var.group)       
        for successor in component["successors"]:
            model.Add(component_vars[successor].start > this_var.start)
        successor_lookup[component["name"]] = component["successors"]
        
        
        
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    orderings = collections.defaultdict(list)
    positions = {}
    roots = []
    threads = []
    thread_list = []
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        for component in component_data:
            position = solver.Value(component_vars[component["name"]].start)
            positions[component["name"]] = position
            orderings[position].append(component["name"])
            
        highest = max(positions.values())
        
        def append_children(positions, thread, item):
            for child in successor_lookup[item]:
                thread[positions[child]].append(child)
                append_children(positions, thread, child)

        def dict_to_list(things):
            items = []
            for key in sorted(things):
                items.append(things[key])
            return items

        for item in orderings[0]:
            thread = collections.defaultdict(list)
            threads.append(thread)
            thread[0] = [item]
            append_children(positions, thread, item)
        
        for index, thread in enumerate(threads):
            threads[index] = dict_to_list(threads[index])
        
    return threads

#parallelisable_builds = parallelise_components(component_data = [
#
#      {
#          "name": "terraform/vpc/plan",
#          "ancestors": ["terraform/vpc/validate"],
#          "successors": ["terraform/vpc/run"]
#      },
#      {
#          "name": "terraform/vpc/run",
#          "ancestors": ["terraform/vpc/plan"],
#          "successors": ["terraform/vpc/test", "terraform/vpc/deploy"]
#      },
#      {
#          "name": "terraform/vpc/deploy",
#          "ancestors": ["terraform/vpc/run"],
#          "successors": []
#      },
#      {
#          "name": "terraform/vpc/test",
#          "ancestors": ["terraform/vpc/run"],
#          "successors": ["integration"]
#      },
#
#      {
#          "name": "terraform/users/validate",
#          "ancestors": [],
#          "successors": ["terraform/users/plan"]
#      },
#      {
#          "name": "terraform/users/plan",
#          "ancestors": ["terraform/users/validate"],
#          "successors": ["terraform/users/run"]
#      },
#      {
#          "name": "terraform/users/run",
#          "ancestors": ["terraform/users/plan"],
#          "successors": ["terraform/users/test"]
#      },
#      {
#          "name": "terraform/users/test",
#          "ancestors": ["terraform/users/run"],
#          "successors": ["integration"]
#      },
#      {
#          "name": "terraform/vpc/validate",
#          "ancestors": [],
#          "successors": ["terraform/vpc/plan"]
#      },
#      {   "name": "integration",
#        "ancestors": ["terraform/vpc/test", "terraform/users/test"],
#        "successors": ["terraform/services/validate"]
#      },
#      {
#        "name": "terraform/services/validate",
#        "ancestors": ["integration"],
#        "successors": []
#      },
#
#
#      {
#          "name": "terraform/bastion/plan",
#          "ancestors": ["terraform/bastion/validate"],
#          "successors": ["terraform/bastion/run"]
#      },
#      {
#          "name": "terraform/bastion/run",
#          "ancestors": ["terraform/bastion/plan"],
#          "successors": ["terraform/bastion/test"]
#      },
#      {
#          "name": "terraform/bastion/deploy",
#          "ancestors": ["terraform/bastion/run"],
#          "successors": []
#      },
#      {
#          "name": "terraform/bastion/test",
#          "ancestors": ["terraform/bastion/run"],
#          "successors": []
#      },
#      {
#          "name": "terraform/bastion/validate",
#          "ancestors": [],
#          "successors": ["terraform/bastion/plan"]
#      },
#
#
#      
# ])
#pprint(parallelisable_builds)