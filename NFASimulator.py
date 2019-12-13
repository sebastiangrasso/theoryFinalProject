import fileinput
import sys
import re

def main():
    transitionRules = {("State", "Input"): ["Transition States"]}
    startState = ""
    acceptState = ""
    i = 0
    
    file = open(sys.argv[1])
    for line in file:
        if i == 0:
            startState = re.search('START=(.*);', line).group(1)
            acceptState = (re.search('ACCEPT=(.*)', line).group(1)).split(',')
            i=i+1
            continue
        parts = (line.rstrip()).split('->')
        stateInput = parts[0].split(':')
        try:
            stateInputTup = (stateInput[0], stateInput[1])
        except IndexError:
            stateInputTup = (stateInput[0], "*")
        if stateInputTup in transitionRules.keys():
            transitionRules[stateInputTup].append(parts[1])
        else:
            transitionRules[stateInputTup] = [parts[1]]
    
    currPossStates = [startState]
    for char in sys.argv[2]:
        nextStates = []
        for states in currPossStates:
            try:
                nextStates.extend(transitionRules.get((states, char)))
            except:
                pass
            try:
                nextStates.extend(transitionRules.get((states, "*")))
            except:
                pass
        currPossStates = nextStates
    
    return any(item in currPossStates for item in acceptState)

if __name__ == "__main__":
    main()
