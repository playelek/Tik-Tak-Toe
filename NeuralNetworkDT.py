import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from dense import Dense
from activations import Tanh, Sigmoid
from losses import mse, mse_prime
from network import train, predict

import json
import os
import sys
import random

class NeuralNetwork: 
    stepList = []
    invert_stepList = []
    state_action = {}
    state_action_model = {
        'state' : [],
        'score' : 0
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

    def __init__(self):
        self.versions = "1.0"
        self.name = "markov"

    def load_state_action(self , fname = None):
        if fname == None:
            fname = self.state_action_fname
        print("current file : {}".format(fname))
        flists = open("{}".format(fname), 'r')
        print("flist was open : {}".format(flists))
        dat = flists.read()
        if (self.debugShow == True):
            print("JSON data : {}".format(dat))
        if dat :
            self.state_action = json.loads(dat)

        else:
            self.state_action = {}
        # print("state_action : {}".format(self.state_action))

    def save_state_action(self , fname = None):
        if fname == None:
            fname = self.state_action_fname
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
        if len(self.state_action) == 0:
            return '-1' , []
        for keys , value in self.state_action.items():
            # print("keys : {} - value : {}".format(keys, value))
            if state == value['state']:
                return keys , value["state"]
        return '-1' , []  

    def update_state_action(self , state = None , goal = None):
        keys_state = '-1'
        score_state = 0

        if (goal == None) or (goal == 0):
            score_state = 0
        else:
            score_state = goal

        keys_state , value_state = self.find_state(state)
        if keys_state == '-1':
            thisState = str("{}".format(len(self.state_action)))
            thisStateDict = {
                'state' : list(state),
                'score' : score_state
            }
            self.state_action[thisState] = thisStateDict
            keys_state = thisState

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