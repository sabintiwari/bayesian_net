import copy
import io
import json
import os
import sys
import itertools
from network import Network
from node import Node


def normalize(value, net):
	'''
		Normalizes the summation of the provided value by creating
		a constant from the values of different nodes.
	'''
	norm_values = [4 for _ in net.nodes]

	for given_name in net.given:
		for i in range(len(net.nodes)):
			if net.nodes[i].name == given_name[1]:
				norm_values[i] = get_value(given_name)

	norm_net = copy.deepcopy(net)
	norm_net.assign_values(norm_values)
	normalizing_constant = norm_net.solve()

	print(net.conj + " = " + str(value / normalizing_constant))


def get_value(val):
	'''
		Gets the value of the given to calculate the normalizer.
	'''
	if val[0] == "-":
		return 2
	elif val[0] == "+":
		return 3
	return 4


def are_args_valid(args):
	'''
		Checks if the arguments provided to the program are valid.
	'''
	if len(args) == 5:
		#if length of args is 5
		for arg in args:
			#check that all the args are valid
			if not is_int(arg):
				#return False if any of the args is not an integer
				return False
			else:
				arg_int = int(arg)
				if arg_int < 0 or arg_int > 4:
					#return False if the the value is less than 0 or greater than 5
					return False
		#return True if args are valid
		return True
	else:
		#return false if length of args is not 5
		return False


def is_int(val):
	'''
		Checks if the provided value is an integer.
	'''
	try:
		int(val)
		return True
	except ValueError:
		return False

if __name__ == "__main__":
	'''
		Entry point for the program.
	'''
	if len(sys.argv) < 2:
		sys.exit("Error! The program requires the path to the json config file that contains the network information.")

	config_path = os.path.normpath(sys.argv[1])
	if not os.path.isfile(sys.argv[1]):
		sys.exit("Error! Config file not found: " + config_path)

	with open(config_path, "r", encoding="utf-8") as cf:
		config_str = cf.read()
		config_json = json.loads(config_str)
		if (config_json["nodes"] is None or len(config_json["nodes"]) == 0):
			sys.exit("Error! Config file requires a 'nodes' attribute with a list of nodes in the network.")
		if (config_json["factors"] is None or len(config_json["factors"].keys()) == 0):
			sys.exit("Error! Config file requires a 'factors' attribute with a mapping for factors to use.")

	net = Network(config_json["nodes"], config_json["factors"])
	end = False
	
	while not end:
		values = input("Enter a list of values for the following nodes\n, " + " ".join([node.name for node in net.nodes]) + " separated by spaces:")
		if len(values) != len(net.nodes):
			print("Error: The program takes exactly 5 integer command line arguments between 0 - 4.\n\tE.g. 2 4 3 4 4")
			continue

		value = net.solve()
		if not value is None:
			if net.has_evidence:
				normalize(value, net)
			else:
				print(net.conj + " = " + str(value))