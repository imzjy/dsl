#!/bin/env python

import rules_parser as r

class StateMachine(object):
	"""
	StateMachine which hold the current state and enable the state transition based on rules file
	"""
	def __init__(self, state):
		super(StateMachine, self).__init__()
		self.state = state

	def transit(self, event):
		acceptable_events = Rules.get_acceptable_events(self.state)
		if not (event in acceptable_events):
			print "error, only accept following events: when state is " + self.state
			for e in acceptable_events:
				print "  " + e
			return
		self.__transit_to(event)

	def __transit_to(self, event):
		transit_table = Rules.get_transit_table(self.state)
		print "transit to " + transit_table[event]
		self.state = transit_table[event]

class Rules(object):
	"""docstring for Rules"""
	def __init__(self):
		super(Rules, self).__init__()

	@staticmethod
	def get_acceptable_events(state):

		events_table = r.get_acceptable_events_table()
		return events_table[state]

	@staticmethod
	def get_transit_table(state):
		transit_table = r.get_transit_table()

		return transit_table[state]


if __name__ == '__main__':
	
	#test case
	stateMachine = StateMachine("idle")
	stateMachine.transit("lightOn")
	stateMachine.transit("doorOpen")

	#reset
	stateMachine.transit("reset")

	#whole process
	stateMachine.transit("doorOpen")
	stateMachine.transit("drawerOpen")
	stateMachine.transit("lightOn")
	stateMachine.transit("doorClose")