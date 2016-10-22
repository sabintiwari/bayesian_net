#import files
import sys
import itertools

#interal classes
from Network import Network
from Node import Node

#region Execution methods

# Main method         
def main(args):
	del args[0]
	if are_args_valid(args):
		net = Network(int(args[0]), int(args[1]), int(args[2]), int(args[3]), int(args[4]))
		value = net.solve()
		if not value is None:
			if net.has_evidence:
				normalize(value, net.given, net.conj)
			else:
				print(net.conj + " = " + stringify(value))
	else:
		print("Error: The program takes exactly 5 integer command line arguments between 0 - 4.\n\tE.g. 2 4 3 4 4")

# Normalize the summation
def normalize(value, given, conj):
	a = 4
	b = 4
	e = 4
	j = 4
	m = 4
	for g in given:
		if g[1] == "A":
			a = get_value(g)
		elif g[1] == "B":
			b = get_value(g)
		elif g[1] == "E":
			e = get_value(g)
		elif g[1] == "J":
			j = get_value(g)
		elif g[1] == "M":
			m = get_value(g)
	norm_net = Network(a, b, e, j, m)
	normalizing_constant = norm_net.solve()
	print(conj + " = " + stringify(value / normalizing_constant))

def stringify(value):
	return str(value)

# Gets the value of the given to calculate the normalizer
def get_value(val):
	if val[0] == "-":
		return 2
	elif val[0] == "+":
		return 3
	return 4

# Checks if the arguments are valid
def are_args_valid(args):
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

# Checks if the value is an integer
def is_int(val):
	try:
		int(val)
		return True
	except ValueError:
		return False

#endregion Execution methods

# Call the main method with the arguments
main(sys.argv)