# NFAtoDFA.py :
# This is Python code for representing finite automata, DFAs and NFAs, 
# and for converting from an NFA into a DFA.  
#
# Harry Yan, 7/3/2013
#

class DFA:     
     """Class that encapsulates a DFA."""
     def __init__(self, transitionFunction, initialState, finalStates):
          self.delta = transitionFunction    
          self.q0 = initialState
          self.F = finalStates
          self.current_state = initialState
     def deltaHat(self, state, inputString):
          for a in inputString: 
               state = self.delta[state][a]
          return state
     def inLanguage(self, inputString):
          return self.deltaHat(self.q0, inputString) in self.F

     def alphabet(self):
          """Returns the NFA's input alphabet, generated on the fly."""
          Sigma = set(['1', '0'])
          return Sigma
     def minimizeDFA(self,classes,dfaAlphabet):
          new_states = []
          new_start = None
          new_delta = {}
          new_accepts = []
          new_current_state = None
          state_map = {}
          newdelta = {}

          for state_class in classes:
                  temp = state_class[0]
                  for small in state_class:
                          temp = temp | small
                  new_states.append(temp)
                  for state in new_states:
                    state_map[state] = temp
                    if state == M.q0:
                        new_start = temp

          for state_class in classes:
                  temp1 = state_class[0]
                  for small in state_class:
                          temp1 = temp1 | small
                  newdelta[temp1] = {}
                  for a in dfaAlphabet:
                          nextStates2 = reduce(lambda x,y: x|y, [M.deltaHat(q,a) for q in state_class])
                          if temp1 >= nextStates2:
                                  nextStates2 = temp1
                                  newdelta[temp1][a] = nextStates2
                          else:
                               if nextStates2 in new_states:
                                    for x in new_states:
                                         if x == nextStates2:
                                              nextStates2 = x
                                              newdelta[temp1][a] = nextStates2
                               else:
                                    for x in new_states:
                                         if x > nextStates2 :
                                              nextStates2 = x
                                              newdelta[temp1][a] = nextStates2

          for acc in M.F:
              if acc in new_states:
                  new_accepts.append(acc)

          return newdelta
     def classify(self,classes,dfaAlphabet):
          changed = True
          while changed:
               changed = False
               for cl in classes:
                    local_change = False
                    for alpha in dfaAlphabet:
                         next_class = None
                         new_class = []
                         for state in cl:
                              next = M.delta[state][alpha]
                              if next_class == None:
                                   for c in classes:
                                        if next in c:
                                             next_class = c
                              elif next not in next_class:
                                   new_class.append(state)
                                   changed = True
                                   local_change = True
                         if local_change == True:
                              old_class = []
                              for c in cl:
                                   if c not in new_class:
                                        old_class.append(c)
                              classes.remove(cl)
                              classes.append(old_class)
                              classes.append(new_class)
                              break
          return classes
     
class NFA: 
     """Class that encapsulates an NFA."""
     def __init__(self, transitionFunction, initialState, finalStates,epsilon):
          self.delta = transitionFunction    
          self.q0 = initialState
          self.epsilon = epsilon
          self.F = set(finalStates)
     def eclosure(self,state):
                equal = self.deltaHat(state,self.epsilon)
                return equal
     def eclosureSet(self,state):
                equal = self.deltaHatSet(state,self.epsilon)
                return equal
     def deltaHat(self, state, inputString):
          """deltaHat is smart enough to return the empty set if no transition is defined."""
          states = set([state])
          for a in inputString: 
               newStates = set([])
               for state in states: 
                    try:
                         newStates = newStates | self.delta[state][a]
                    except KeyError: pass
               states = newStates
          return states
     def deltaHatSet(self, state, inputString):
           states = state
           for a in inputString: 
                newStates = set([])
                for state in states: 
                     try:
                          newStates = newStates | self.delta[state][a]
                     except KeyError: pass
                states = newStates
           return states
     def inLanguage(self, inputString):
          return len(self.deltaHat(self.q0, inputString) & self.F) > 0
     def alphabet(self):
          """Returns the NFA's input alphabet, generated on the fly."""
          Sigma = set(['1', '0'])
          return Sigma
     def states(self):
          """Returns the NFA's set of states, generated on the fly."""
          Q = set([self.q0]) | set(self.delta.keys()) | reduce(lambda a,b:a|b, reduce(lambda a,b:a+b, [x.values() for x in self.delta.values()]))     # {q0, all states with outgoing arrows, all with incoming arrows}
          return Q
def convertNFAtoDFA(N):
     """Converts the input NFA into a DFA.  
     
     The output DFA has a state for every *reachable* subset of states in the input NFA.  
     In the worst case, there will be an exponential increase in the number of states.
     """
     eclosureQ0 = N.eclosure(N.q0)
     temp = set([N.q0])
     temp |= eclosureQ0
     N.q0 = temp.copy()
     q0 = frozenset(temp)   # frozensets are hashable, so can key the delta dictionary
     Q = set([q0])
     unprocessedQ = Q.copy() # unprocessedQ tracks states for which delta is not yet defined
     delta = {}
     F = []
     Sigma = N.alphabet()
     count = 0
     qSetM = set([])
     
     while len(unprocessedQ) > 0:
          if count >= 1:
               qSet = unprocessedQ.pop()
               qSetM = qSet
               qSetM |= N.eclosureSet(qSetM)
               qSet = frozenset(qSet)
          else:
               qSet = unprocessedQ.pop()
               qSetM = qSet
          
          count = count+1
          
          delta[qSet] = {}
          for a in Sigma:
               nextStates = reduce(lambda x,y: x|y, [N.deltaHat(q,a) for q in qSetM])
               nextStates = frozenset(nextStates)
               delta[qSet][a] = nextStates
               if not nextStates in Q: 
                    Q.add(nextStates)
                    unprocessedQ.add(nextStates)


     for qSet in Q: 
          if len(qSet & N.F) > 0: 
               F.append(qSet)
     M = DFA(delta, q0, F)
     return M

delta = {'q0':{'0':set(['q0']),'1':set(['q3']),'e':set(['q2','q1'])}, 'q1':{'0':set(['q1','q2']),'1':set(['q3','q0'])}, 'q2':{'0':set(['q2']),'1':set(['q3'])},'q3':{'0':set(['q2','q4']),'1':set(['q3'])},'q4':{'0':set(['q4']),'1':set(['q4'])}}
N = NFA(delta, 'q0', ['q4'],['e'])
M = convertNFAtoDFA(N)
classes = [M.F, [x for x in set(M.delta).difference(set(M.F))]]
dfaAlphabet = M.alphabet()
classes = M.classify(classes,dfaAlphabet)
newdelta2 = M.minimizeDFA(classes,dfaAlphabet)
print(newdelta2)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
