import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from dense import Dense
from activations import Tanh, Sigmoid

from execution import Execution

import json
import os
import sys
import random

class NeuralNetwork: 
    stepList = []
    invert_stepList = []
    state_action = {        
        'X' : [],
        'O' : [],
        'D' : []
    }
    state_action_model = {
        'state' : [],
        'score' : []
    }
    playFirst = False
    dirpath = os.path.dirname(sys.argv[0])
    state_action_fname = "neuralnetwork_action.json"

    listEdge = []
    dictEdgeScore = {}

    resultStat = {  'Games' : 0,
                    'win' : 0,
                    'loss' : 0,
                    'draw' : 0
                }

    updateGraph = False
    debugShow = False

    network = [
        Dense(9, 18),
        Tanh(),
        Dense(18, 9),
        Tanh(),
        Dense(9, 9),
        Tanh(),
        Dense(9, 4),
        Tanh(),
        Dense(4, 1),
        Tanh()
    ]

    # initial execution
    exect = Execution(network, "loss", True, 0.1)

    def __init__(self):
        self.versions = "1.0"
        self.name = "NeuralNetwork"

    def load_state_action(self , fname = None):
        if fname == None:
            fname = self.state_action_fname
        print("current file : {}".format(fname))
        flists = open("{}".format(fname), 'r')
        print("flist was open : {}".format(flists))
        dat = flists.read()
        if (self.debugShow == True):
            print("JSON data : {}".format(dat))
        if len(dat) > 0 :
            X = list()
            Y = list()
            self.state_action = json.loads(dat)
            for keys, values in self.state_action.items():
                for state in values:
                    if keys == 'X':
                        X.append(state)
                        Y.append(1)
                    elif keys == 'O':
                        X.append(state)
                        Y.append(-1)
                    else:   
                        X.append(state)
                        Y.append(0) 
            # train
            if len(X) > 0 and len(Y) > 0:
                listError = self.exect.train(x_train= np.reshape(X,(len(X), 9, 1)), y_train= np.reshape(Y, (len(Y), 1, 1)), epochs=500)
                print("this coeff : {}".format(self.exect.coeff))

        else:
            self.state_action = {        
                'X' : [],
                'O' : [],
                'D' : []
            }
        # print("state_action : {}".format(self.state_action))

    def save_state_action(self , fname = None, state = None, goal = None):
        keys_state = '-1'
        score_state = 0

        if fname == None:
            fname = self.state_action_fname

        if (goal == None) or (goal == 0):
            score_state = 0
        else:
            score_state = goal

        keys_state , value_state = self.find_state(state)  
        print("state : {} - goal : {} - keys : {} - value : {}".format(state, goal, keys_state , value_state))
        if keys_state == '-1':
            if goal == -1:
                if len(self.state_action["O"])>15 :
                    self.state_action["O"].pop(0)
                self.state_action["O"].append(state)
            elif goal == 1:
                if len(self.state_action["X"])>15 :
                    self.state_action["X"].pop(0)
                self.state_action["X"].append(state)
            elif goal == 0:
                if len(self.state_action["D"])>15 :
                    self.state_action["D"].pop(0)
                self.state_action["D"].append(state)

        state_action_json = json.dumps(self.state_action, indent=4)
        print("current file : {}".format(fname))
        flists = open("{}".format(fname), 'w')
        print("flist was open")
        flists.write(state_action_json)
        flists.close()
        print("flist was closed")

    def find_state(self , state = None):
        if state == None:
            return '-1' , []
        if len(self.state_action["X"]) > 0:
            if state in self.state_action["X"]:
                return 0 , list(state)            
        if len(self.state_action["O"]) > 0:
            if state in self.state_action["O"]:
                return 0 , list(state) 
        if len(self.state_action["D"]) > 0:
            if state in self.state_action["D"]:
                return 0 , list(state) 
        return '-1' , list(state)  

    def updateResult(self ,winner = 0):
        playas = 0
        if self.playFirst :
            playas = 1
        else :
            playas = -1
        self.resultStat['Games'] += 1
        if winner == 0 :
            self.resultStat['draw'] += 1
        elif winner == playas:
            self.resultStat['win'] += 1
        else:
            self.resultStat['loss'] += 1

    def find_bestPlay(self , state = None , playas = 0):
        aval_block = []
        left_block = []
        play_block = 0
        nextState = []
        thisBlock = []
        thisState = list(state)
        self.listEdge = []
        self.dictEdgeScore = {}
        dictScore = {"block":0, "score":0.5*playas}
        if state == None:
            return 0
        for pos in range(len(state)):
            if state[pos] == 0:
                aval_block.append(pos+1)
        print("find_bestPlay get aval_block : {}".format(aval_block)) 
        left_block = list(aval_block)
        for eachBlock in left_block:
            thisState[eachBlock-1] = playas
            # print("find_bestPlay get block : {} - thisState : {}".format(eachBlock, thisState)) 
            thisBlock = list()
            for a in thisState:
                thisBlock.append([a])
            # print("find_bestPlay get block : {} - thisBlock : {}".format(eachBlock, thisBlock))
            thisScore = self.exect.predict(input= thisBlock).item()
            thisState[eachBlock-1] = 0
            print("find_bestPlay get block : {} - thisScore : {} - {}".format(eachBlock, thisScore, type(thisScore))) 
            if playas > 0:
                if thisScore > dictScore["score"]:
                    dictScore["block"] = eachBlock
                    dictScore["score"] = thisScore
            elif playas < 0:
                if thisScore < dictScore["score"]:
                    dictScore["block"] = eachBlock
                    dictScore["score"] = thisScore
            # print("find_bestPlay playas : {} - get play : {} with score : {}".format(playas,dictScore["block"],dictScore["score"])) 
        print("find_bestPlay playas : {} - get play : {} with score : {}".format(playas,dictScore["block"],dictScore["score"])) 
        play_block = dictScore["block"]
        if play_block == 0:
            play_block = random.choice(left_block)
            print("find_bestPlay random play_block : {}".format(play_block))
        return play_block 