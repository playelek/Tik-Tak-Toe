import time
import sys
import random
from os import system, name 

import numpy as np
from math import inf as infinity
from markovDT import markov
from NeuralNetworkDT import NeuralNetwork

game_state =    [   0,0,0,
                    0,0,0,
                    0,0,0 ]
players = ['X','O']

dict_state = {  0:' ',
                1:'X',
                -1:'O'}  
dict_player = {
                    'X' : 1,
                    'O' : -1
            }
mk = markov()
nn = NeuralNetwork()

def play_move(state, player, block_num):
    if state[int(block_num-1)] == 0:
        state[int(block_num-1)] = dict_player[player]
    
def check_current_state(game_state):
    draw_flag = 0
    for i in range(9):
        if game_state[i] == 0:
            draw_flag = 1
    
    if (abs(game_state[0] + game_state[1] + game_state[2]) == 3):
        return game_state[0], "Done"
    if (abs(game_state[3] + game_state[4] + game_state[5]) == 3):
        return game_state[3], "Done"
    if (abs(game_state[6] + game_state[7] + game_state[8]) == 3):
        return game_state[6], "Done"

    if (abs(game_state[0] + game_state[3] + game_state[6]) == 3):
        return game_state[0], "Done"
    if (abs(game_state[1] + game_state[4] + game_state[7]) == 3):
        return game_state[1], "Done"
    if (abs(game_state[2] + game_state[5] + game_state[8]) == 3):
        return game_state[2], "Done"
    
    if (abs(game_state[0] + game_state[4] + game_state[8]) == 3):
        return game_state[4], "Done"
    if (abs(game_state[2] + game_state[4] + game_state[6]) == 3):
        return game_state[4], "Done"
    
    if draw_flag is 0:
        return 0, "Done"
        
    return None, "Not Done"

def print_board(game_state):
    show_state =    [   ' ',' ',' ',
                        ' ',' ',' ',
                        ' ',' ',' ' ]
    for pos in range(len(game_state)):
        show_state[pos] = dict_state[game_state[pos]]

    print('----------------')
    print('| {} || {} || {} |'.format(show_state[0],show_state[1],show_state[2]))
    print('----------------')
    print('| {} || {} || {} |'.format(show_state[3],show_state[4],show_state[5]))
    print('----------------')
    print('| {} || {} || {} |'.format(show_state[6],show_state[7],show_state[8]))
    print('----------------')
    

def random_turn(state , playas = 0):
    play_block = mk.random_next(state)
    return play_block

def Human_turn(state, playas = 0):
    cont = True
    aval_block = []
    play_block = 0
    for pos in range(len(state)):
        if state[pos] == 0:
            aval_block.append(pos+1)
    print("get aval_block : {}".format(aval_block))
    while cont:
        blockInput = input("Human !!!! , your turn! Choose where to place {} to {}: ".format(dict_state[playas],aval_block))
        if blockInput.isdigit(): 
            block_choice = int(blockInput)
            if block_choice not in aval_block:
                print("Please insert only {}".format(aval_block))
            else:
                play_block = block_choice
                cont = False
    return play_block

def markov_turn(state, playas = 0):
    play_block = mk.find_bestPlay(state, playas)
    return play_block

def neuralnetwork_turn(state, playas = 0):
    play_block = nn.find_bestPlay(state, playas)
    return play_block

# define our clear function 
def scnclear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

# main.py
print(__name__)

def main():
    # PLaying
    argumentList = sys.argv[1:]
    print ("argumentList : {}".format(argumentList))
    if "-g" in argumentList:
        print ('run with show update graph')
        mk.updateGraph = True
    if "-d" in argumentList:
        print ('run with show update graph')
        mk.updateGraph = True

    play_again = 'Y'
    player_choice = 'Y'
    current_player = 1
    goal = 0
    playCount = 0
    winbyX = 0
    winbyO = 0
    Draw = 0
    winRateX = 0.5
    winRateO = 0.5
    drawRate = 0.0
    play_mode = '0'
    pMode = ['1','2', '3']
    markovWin = 0
    nnWin = 0
    mk.load_state_action()
    nn.load_state_action()
    scnclear()
    mk.playFirst = True
    nn.playFirst = False 
    while play_mode not in pMode:
        print('''Choose Play Mode :
                Markov has {} states
                NeuralNetwork has {} states
                [1] : You VS Markov
                [2] : You VS NeuralNetwork
                [3] Markov VS NeuralNetwork'''.format(len(mk.state_action), len(nn.state_action)))
        play_mode = input("Please Choose [1-3]")
        print("PlayMode : {}".format(play_mode))

    while play_again == 'Y' or play_again == 'y':
        game_state =    [   0,0,0,
                            0,0,0,
                            0,0,0 ]
        current_state = "Not Done"
        playCount += 1
        scnclear()
        print("New Game! {}".format(playCount))      
        print_board(game_state)
        if play_mode == '1' or play_mode == '2':
            player_choice = input("X is play first , Do you wanna play first [Y/N] : ") 
            if player_choice == 'Y' or player_choice == 'y':
                # player_choice = 'X'
                mk.playFirst = False
                nn.playFirst = False
            # elif play_mode == '3':
            #     mk.playFirst = False
            #     nn.playFirst = True 
            else:
                # player_choice = 'O'
                mk.playFirst = True
                nn.playFirst = True
        else:
            # mk.playFirst = False
            # nn.playFirst = True 
            print("playCount : Winby X : Winby O : Draw --- {} : {:05.3f} : {:05.3f} : {:05.3f}".format(playCount,winRateX,winRateO,drawRate))
            print("Markov State has : {}".format(len(mk.state_action)))
            print("Markov Stat has {}".format(mk.resultStat)) 
            print("Markov Win {}".format(markovWin)) 
            print("NeuralNetwork State has : {}".format(len(nn.state_action)))
            print("NeuralNetwork Stat has {}".format(nn.resultStat))  
            print("NeuralNetwork Win {}".format(nnWin))    
            player_choice = 'N'           
        winner = None
        

        current_player = 1    
        mk.stepListClear()
        mk.update_state_action(game_state,0) 
        while current_state == "Not Done":
            print("current game_state : {}".format(game_state))
            if current_player == 1: # play X
                if play_mode == '1':
                    if mk.playFirst: 
                        block_choice = markov_turn(state = game_state, playas = current_player)
                    else:
                        block_choice = Human_turn(state = game_state, playas = current_player)
                elif play_mode == '2':
                    if nn.playFirst: 
                        block_choice = neuralnetwork_turn(state = game_state, playas = current_player)
                    else:
                        block_choice = Human_turn(state = game_state, playas = current_player)
                    # block_choice = markov_turn(state = game_state, playas = current_player)
                else:
                    if mk.playFirst: 
                        block_choice = markov_turn(state = game_state, playas = current_player)
                    else:
                        block_choice = neuralnetwork_turn(state = game_state, playas = current_player)
                    # block_choice = markov_turn(state = game_state, playas = current_player)
            else:   # play O
                if play_mode == '1':
                    if not mk.playFirst: 
                        block_choice = markov_turn(state = game_state, playas = current_player)
                    else:
                        block_choice = Human_turn(state = game_state, playas = current_player)
                elif play_mode == '2':
                    if not nn.playFirst: 
                        block_choice = neuralnetwork_turn(state = game_state, playas = current_player)
                    else:
                        block_choice = Human_turn(state = game_state, playas = current_player)
                    # block_choice = markov_turn(state = game_state, playas = current_player)
                else:
                    if not mk.playFirst: 
                        block_choice = markov_turn(state = game_state, playas = current_player)
                    else:
                        block_choice = neuralnetwork_turn(state = game_state, playas = current_player)
                    # block_choice = markov_turn(state = game_state, playas = current_player)
            play_move(game_state ,dict_state[current_player], block_choice)
            time.sleep(3)
            # scnclear()
            print("Game! {}".format(playCount)) 
            # print("current game_state : {}".format(game_state))
            print_board(game_state)
            winner, current_state = check_current_state(game_state)
            if winner is not None:
                if winner == 1:
                    if mk.playFirst == True:
                        markovWin += 1
                    if nn.playFirst == True:
                        nnWin += 1
                    winbyX +=1
                    print("Game! {} - {} won!".format(playCount, dict_state[winner]))
                elif winner == -1:
                    if mk.playFirst == False:
                        markovWin += 1
                    if nn.playFirst == False:
                        nnWin += 1
                    winbyO +=1
                    print("Game! {} - {} won!".format(playCount, dict_state[winner]))
                else:
                    Draw +=1
                    print("Game! {} - Draw!".format(playCount))

                winRateX = float(winbyX/playCount)
                winRateO = float(winbyO/playCount)
                drawRate = float(Draw/playCount)
                mk.updateResult(winner)
                nn.updateResult(winner)
                print("playCount : Winby X : Winby O : Draw --- {} : {:05.3f} : {:05.3f} : {:05.3f}".format(playCount,winRateX,winRateO,drawRate))
                print("Markov State has : {}".format(len(mk.state_action)))
                print("Markov Stat has {}".format(mk.resultStat)) 
                print("Markov Win {}".format(markovWin)) 
                print("NeuralNetwork State has : {}".format(len(nn.state_action)))
                print("NeuralNetwork Stat has {}".format(nn.resultStat))  
                print("NeuralNetwork Win {}".format(nnWin))   
                mk.update_state_action(game_state,winner) 
                mk.save_state_action()
                # nn.update_state_action(game_state,winner) 
                nn.save_state_action(state = game_state, goal = winner)
                time.sleep(3)
            else:
                current_player *= -1
                mk.update_state_action(game_state,0) 

            time.sleep(1)
        if play_mode == '1' or play_mode == '2':
            play_again = input('Lets Play Again?(Y/N) : ')
        elif play_mode == '2':
            nn.load_state_action()
            play_again = input('Lets Play Again?(Y/N) : ')
        else:
            nn.load_state_action()
            play_again = 'Y'
            if mk.playFirst == True:
                mk.playFirst = False
                nn.playFirst = True
            else:
                mk.playFirst = True
                nn.playFirst = False                

        if play_again == 'N' or play_again == 'n':
            print('GoodBye!')
            # mk.generateGraph()
if __name__ == "__main__":
    main()