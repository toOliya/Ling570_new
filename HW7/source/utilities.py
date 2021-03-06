import re
import math

class Utilities:
        def __init__(self):
                self.current_init_dict = {}
                self.current_trans_dict = {}  
                self.current_inverse_trans_dict = {}
                self.current_emiss_dict = {}
		self.current_symb_dict = {}

                self.flattenedStates = {} 

                self.init_state = "init_state"
                self.trans_state = "trans_state"
                self.emiss_state = "emiss_state"

                self.currentState = self.init_state

        def buildFlattenedStates(self):
                self.flattenedStates = {}
                for fromState in self.current_trans_dict:

                        if(not self.flattenedStates.has_key(fromState)):
                                self.flattenedStates[fromState] = None

                        for toState in self.current_trans_dict[fromState]:
                                if(not self.flattenedStates.has_key(toState)):
                                        self.flattenedStates[toState] = None

	def ReadObsStr(self, StrVal):
		splitVals = re.split("\s+", StrVal)
		return splitVals

	def readInput(self, hmmInputLine):
                if(hmmInputLine.strip() == ""):
                        return

		lineContents = re.split("\s+", hmmInputLine.strip())
		if len(lineContents) > 0:
			firstItem = lineContents[0]
			if firstItem == '\\init':
				self.currentState = self.init_state			
					
                if(self.currentState == self.init_state):
                        lineContents = re.split("\s+", hmmInputLine.strip())

                        # assuming that 1st is from_state(s), 2rd is prob
                        if(len(lineContents) > 0):
                                firstItem = lineContents[0]
                                if(firstItem == '\\transition'):

                                        self.currentState = self.trans_state
                                elif(len(lineContents) > 1):
                                        # build up init dictionary
                                        self.current_init_dict[firstItem] = float(lineContents[1])
                
                elif(self.currentState == self.trans_state):
                        lineContents = re.split("\s+", hmmInputLine.strip())

                        # assuming that 1st is from_state(s), 2nd is prob
                        if(len(lineContents) > 0):
                                firstItem = lineContents[0]
                                if(firstItem == '\\emission'):
                                        self.currentState = self.emiss_state
                                elif(len(lineContents) > 2):
                                        to_state = lineContents[1]
                                        prob = float(lineContents[2])

                                        if(prob != 0.0):
                                                prob = math.log10(prob)

                                        if(self.current_trans_dict.has_key(firstItem)):
                                                self.current_trans_dict[firstItem][to_state] = prob
                                        else:
                                                self.current_trans_dict[firstItem] = { to_state: prob }

                                        if(self.current_inverse_trans_dict.has_key(to_state)):
                                                self.current_inverse_trans_dict[to_state][firstItem] = prob
                                        else:
                                                self.current_inverse_trans_dict[to_state] = { firstItem: prob }

                elif(self.currentState == self.emiss_state):
                        lineContents = re.split("\s+", hmmInputLine.strip())

                        # assuming that 1st is from_state(s), 2nd is prob
                        if(len(lineContents) > 0):
                                firstItem = lineContents[0]

                                if(len(lineContents) > 2):
                                        symbol = lineContents[1]
                                        prob = float(lineContents[2])

                                        if(prob != 0.0):
                                                prob = math.log10(prob)

                                        if(self.current_emiss_dict.has_key(firstItem)):
                                                self.current_emiss_dict[firstItem][symbol] = prob
                                        else:
                                                self.current_emiss_dict[firstItem] = { symbol: prob }

					if (self.current_symb_dict.has_key(symbol)):
						self.current_symb_dict[symbol][firstItem] = prob
					else:
						self.current_symb_dict[symbol] = {firstItem : prob}
