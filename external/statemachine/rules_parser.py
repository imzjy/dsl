#!/bin/env python

from pyparsing import *
from pprint import pprint

def first_as_str(tokens):
	return str(tokens[0])

def first_as_int(tokens):
	return int(tokens[0])

def get_tokens():
	keywords = oneOf("Events States State")
	word = ~keywords + Word(alphas, alphanums+'_')
	transition = Group(word.setResultsName("f").setParseAction(first_as_str) + 
		Word("=>") + 
		word.setResultsName("t").setParseAction(first_as_str)).setResultsName("tran")

	states = Group(Word("States", ":") + OneOrMore(word)).setResultsName("states")
	events = Group(Word("Events", ":") + OneOrMore(word)).setResultsName("events")
	transitions = Group(Word("State") + 
		word.setResultsName("state").setParseAction(first_as_str) + 
		Word(":") + 
		OneOrMore(transition).setResultsName("trans"))

	rules = events + states + OneOrMore(transitions).setResultsName("transitions")
	rules = rules + stringEnd


	with open("state_transition.rules") as f:
		rule_string = f.read()
	

	#pprint(keywords)
	rules.ignore(cStyleComment)
	tokens = rules.parseString(rule_string)
	#pprint(tokens.states)
	#pprint(tokens.events)
	return tokens

def get_acceptable_events_table():

	tokens = get_tokens()

	lookup_table = dict()
	for ts in tokens.transitions:
		#print ts.state
		lookup_table[ts.state] = []
		for t in ts.trans:
			#print t.f, " goes to ", t.t
			lookup_table[ts.state].append(t.f)
		#print ""
	
	global_events = lookup_table.pop("ALL", [])
	extend_table = dict()
	for k, v in lookup_table.items():
		extend_table[k] = v + global_events
	
	return extend_table

def get_transit_table():
	tokens = get_tokens()

	lookup_table = dict()
	for ts in tokens.transitions:
		lookup_table[ts.state] = dict()
		for t in ts.trans:
			lookup_table[ts.state][t.f] = t.t

	global_events = lookup_table.pop("ALL", [])
	extend_transit_table = dict()
	for k, v in lookup_table.items():
		extend_transit_table[k] = dict(global_events.items() + v.items())

	# pprint(extend_transit_table)

	return extend_transit_table

if __name__ == '__main__':
	get_acceptable_events_table()
	get_transit_table()