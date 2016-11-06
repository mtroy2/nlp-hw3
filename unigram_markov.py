import os


class UnigramMarkov(object):

    def __init__(self):
        self.word_taggings = {}
        self.likely_tag = {}
        self.tag_words = {}
        self.tag_words['/N'] = {}
        self.tag_words['/F'] = {}
        self.tag_words['/E'] = {}
        self.tag_words['/D'] = {}
        self.tag_words['/A'] = {}
        self.tag_words['/R'] = {}

        test = open(os.getcwd() + '/hw3-data/test.txt')
        self.test_text = test.readlines()
        for line in self.test_text:
            line = line.rstrip()
        
    def read_train(self): 
        train = open(os.getcwd() + '/hw3-data/train.txt')
        train_text = train.read()
        train_text = train_text.split()
        # Read train file, split words and tags, enter info into word-tag dict
        for w_tag_pair in train_text:
            word = w_tag_pair[:-2]
            tag = w_tag_pair[-2:]
            if word in self.word_taggings.keys():
                if tag in self.word_taggings[word].keys():
                    self.word_taggings[word][tag] += 1
                else:
                    self.word_taggings[word][tag] = 1
            else:
                self.word_taggings[word] = {}
                self.likely_tag[word] = ''
                self.word_taggings[word][tag] = 1
        # determine most likely tagging for each word
        for word, tags in self.word_taggings.items():
            max_tag = ['',0]
            for tag, number in tags.items():        
                if int(number) >= max_tag[1]:
                    max_tag = [tag,number]
                    self.likely_tag[word] = tag

        # populate tag_words dic : { tag : {word: count} }
        
        for word,tags in self.word_taggings.items():
            for tag,number in tags.items():
                if word in self.tag_words[tag].keys():
                    self.tag_words[tag][word] += 1
                else:
                    self.tag_words[tag][word] = 1
    def you_prob(self):
        prob_sum = 0.
        you_tot = sum(self.word_taggings['you'].values())
        for tag,count in self.word_taggings['you'].items():
            you_prob = count/you_tot
            print(' P( ' + tag + ' | you ) = ' + str(you_prob) )
            prob_sum += you_prob
        print('Sum of probability P(tag|you) = ' + str(prob_sum)) 
    def test_set(self):


        self.test(self.test_text, 'test set')

    def test(self,test_text, name,p = 'f'):

        # Read test file, guess most likely tag
        correct = 0
        total = 0
        guess_str = ""
       
        for line in test_text:
            for w_tag_pair in line.split():
                
                word = w_tag_pair[:-2]
            
                if word in self.likely_tag.keys():
                    tag_guess = self.likely_tag[word]
                else:
                    tag_guess = '/N'
                guess_str += word + tag_guess + ' '
                correct_tag = w_tag_pair[-2:]
                if tag_guess == correct_tag:
                    correct += 1
                total += 1
        accuracy = correct/total
        if p == 'true':
            print ("\nSecond line ---------------------------------------")
            print("Guessed tags: " + guess_str)
            print("Correct tags: " + line)
        print ('total accuracy on ' + name + ' = ' + str(accuracy) ) 
    def second_line(self):
        
        second_line = self.test_text[1]
        second_line = [second_line]
        #second_line = second_line.split()
        self.test(second_line, 'second line', 'true' )
if __name__ == '__main__':
    model = UnigramMarkov()
    model.read_train()
    model.you_prob()


    model.test_set()
    
    model.second_line()

