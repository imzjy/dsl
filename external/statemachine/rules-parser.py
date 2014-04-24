#!/bin/env python

from pyparsing import *
from pprint import pprint

def first(tokens):
	return tokens[0]

def main():
	keywords = oneOf("Events States State")
	word = ~keywords + Word(alphas, alphanums+'_')
	transition = Group(word.setResultsName("f").setParseAction(first) + Word("=>") + word.setResultsName("t").setParseAction(first)).setResultsName("tran")

	states = Group(Word("States", ":") + OneOrMore(word)).setResultsName("states")
	events = Group(Word("Events", ":") + OneOrMore(word)).setResultsName("events")
	transitions = Group(Word("State") + word.setResultsName("state").setParseAction(first) + Word(":") + OneOrMore(transition).setResultsName("trans"))

	rules = events + states + OneOrMore(transitions).setResultsName("transitions")
	rules = rules + stringEnd


	with open("state-transition.rules") as f:
		rule_string = f.read()
	

	#pprint(keywords)
	rules.ignore(cStyleComment)
	tokens = rules.parseString(rule_string)
	#pprint(tokens.states)
	#pprint(tokens.events)

	lookupTable = dict()
	for ts in tokens.transitions:
		print ts.state
		lookupTable[ts.state] = []
		for t in ts.trans:
			print t.f, " goes to ", t.t
			lookupTable[ts.state].append(t.f)
		print ""
	
	pprint(lookupTable)
	


if __name__ == '__main__':
	main()