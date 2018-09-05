# Find++

## Introduction 
* Sometimes, looking for keywords on a webpage just doesn't cut it. Therefore, at the hackathon held at the University at Buffalo during Nov 2017, we thought of developing something that can perform semantic search (based on query-passage similarity) on the paragraphs that exist on a particular webpage.
* Find++ is a Chrome Extension that was built for UBHacking 2017, University at Buffalo's annual hackathon. 
* It performs Natural Language Search on a webpage using word and document embeddings.

## Dependencies for app.py
* gensim: pip install -e git+https://github.com/jhlau/gensim.git#egg=gensim 
* flask 
* numpy 
* nltk 

## Running the code
* Load the extension folder into the Chrome browser while in Developer mode. 
* Go to a new webpage, click the extension and wait for 15 seconds. 
* Click the extension icon once again after that to search in Natural Language 
* Your result will be printed in the pop up window. 

## Issues
* Project development has been on a hiatus due to busy schedules. Hope to resume development soon. In the mean time, if this helps you in anyway, do freely clone it and use it freely. Do let me know if it was useful to you in anyway!

## References
Forked Gensim repository to obtain doc vectors from pretrained Glove word vectors: https://github.com/jhlau/gensim

