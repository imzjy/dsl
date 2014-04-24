#!/bin/env python

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

		if state == "idle":
			return ("reset", "doorOpen")
		elif state == "active":
			return ("reset", "lightOn", "drawerOpen")
		elif state == "waitingForDrawer":
			return ("reset", "drawerOpen")
		elif state == "waitingForLight":
			return ("reset", "lightOn")
		elif state == "unlockPanel":
			return ("reset", "doorClose")

	@staticmethod
	def get_transit_table(state):
		transit_table = dict()
		transit_table["reset"] = "idle"

		if state == "idle":
			transit_table["doorOpen"] = "active"
		elif state == "active":
			transit_table["lightOn"] = "waitingForDrawer"
			transit_table["drawerOpen"] = "waitingForLight"
		elif state == "waitingForDrawer":
			transit_table["drawerOpen"] = "unlockPanel"
		elif state == "waitingForLight":
			transit_table["lightOn"] = "unlockPanel"
		elif state == "unlockPanel":
			transit_table["doorClose"] = "idle"

		return transit_table



if __name__ == '__main__':
	
	stateMachine = StateMachine("idle")
	stateMachine.transit("lightOn")
	stateMachine.transit("doorOpen")
	stateMachine.transit("reset")

	stateMachine.transit("doorOpen")
	stateMachine.transit("drawerOpen")
	stateMachine.transit("lightOn")
	stateMachine.transit("doorClose")