import os
import nltk as nltk
from tabulate import tabulate
import numpy as np
from HMM_Map import *
from pandas import DataFrame
import collections
class UnigramMarkov(object):

    def __init__(self):
        self.word_taggings = {}
        self.tag_words = {}
        self.row_lookup = {}
        self.column_lookup = {}
        self.tags = ['/N','/F','/E','/D','/A','/R',]

        self.tag_matrix = []
        self.states = []
        for i,tag in enumerate(self.tags):
            self.row_lookup[tag] = i
            self.column_lookup[tag] = i+1
            self.tag_words[tag] = {}
        self.tag_words['/T'] = {}
        self.tag_words['/S'] = {}
        self.row_lookup['/T'] = 6
        self.column_lookup['/S'] = 0
        
        for i in range(0, 7):
            self.tag_matrix.append( [0]*7)
        test = open(os.getcwd() + '/hw3-data/test.txt')
        self.test_text = test.readlines()
        for line in self.test_text:
            line = line.rstrip()
        train = open(os.getcwd() + '/hw3-data/train2.txt')
        self.train_text = train.readlines()
        for line in self.train_text:
            line = line.rstrip()

    def read_train(self): 

        
 
        # Read train file, split words and tags, enter info into word-tag dict
        for line in self.train_text:
            tag_l = []
            line=line.rstrip()
            line = '<s>/S ' + line + ' </s>/T' 
            for w_tag_pair in line.split():
                
                word = w_tag_pair[:-2]
                tag = w_tag_pair[-2:]
                tag_l.append(tag)
                if word in self.word_taggings.keys():
                    if tag in self.word_taggings[word].keys():
                        self.word_taggings[word][tag] += 1.
                    else:
                        self.word_taggings[word][tag] = 1.
                else:
                    self.word_taggings[word] = {}                    
                    self.word_taggings[word][tag] = 1.
            tag_grams = nltk.ngrams(tag_l, 2)
            for gram in tag_grams:
                self.tag_matrix[self.row_lookup[gram[1]]][self.column_lookup[gram[0]]] += 1.

        # Smoothing, change all 1 ct words to <unk>
        remove_list = []
        for word, tags in self.word_taggings.items():  
            if sum(tags.values()) == 1:
                remove_list.append(word)
        self.word_taggings['<unk>'] = {}
        for w in remove_list:
            # copy tag values into unk entry
            for tag,val in self.word_taggings[w].items():
                if tag in self.word_taggings['<unk>'].keys():
                    self.word_taggings['<unk>'][tag] += val
                else:
                    self.word_taggings['<unk>'][tag] = val
            del(self.word_taggings[w])           
    
        # populate tag_words dic : { tag : {word: count} }
        
        for word,tags in self.word_taggings.items():
            for tag,number in tags.items():
                if word in self.tag_words[tag].keys():
                    self.tag_words[tag][word] += 1.
                else:
                    self.tag_words[tag][word] = 1.
        # turn tag_words into probabilities
        for tag, word_dict in self.tag_words.items():
            self.tag_words[tag] = collections.OrderedDict(sorted(word_dict.items()))
        self.tag_words = collections.OrderedDict(sorted(self.tag_words.items()))
        for tag, wcs in self.tag_words.items():
            for word,count in wcs.items():
                #print(tag + " " + word + " " + str(count) + " " + str(sum(wcs.values())))
                self.tag_words[tag][word] = count / sum(wcs.values())
        self.tag_matrix = np.array(self.tag_matrix)
        col_sum = self.tag_matrix.sum(axis=0)
        for i,row in enumerate(self.tag_matrix):
            for j,entry in enumerate(row):
                self.tag_matrix[i][j] = entry / col_sum[j]

        print (DataFrame(self.tag_matrix, columns=['/S','N', 'F', 'E', 'D', 'A', 'R',], index=['N', 'F', 'E', 'D', 'A', 'R', '/T']))
   
    def you_prob(self):
        
        you_tot = sum(self.word_taggings['you'].values())
        for tag,wcs in self.tag_words.items():
            if 'you' in wcs.keys():
                print('P( you | ' + tag + ') = ' + str(wcs['you']) )
            else:
                print('P( you | ' + tag + ') = 0')
           
    def test_set(self):


        self.test(self.test_text, 'test set')

    def test(self,test_text, name,p = 'f'):

        # Read test file, guess most likely tag
        correct = 0
        total = 0
        guess_str = ""

        for line in test_text:
            self.states.clear()
            line=line.rstrip()
            sentence = []
            t_list = []
            line = '<s>/S ' + line + ' </s>/T' 
            for w_tag_pair in line.split():
                word = w_tag_pair[:-2]
                tag = w_tag_pair[-2:]
                sentence.append(word)
                t_list.append(tag)

                # create state
                if word in self.word_taggings.keys():
                    new_state = State(word)
                    # Create substates
                    for tag,prob in self.word_taggings[word].items():
                        weight = self.tag_words[tag][word]
                        new_state.add_substate(tag, weight)
                        
                    self.states.append(new_state)
                else:
                    new_state = State('<unk>')
                    for tag,prob in self.word_taggings['<unk>'].items():
                        weight = self.tag_words[tag]['<unk>']
                        new_state.add_substate(tag,weight)
                   
                    self.states.append(new_state)
            self.create_edges()
            # begin viterbi algorithm
            self.states[0].substates[0].viterbi = 0        
                        
            for i,state in enumerate(self.states[1:]):
                # starting from 1st index, but enumerate default value is 0th index
            
                for substate in state.substates:      
                 
                    for edge in substate.edges:
   
                        if edge.start_node.viterbi + edge.weight > substate.viterbi:
                            substate.viterbi = edge.start_node.viterbi + edge.weight
                            substate.back_point = edge.start_node
            #for state in self.states:
             #   print("State: " + state.word)   
              #  for sub in state.substates:
               #     print("\tTag: " + sub.tag + " Viterbi: " + str(sub.viterbi ))


            best_tags = []
            cur_state = self.states[-1].substates[0]
            while cur_state.back_point != None:
                best_tags.append(cur_state.tag)
                cur_state = cur_state.back_point
            
            best_tags.append('/S')
            best_tags.reverse()

            print(best_tags)
            print(t_list)

            for i,t in enumerate(best_tags):     
                correct_tag = t_list[i]
                if t == correct_tag:
                    correct+= 1
                total += 1
        accuracy = correct / total
        print ('total accuracy on ' + name + ' = ' + str(accuracy) ) 
    def second_line(self):
        
        second_line = self.test_text[1]
        second_line = [second_line]
        #second_line = second_line.split()
        self.test(second_line, 'second line', 'true' )

    def create_edges(self):
        # Next state owns incoming transitions
        # form edges from last state to first
        self.states.reverse()
        for i,state in enumerate(self.states):
            if state.word != '<s>':
                for cur_substate in state.substates:
                    # all substates of next state
                    for prev_sub in self.states[i+1].substates:
                        end_tag = cur_substate.tag
                        start_tag = prev_sub.tag
                        word_weight = np.log(cur_substate.word_weight)
                        tag_weight = np.log(self.tag_matrix[self.row_lookup[end_tag]][self.column_lookup[start_tag]])
                        cur_substate.add_edge(prev_sub, word_weight + tag_weight)
        self.states.reverse()
if __name__ == '__main__':
    model = UnigramMarkov()
    model.read_train()
    #model.you_prob()


    model.test_set()
    
    model.second_line()

