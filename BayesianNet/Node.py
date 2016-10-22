#region Node class

# Class that handles each node
class Node:
	# Initialize the Node object
	def __init__(self, index, name, val, parents, children):
		self.index = index #unique index
		self.name = name #unique variable name
		self.val = val
		# assign the given name e.g. -A, +A, or ?A
		if val == 0 or val == 2:
			self.given_name = "-" + name
		elif val == 1 or val == 3:
			self.given_name = "+" + name
		else:
			self.given_name = "?" + name
		# the two possible values that the variable can have e.g. -A or +A
		self.values = ["+" + name, "-" + name]
		# assign the parents and children
		self.parents = parents
		self.children = children
		
	# Adds a parent to the this node and makes it the child of the parent
	def add_parent(self, parent):
		parent.children.append(self)
		self.parents.append(parent)

	# build string representation of P(X|parents(X))
	# returns the probability notation e.g. P(+J|+A)
	def get_formula(self):
		formula = "P(" + self.given_name
		if len(self.parents) > 0: formula = formula + "|"
		for p in self.parents:
			formula = formula + p.given_name + "^"
		formula = formula.strip('^') + ")"
		return formula

	# Prints the node, its value, its parents, and its
	def to_string(self):
		a = "{\nNode: " + self.name + ", Value: " + self.given_name + ",\n"
		a = a + "Parents: {"
		for p in self.parents:
			a = a + "[" + p.name + "]"
		a = a + "}, Children: {" 
		for c in self.children:
			a = a + "[" + c.name + "]"
		a = a + "}\n}\n"
		return a

#endregion Node class