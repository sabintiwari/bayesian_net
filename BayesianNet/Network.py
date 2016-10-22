#region Network class
from Node import Node

# Class that handles the Network of variables and their probabilties
class Network:
	# Initialize the Network object
	def __init__(self, a, b, e, j, m):
		self.nodes = []
		self.given = []
		self.factors = {}
		self.conj = ""
		self.has_evidence = False
		self.values = ["+", "-"]

		# set the variables based on the table
		self.nodes.append(Node(0, "A", a, [], []))
		self.nodes.append(Node(1, "B", b, [], []))
		self.nodes.append(Node(2, "E", e, [], []))
		self.nodes.append(Node(3, "J", j, [], []))
		self.nodes.append(Node(4, "M", m, [], []))

		# set the edges based on the table
		self.assign_parent("J", "A")
		self.assign_parent("M", "A")
		self.assign_parent("A", "B")
		self.assign_parent("A", "E")

		# set the unobserved to contain all the nodes until the formulation is done
		self.unobserved = list(self.nodes)

		# assign the values from the table
		self.factors = {"P(+B)": 0.001, "P(+E)": 0.002, "P(+A|+B^+E)": 0.95, "P(+A|+B^-E)": 0.94, "P(+A|-B^+E)": 0.29, "P(+A|-B^-E)": 0.001, "P(+J|+A)": 0.90, "P(+J|-A)": 0.05, "P(+M|+A)": 0.70, "P(+M|-A)": 0.01}

	# Solves the conjunction
	def solve(self):
		# Formulates the given values
		self.conj = self.formulate()
		# if the conjuction is valid
		if not self.conj == "ERROR: BAD QUERY":
			# build the formula
			formula = []
			for node in self.nodes:
				formula.append(node.get_formula())
			# calculate the summations
			summation = self.f(formula, self.create_summation_tuples(self.unobserved))
			return summation
		# if the conjunction is not valid
		return None

	# Creates the tuples of all possible values using the possible_values method
	# returns the tuples
	def create_summation_tuples(self, unobserved):
		values = []
		summation_tuple = []
		for var in unobserved:
			values.append(var.values)
		return self.possible_values(values)
	
	# Gets all the possible values using the combitnation from the lists
	def possible_values(self, lists):
		if lists == []:
			return [()]
		return [x + (y,) for x in self.possible_values(lists[:-1]) for y in lists[-1]]

	# Sums the formula based on the tuples of unobserved variables
	# returns the net product and sum
	def f(self, formula, tuples):
		formulas = []
		# create all the formulas with the updated possiblities of the unobserved variables
		for var in tuples:
			with_values = []
			for fmla in formula:
				for i in var:
					fmla = fmla.replace("?" + i[1], i)
				with_values.append(fmla)
			formulas.append(with_values)
		
		# get the summation
		total_sum = 0
		for fmla in formulas:
			total_product = 1
			# print fmla
			for sub_fmla in fmla:
				# get the value of the formula from the table values stored in self.factors
				value = self.check_value(sub_fmla)
				total_product = total_product * value
				# print sub_fmla + ": " + str(value)
				# print "Total Value: " + str(total_product)
			total_sum = total_sum + total_product
		return total_sum

	# Gets the node with the given name
	# return a node if found
	def get_node(self, name):
		for node in self.nodes:
			if node.name == name:
				return node
		return None

	# Checks if the value of the formula is given in self.factors
	def check_value(self, formula):
		is_negative = False
		formula_list = list(formula)
		# if the formulat is checking for negative of a given, keep track
		if formula_list[2] == "-":
			is_negative = True
			formula_list[2] = "+"
		formula = "".join(formula_list)
		if formula in self.factors:
			# if the formula is negative get 1 - the value
			if is_negative:
				return 1 - self.factors[formula]
			# else return the value from the dictionary
			else:
				return self.factors[formula]
		return 1.0

	# Formulates the given parameters
	# modifies the self.unobserved and self.given lists
	# the formula itself is just for display purposes, the calculation 
	#	is done using the given and unobserved variables
	# return the string formula e.g. 2 4 3 4 4 -> P(-A^+E)
	def formulate(self):
		query = []
		given = []
		# check all the nodes for what they represent in the given values
		for node in self.nodes:
			if node.val == 0 or node.val == 1:
				given.append(node.given_name)
				self.unobserved.remove(node)
			elif node.val == 2 or node.val == 3:
				query.append(node.given_name)
				self.unobserved.remove(node)
		# build and return the formula
		self.given = list(given)
		# if there is evidence, mark the value 'has_evidence' which means we need to normalize
		if len(given) > 0:
			self.has_evidence = True
		# build the probability notation from the given values
		formula = "P("
		# add the query variables
		for q in query:
			formula = formula + q + "^"
		formula = formula.strip('^')
		#add the given variables
		if len(given) > 0:
			formula = formula + "|"
		for g in given:
			formula = formula + g + "^"
		formula = formula.strip('^') + ")"
		# return error if there are no query variables
		if len(query) == 0:
			print("Invalid formula provided. " + formula)
			return "ERROR: BAD QUERY"
		# return the string formula
		return formula 

	# Assigns b as the parent of a
	def assign_parent(self, a, b):
		self.nodes[self.get_node(a).index].add_parent(self.nodes[self.get_node(b).index])

#endregion Network class