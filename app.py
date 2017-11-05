
# coding: utf-8

# In[1]:


from flask import Flask,jsonify,request
from numpy.linalg import norm
app = Flask(__name__)
	

##Form doc vectors from Glove word vectors.

import numpy as np
import gensim
from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import strip_punctuation,remove_stopwords
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib
import re
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def process_data(text_array):
    sents = text_array
    for i,sentence in enumerate(sents):
        sents[i] = strip_punctuation(sentence)
        #d = ' '.join(word_tokenize(text_array))
        sents[i] = remove_stopwords(sents[i])
        sents[i] = sents[i].lower()
    return sents

def load_word_vectors(fpath):
    f = open(fpath,'r')
    word_vectors = {} #dic with key as word and vector as value
    for line in f.readlines():
        word = line.split()[0]
        word_vectors[word] = np.array([float(s) for s in line.split()[1:]])
    f.close()
    return word_vectors
   


#Form the document vectors using existing word vectors
#inputs list of sentences, that are processed, and the word_vectors dictionary
def form_doc_vectors(sen_list, word_vectors):
    print("Creating doc vecs")
    #Split the sentence into words and concatenate their word_vectors vertically
    sen_vecs = []
    for sen in sen_list:
        words = sen.split()
        
        vec = np.array([word_vectors[w] for w in words if w in word_vectors.keys()])
        min_vec = np.min(vec,axis=0)
        max_vec = np.max(vec,axis=0)
        #Concatenate min and max horizontally
       
        doc_vec = np.hstack((min_vec,max_vec)).tolist()
        sen_vecs.append(doc_vec)
        
    return sen_vecs

def form_query_vec(query, word_vectors):
    words = query.split()
    try:
       vec = np.array([word_vectors[w] for w in words])
       min_vec = np.min(vec,axis=0)
       max_vec = np.max(vec,axis=0)
       query_vec = np.hstack((min_vec,max_vec)).tolist()
    except KeyError:
       query_vec = ''
    return query_vec


def find_dists(query_vec, sen_vecs):
    dists =  norm(sen_vecs-query_vec, axis=1, ord=1)
    #find min dists
    indices = range(0,len(dists))
    #Zip and sort by value
    zipped = zip(indices,dists)
    zipped.sort(key=lambda x: x[1])
    min_indices, min_dists = list(zip(*zipped))
    return min_indices, min_dists
text_array = ["hey what is your name","my name is nitin"]
word_vectors = load_word_vectors('./Glove/glove.6B.100d.txt')
global_sen_vecs = []

@app.route('/')
def index():
    return "Hello, World!"


from flask import abort

@app.route('/senvec/indexing/', methods=['POST'])
def indexing():
    print("creating word vectors")
    global global_sen_vecs
    
    if not request.json or not 'dump' in request.json:
        abort(400)
    dump = request.json['dump']
    text_array = re.sub(r'[^\x00-\x7F]+','', text_from_html(dump)).split(".")
    text_array = process_data(text_array[0:10])
    print("Text array created")
    global_sen_vecs = form_doc_vectors(text_array,word_vectors)
    print("Doc vectors created")
    return str({'sentence_vectors': global_sen_vecs, 'text_array': text_array})
@app.route('/senvec/searching/', methods=['POST'])
def searching():
    if not request.json or not 'query' in request.json:
        abort(400)
    query = request.json['query']
    sen_vecs = request.json['sen_vecs']
    print(query)
    query_vec = form_query_vec(query,word_vectors)
    #Find distances and return top IDs
    min_indices, min_dists = find_dists(np.array(query_vec),np.array(sen_vecs))
    return str({'top_ids': min_indices,'top_values':min_dists})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000,debug=True)





