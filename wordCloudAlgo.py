#import matplotlib as mpl
#from operator import itemgetter
#import matplotlib.pyplot as plt
import re
from subprocess import check_output
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder, TrigramAssocMeasures, TrigramCollocationFinder 
#import numpy as np
import pickle
from PIL import Image

def prepareStopWords():
    stopwordsList = []
    # Load default stop words and add a few more specific to my text.
    stopwordsList = stopwords.words('english')
    return stopwordsList

#WNL = nltk.WordNetLemmatizer()

# preprocess the text before word cloud genetation
def preprocess_text(rawText, bad_words_list = [], replace_words_dict = {}):
    rawText = rawText.lower() 
    rawText = rawText.replace("'", "")
    rawText = rawText.replace("/", "")
    rawText = rawText.replace("_", "")
    for key,value in replace_words_dict.items():
        rawText = rawText.replace(key, value)
    #tokens = nltk.word_tokenize(rawText)
    #text = nltk.Text(tokens)
    text = rawText.split(" ")
    #print("after tokens", text)
    # Load default stop words and add a few more.
    stopWords = prepareStopWords()
    for word in bad_words_list:
        stopWords.append(word) 
    # Remove extra chars and remove stop words.
    text_content = [''.join(re.split("[ .,;:!?‘’``''@#$%^_*()<>{}~\n\t\\\+]", word)) for word in text]
    #text_content = [word for word in text]
    text_content = [word for word in text_content if not word in stopWords]
    # Remove any entries where the len is zero.
    text_content = [s for s in text_content if len(s) != 0]
    #text_content = [WNL.lemmatize(t) for t in text_content]
       
    return text_content

# create word cloud using bigrams
# word_dict is the dictionary we'll use for the word cloud.
def create_wordCloud_dict_unigrams(text_content, bad_unigrams = []):
    word_dict = {}
    for word in text_content:
    	if word in word_dict:
    		word_dict[word] = word_dict[word] + 1
    	else:
    		word_dict[word] = 1
    return word_dict

def create_wordCloud_dict_bigrams(text_content, bad_bigrams = []):
    finder = BigramCollocationFinder.from_words(text_content)
    bigram_measures = BigramAssocMeasures()
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    # Sort highest to lowest based on the score.
    #scoredList = sorted(scored, key=itemgetter(1), reverse=True)
    scoredList = scored
    word_dict = {}
    listLen = len(scoredList)
    # Set the key to the scored value. 
    for i in range(listLen):
        word_dict[' '.join(scoredList[i][0])] = scoredList[i][1]
    for bad_bigram in bad_bigrams:
        if bad_bigram in word_dict:
            del word_dict[bad_bigram]
    return word_dict

# create word cloud using trigrams
def create_wordCloud_dict_trigrams(text_content, bad_trigrams):
    finder = TrigramCollocationFinder.from_words(text_content)
    trigram_measures = TrigramAssocMeasures()
    scored = finder.score_ngrams(trigram_measures.raw_freq)
    # Sort highest to lowest based on the score.
    #scoredList = sorted(scored, key=itemgetter(1), reverse=True)
    scoredList = scored
    word_dict = {}
    listLen = len(scoredList)
    # Set the key to the scored value. 
    for i in range(listLen):
        word_dict[' '.join(scoredList[i][0])] = scoredList[i][1]
    for bad_bigram in bad_trigrams:
        if bad_trigram in word_dict:
            del word_dict[bad_trigram]
    return word_dict        

# Set word cloud params and instantiate the word cloud.
# The height and width only affect the output image file.
WC_height = 500
WC_width = 1000
WC_max_words = 40

def transform_format(val):
    if val > 0:
        return 255
    else:
        return 0

def generateMask():
	with open("mask.pkl", 'rb') as file:
		mask = pickle.load(file)
	return mask


def create_word_cloud(word_dict, mpltr, fig_name, mask = None): 
    wordCloud = WordCloud(background_color='white',max_words=WC_max_words, height=WC_height, width=WC_width, mask = mask)
    wordCloud.generate_from_frequencies(word_dict)
    #mpltr.ax.rcParams['figure.figsize'] = [14, 7]
    #plt.title('Most frequently occurring bigrams connected with an underscore_')
    mpltr.ax.imshow(wordCloud, interpolation='bilinear')
    mpltr.ax.axis("off")
    mpltr.draw()
    return WordCloud
    #wordCloud.to_file(fig_name+".png")

def final_funcs(self,raw_text, mpltr, save_file_name= "",replace_words_dict = {}, bad_words_list = [], bad_grams = []):
    text_content = preprocess_text(raw_text, bad_words_list, replace_words_dict)
    if self.unigramRB.isChecked():
    	word_dict = create_wordCloud_dict_unigrams(text_content, bad_grams)
    elif self.bigramRB.isChecked():
    	word_dict = create_wordCloud_dict_bigrams(text_content, bad_grams)
    elif self.trigramRB.isChecked():
    	word_dict = create_wordCloud_dict_trigrams(text_content, bad_grams)
    if self.circularRB.isChecked():
    	mask = generateMask()
    else:
    	mask = None
    WordCloudObj =  create_word_cloud(word_dict, mpltr, save_file_name, mask = mask)
    return WordCloudObj