#!/usr/bin/env python

import numpy
import pickle
import sys


def main():
	numpy.set_printoptions(precision=1, linewidth=284, threshold=40, edgeitems=13)
	filename2 = sys.argv[1]
	print "Loading PCA node from", filename2
	f = open(filename2,  "rb")
	pnode = pickle.load(f)
	f.close()
	print "Loading done"
	filename3 = sys.argv[2]
	print "Loading test pair from", filename3
	f = open(filename3,  "rb")
	testin, testout = pickle.load(f)
	f.close()
	print "Test in:"
	print testin
	testout = pnode.execute(testin)
	print "Testout from file:"
	print testout
	my_testout = pnode.execute(testin)
	print "Testout from here:"
	print my_testout
	print "They are equal:", testout == my_testout

if __name__ == "__main__":
	main()
