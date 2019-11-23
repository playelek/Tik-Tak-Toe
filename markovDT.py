import json
import os
import sys
import random
import networkx as nx
import matplotlib.pyplot as plt

class markov: 
    stepList = []
    invert_stepList = []
    state_action = {}
    state_action_model = {
        'state' : [],
        'next' : [],
        'score' : 0,
        'end' : False
    }
    discount = 0.9
    playFirst = False
    dirpath = os.path.dirname(sys.argv[0])
    state_action_fname = "state_action.json"

    listEdge = []
    dictEdgeScore = {}

    resultStat = {  'Games' : 0,
                    'win' : 0,
                    'loss' : 0,
                    'draw' : 0
                }

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
        # print("JSON data : {}".format(dat))
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
            if state == value['state']:
                return keys , value["state"]
        return '-1' , []            

    def random_next(self , state):
        aval_block = []
        play_block = 0
        for pos in range(len(state)):
            if state[pos] == 0:
                aval_block.append(pos+1)
        print("get aval_block : {}".format(aval_block))
        play_block = random.choice(aval_block)
        print("get play_block : {}".format(play_block))
        return play_block 

    def score_calculate(self , currentStep = '-1' , playas = 0):
        listStep = []
        listScore = []
        dictScore = {}
        stepScore = 0
        # currentScore = 0
        # chooseScore = playas
        chooseScore = 0
        chooseStep = '0'
        if (currentStep == '-1') or (playas == 0):
            return '-1' , 0 , False
        stepIsEnd = self.state_action[currentStep]['end']   
        if stepIsEnd :
            currentScore = self.state_action[currentStep]['score']
        else :
            listStep = list(self.state_action[currentStep]['next'])
            # print("score_calculate currentStep : {} get listStep : {}".format(currentStep,listStep))
            for stp in listStep:
                # print("score_calculate currentStep : {} get stp : {}".format(currentStep, stp))
                byStep , stepScore , status = self.score_calculate(stp , playas*(-1))
                dictScore[byStep] = {
                                        'score' : stepScore,
                                        'status' : status
                                    }
                print("score_calculate get byStep : {}, stepScore : {:7.4f}, status : {}".format(currentStep , stepScore , status))
                self.listEdge.append(tuple([currentStep,byStep,abs(stepScore)]))
            # print("score_calculate playas : {} currentStep : {} get dictScore : {}".format(playas, currentStep,dictScore))
            for keys , value in dictScore.items():
                print("score_calculate get keys : {} get value : {} chooseScore : {}".format(keys , value, chooseScore))
                if chooseStep == '0':
                    chooseScore = value['score']
                    chooseStep = keys
                if abs(value['score']) > abs(chooseScore):
                    chooseScore = value['score']
                    chooseStep = keys                        
            # print("score_calculate playas : {} get chooseStep : {} get chooseScore : {}".format(playas, chooseStep , chooseScore)) 
            currentScore = chooseScore * self.discount
            # currentStep = chooseStep
            self.state_action[currentStep]['score'] = currentScore
            self.state_action[currentStep]['end'] = False
        print("score_calculate playas : {} get currentStep : {},\tcurrentScore : {:7.4f},\tstepIsEnd : {}".format(playas, currentStep , currentScore , stepIsEnd))    
        self.dictEdgeScore[currentStep] = currentScore
        return currentStep , currentScore , stepIsEnd 

    def find_Play(self , currentStep = None , playas = -1):
        tempMinScore = 1
        tempMinStep = '0'
        tempMaxScore = -1
        tempMaxStep = '0'
        tempScore = 0
        tempStep = '0'
        playInvert = False
        listStep = list(self.state_action[currentStep]['next'])
        # print("find_nextPlay currentStep : {} get listStep : {}".format(currentStep,listStep))
        for stp in listStep:
            print("score_calculate get stp : {} score : {}".format(stp, self.state_action[stp]['score']))
            if self.state_action[stp]['score'] < tempMinScore:
                tempMinScore = self.state_action[stp]['score']
                tempMinStep = stp
            if self.state_action[stp]['score'] > tempMaxScore:
                tempMaxScore = self.state_action[stp]['score']
                tempMaxStep = stp

        if playas > 0:
            # if (tempMinStep == '0') and (tempMaxStep != '0'):  
            if tempMaxScore > 0:  
                print("find_nextPlay tempMaxStep : {} get tempMaxScore : {}".format(tempMaxStep,tempMaxScore))
                tempStep = tempMaxStep
                tempScore = tempMaxScore
                playInvert = False
            else:
                print("No find_nextPlay tempMaxStep : {} get tempMaxScore : {}".format(tempMaxStep,tempMaxScore))
                tempStep, tempScore, playInvert = self.find_Play(tempMinStep,playas*(-1))
                playInvert = True
        if playas < 0:
            # if (tempMaxStep == '0') and (tempMinStep != '0'):
            if tempMinScore < 0:
                print("find_nextPlay tempMinStep : {} get tempMinScore : {}".format(tempMinStep,tempMinScore))
                tempStep = tempMinStep
                tempScore = tempMinScore
                playInvert = False
            else:
                print("No find_nextPlay tempMinStep : {} get tempMinScore : {}".format(tempMinStep,tempMinScore))
                tempStep, tempScore, playInvert = self.find_Play(tempMaxStep,playas*(-1))
                playInvert = True
        print("find_nextPlay currentStep : {} get PlayStep : {} , playInvert : {}".format(currentStep,tempStep,playInvert))   
        return tempStep , tempScore , playInvert     

    def find_bestPlay(self , state = None , playas = -1):
        aval_block = []
        left_block = []
        play_block = 0
        nextState = []
        self.listEdge = []
        self.dictEdgeScore = {}
        if state == None:
            return 0

        for pos in range(len(state)):
            if state[pos] == 0:
                aval_block.append(pos+1)
        print("find_bestPlay get aval_block : {}".format(aval_block)) 
        left_block = list(aval_block)
        operateState = self.stepList[-1]
        print("find_bestPlay playas : {} - get operateState : {}".format(playas,operateState)) 
        byStep , stepScore , status = self.score_calculate(operateState , playas)
        byStep , stepScore , playasStatus = self.find_Play(operateState , playas)
        print("find_bestPlay Step : {},\tScore : {:7.4f},\tplayasStatus : {}".format(byStep , stepScore , playasStatus))
        # print("find_bestPlay get self.listEdge : {}".format(self.listEdge)) 
        # print("find_bestPlay get self.dictEdgeScore : {}".format(self.dictEdgeScore))

        # to show State by relation
        self.generateGraph()

        nextState = list(self.state_action[byStep]['state'])
        if playasStatus :
            playas *= (-1)

        for pos in aval_block:
            # print("find_bestPlay get pos {} of nextState : {} playas : {}".format(pos , nextState[pos-1] , playas))
            if nextState[pos-1] == playas:
                play_block = pos
                print("find_bestPlay Predict play_block : {}".format(play_block))
                break

        if play_block == 0:
            for pos in aval_block:
                # print("find_bestPlay get pos {} of nextState : {} playas : {}".format(pos , nextState[pos-1] , playas))
                if nextState[pos-1] == playas*(-1):
                    play_block = pos
                    print("find_bestPlay Predict play_block : {}".format(play_block))
                    break

        if play_block == 0:
            play_block = random.choice(left_block)
            print("find_bestPlay random play_block : {}".format(play_block))
        return play_block 

    def update_state_action(self , state = None , goal = None):
        keys_state = '-1'
        score_state = 0
        status_state = False
        nxtList = []

        if (goal == None) or (goal == 0):
            score_state = 0
        else:
            score_state = goal
            status_state = True

        keys_state , value_state = self.find_state(state)
        if keys_state == '-1':
            thisState = str("{}".format(len(self.state_action)))
            thisStateDict = {
                'state' : list(state),
                'next' : [],
                'score' : score_state,
                'end' : status_state
            }
            self.state_action[thisState] = thisStateDict
            self.stepList.append(thisState)
            keys_state = thisState

        else:
            self.stepList.append(keys_state)
        
        if len(self.stepList) > 1:
            nxtList = list(self.state_action[self.stepList[-2]]['next'])
            if keys_state not in nxtList:
                nxtList.append(keys_state)
                self.state_action[self.stepList[-2]]['next'] = list(nxtList)
        
        # print("state_action : {}".format(self.state_action))
        print("stepList : {}".format(self.stepList))

    def stepListClear(self):
        self.stepList = []

    def generateGraph(self):
        # edges = [(1, 2), (1, 6), (2, 3), (2, 4), (2, 6),  
        #         (3, 4), (3, 5), (4, 8), (4, 9), (6, 7)] 
        dict_name = {}
        # self.generateEdge()
        G = nx.DiGraph() 

        # G.add_edges_from(self.listEdge) 
        G.add_weighted_edges_from(self.listEdge) 
        # We have to set the population attribute for each of the 14 nodes 
        for i in list(G.nodes()): 
            # print("i in G.nodes : {}".format(i))
            G.nodes[i]['Score'] = abs(self.dictEdgeScore[i]) 
            dict_name[i] = "{} : {:4.3f}".format(i,self.dictEdgeScore[i])
        # plt.figure(figsize =(9, 12))
        H = nx.relabel_nodes(G,dict_name)
        # original Graph created 
        # print("List of H nodes: {}".format(H.nodes())) 
        plt.subplot(111) 
        print("The original Graph:") 

        # node_color = [H.degree(v) for v in H] 
        node_color = [5*(nx.get_node_attributes(H, 'Score')[v])  for v in H] 
        # node colour is a list of degrees of nodes 
        
        node_size = [nx.get_node_attributes(H, 'Score')[v] for v in H] 
        # size of node is a list of population of cities 
        # print("List of all node_size: {}".format(node_size)) 
        
        edge_width = [1*H[u][v]['weight'] for u, v in H.edges()] 
        # width of edge is a list of weight of edges 
        # print("List of all edge_width: {}".format(edge_width)) 

        # nx.draw_networkx(H, node_size = node_size,  
        nx.draw_networkx(H, 
                        node_color = node_color, alpha = 0.5, 
                        # with_labels = True, width = edge_width, 
                        with_labels = True,
                        edge_color = edge_width, cmap = plt.cm.Blues) 
        
        plt.axis('off') 
        plt.tight_layout();

        # nx.draw_networkx(H, with_label = True) 
        
        print("Total number of nodes: ", int(H.number_of_nodes())) 
        print("Total number of edges: ", int(H.number_of_edges())) 
        print("List of all nodes: ", list(H.nodes())) 
        print("List of all edges: ", list(H.edges(data = True))) 
        print("Degree for all nodes: ", dict(H.degree())) 
        
        plt.show()

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
