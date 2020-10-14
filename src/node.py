import json


class Node:
	'''
		Initializes an object of the Node class.
		
		@params:
			index: unique index for the current node
			node: the json object for the node
	'''
	def __init__(self, i, node):
		self.index = i
		self.name = node["name"]
		self.formula = ""

		self.values = ["+" + self.name, "-" + self.name]

		self.parents = []
		self.children = []

	def add_parent(self, parent):
		'''
			Adds a parent to the this node and makes it the child of the parent.
		'''
		parent.children.append(self)
		self.parents.append(parent)

	def get_formula(self):
		'''
			Builds string representation of P(X|parents(X)).

			@returns:
				probability notation e.g. P(+J|+A)
		'''
		formula = "P(" + self.given_name

		if len(self.parents) > 0:
			 formula +=  "|"
		parent_names = "^".join([p.given_name for p in self.parents])

		formula += parent_names + ")"
		return formula

	def to_json(self):
		'''
			Gets the current node as a json object.
		'''
		jsonObj = {
			"name": self.name,
			"value": self.given_name,
			"parents": [p.name for p in self.parents],
			"children": [c.name for c in self.children]
		}

		jsonDump = json.dumps(jsonObj)
		return jsonDump

	def to_string(self):
		'''
			Gets the current node, its value, its parents, and its children
			as a string value.
		'''
		jsonVal = self.to_json()
		return str(jsonVal)