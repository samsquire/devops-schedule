require 'csp'
require 'json'
require 'pp'


file = File.read("unscheduled.json")

components = JSON.parse(file)

def parallelise_components(components)
	problem = CSP::Solver::Problem.new

	components.each { |item|
		problem.var(item["name"].to_sym, Range.new(0, components.count()))	
	}
	components.each { |item|
		item["ancestors"].each { |ancestor|
			problem.constrain(item["name"].to_sym, ancestor.to_sym) { |this_var, ancestor_var|
				ancestor_var < this_var
			}	

		}
		item["successors"].each { |successor|
			problem.constrain(item["name"].to_sym, successor.to_sym) { |this_var, successor_var|
				this_var < successor_var
			}	

		}
	}

	solved = problem.solve
	components.each { |item|
		item["position"] = solved[item["name"].to_sym]	
	}
	return components.sort_by { |item| item["position"] }
end

PP.pp(parallelise_components(components))

