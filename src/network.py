from node import Node

# Class that handles the Network of variables and their probabilties
class Network:
	'''
		Initializes a Bayesian network with the provided list of nodes
		and the factors.
		
		@params:
			nodes: List of nodes to initialize. Each node should have an unique name, and a list of parents.
			factors: The mapping of the initialization factors.
	'''
	def __init__(self, nodes, factors):
		self.nodes = []
		self.given = []
		self.factors = {}
		self.conj = ""
		self.has_evidence = False
		self.values = ["+", "-"]

		# set the variables based on the table
		for i in range(len(nodes)):
			nodeObj = Node(i, nodes[i])
			self.nodes.append(nodeObj)

		# set the edges based on the table
		for node in nodes:
			for parent in node.parents:
				self.assign_parent(node["name"], parent)

		# set the unobserved to contain all the nodes until the formulation is done
		self.unobserved = list(self.nodes)

		# assign the values from the table
		self.factors = factors

	def assign_values(self, values):
		'''
			Assigns the values provided in the list
			to the nodes contained in this network.
		'''
		for i in range(len(self.nodes)):
			self.nodes[i].val = values[i]

	def solve(self):
		'''
			Solves the conjunction.
		'''
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

	def create_summation_tuples(self, unobserved):
		'''
			Creates the tuples of all possible values using the possible_values method
			
			@returns
				the tuples containing the summation values
		'''
		values = []

		for var in unobserved:
			values.append(var.values)

		return self.possible_values(values)
	
	def possible_values(self, lists):
		'''
			Gets all the possible values using the combitnation from the lists.
		'''
		if lists == []:
			return [()]

		return [x + (y,) for x in self.possible_values(lists[:-1]) for y in lists[-1]]

	def f(self, formula, tuples):
		'''
			Sums the formula based on the tuples of unobserved variables
			returns the net product and sum.
		'''
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

			# calculate the value of the formula
			for sub_fmla in fmla:
				# get the value of the formula from the table values stored in self.factors
				value = self.check_value(sub_fmla)
				total_product = total_product * value

			# add the product value to the total sum
			total_sum += total_product

		return total_sum
		
	def get_node(self, name):
		'''
			Gets the node with the given name return a node if found.
		'''
		for node in self.nodes:
			if node.name == name:
				return node
		return None

	def check_value(self, formula):
		'''
			Checks if the value of the formula is given in self.factors.
		'''
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

	def formulate(self):
		'''
			Formulates the given parameters modifies the self.unobserved and self.given lists.
			The formula itself is just for display purposes, the calculation is done using the
			given and unobserved variables.
			
			@returns
				the string represention of the formula e.g. 2 4 3 4 4 as P(-A^+E)
		'''
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
		if len(self.given) > 0:
			self.has_evidence = True

		# build the probability notation from the given values
		formula = "P("

		# add the query variables
		for q in query:
			formula = formula + q + "^"
		formula = formula.strip('^')

		#add the given variables
		if len(self.given) > 0:
			formula = formula + "|"
		for g in self.given:
			formula = formula + g + "^"
		formula = formula.strip('^') + ")"

		# return error if there are no query variables
		if len(query) == 0:
			print("Invalid formula provided. " + formula)
			return "ERROR: BAD QUERY"
		
		# return the string formula
		return formula 

	def assign_parent(self, a, b):
		'''
			Assigns b as the parent of a.

			@params:
				a: the node to make the child of b
				b: the node to make the parent of a
		'''
		self.nodes[self.get_node(a).index].add_parent(self.nodes[self.get_node(b).index])