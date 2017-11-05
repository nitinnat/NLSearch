
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
    #dists =  norm(sen_vecs-query_vec, axis=1, ord=1)
    dists = np.dot(query_vec, sen_vecs.T)
    print(dists)
    #find min dists
    indices = range(0,len(dists))
    #Zip and sort by value
    zipped = zip(indices,dists)
    zipped.sort(key=lambda x: x[1])
    min_indices, min_dists = list(zip(*zipped))
    return min_indices, min_dists

def docvecs(dump):
    original_text = dump.split('\n')
    text = re.sub(r'[^\x00-\x7F]+','', dump)
    text_array2 = text.split('\n')
    text_inds = [i for i in range(len(text_array2)) if text_array2[i] != '' and len(text_array2[i].split()) > 5]
    text_array = [text_array2[i] for i in text_inds]
    original_text = [original_text[i] for i in text_inds]
    text_array = process_data(text_array)
    
    f = open("temp.txt",'a')
    for line in text_array:
        f.write(line)
    f.close()
    #doc2vec parameters
    vector_size = 100
    window_size = 15
    min_count = 1
    sampling_threshold = 1e-5
    negative_size = 5
    train_epoch = 100
    dm = 0 #0 = dbow; 1 = dmpv
    worker_count = 1 #number of parallel processes
    #pretrained word embeddings
    pretrained_emb = "./Glove/glove.6B.100d.txt" #None if use without pretrained embeddings
    #input corpus
    train_corpus = "temp.txt"
    #output model
    saved_path = "model.bin"
    #enable logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    #train doc2vec model
    docs = g.doc2vec.TaggedLineDocument(train_corpus)
    model = g.Doc2Vec(docs, size=vector_size, window=window_size, min_count=min_count, sample=sampling_threshold, workers=worker_count, hs=0, dm=dm, negative=negative_size, dbow_words=1, dm_concat=1, pretrained_emb=pretrained_emb, iter=train_epoch)
    #save model
    model.save(saved_path)
    #Convert each sentence into a vector
    vec = []
    print(len(text_array))
    for line in text_array:
        vec.append(model.infer_vector(line).tolist())
    
    return model,text_array,vec,original_text


word_vectors = load_word_vectors('./Glove/glove.6B.100d.txt')
global_sen_vecs = []

@app.route('/')
def index():
    return "Hello, World!"

model = None
from flask import abort
import gensim.models as g
import logging
model = None
global_sen_vecs = None
@app.route('/senvec/indexing/', methods=['POST'])
def indexing():
    global model
    global global_sen_vecs
    model = None
    global_sen_vecs = None
    print("creating word vectors")
    if not request.json or not 'dump' in request.json:
        abort(400)
    dump = request.json['dump']
    model,text_array,global_sen_vecs,original_text = docvecs(dump)
    print("Text array created")
    #return jsonify({'sentence_vectors': global_sen_vecs, 'text_array': text_array})

@app.route('/senvec/searching/', methods=['POST'])
def searching():
    if not request.json or not 'query' in request.json:
        abort(400)
    query = request.json['query']
    sen_vecs = request.json['sentence_vectors']
    model = request.json['model']
    print(query)
    query_vec = model.infer_vector(query)
    #query_vec = form_query_vec(query,word_vectors)
    #Find distances and return top IDs
    min_indices, min_dists = find_dists(np.array(query_vec),np.array(sen_vecs))
    return jsonify({'top_ids': min_indices,'top_values':min_dists})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000,debug=True)





