# [Source 1](https://github.com/ds-modules/Library-HTRC/blob/master/01-setup/01-HTRC-Extracted%20Features.ipynb)<br>
# [Source 2](https://programminghistorian.org/en/lessons/text-mining-with-extracted-features)

# Text Preparation
## Initial Set-up
### Import statements
from htrc_features import FeatureReader
import os, sys, io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from spacy.lang.en import English
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize
from pathlib import Path
import string
import re
from hunspell import Hunspell

### Further Set-up
nltk.download('stopwords')
nltk.download("wordnet")
parser = English()
en_stop = set(nltk.corpus.stopwords.words("english"))
### Deals with HTRC or .txt file formats and their location
is_HTRC = str(sys.argv[1])
is_HTRC = is_HTRC.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
has_custom_stop = str(sys.argv[2])
has_custom_stop = has_custom_stop.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
custom_stop = []
if has_custom_stop:
    f = open("custom_stop.txt", "r")
    custom_stop_str = f.read()
    custom_stop = custom_stop_str.split()
en_stop = set(nltk.corpus.stopwords.words("english") + custom_stop)

file_locs = sys.argv[3]
num_compare = int(sys.argv[4])
n_t_array = []
for n_t in sys.argv[5:]:
    n_t_array.append(int(n_t))
### Set working directory to above
os.chdir(file_locs)

## Functions needed by both HTRC and .txt options
### Function that tokenizes texts
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
            lda_tokens.append(token.lower_)
    return lda_tokens
### Function that prepares text for topic modeling
def prepare_text_for_modelling(vol, is_HTRC):
    h = Hunspell()
    if is_HTRC:
        pre_tokenized = vol.tokens(case=False)
    else:
        pre_tokenized = vol
    raw_txt = ""
    tokens = list(pre_tokenized)
    #### In order to speed up processing, takes a random sample of 500 words from each volume
    rand_arr = np.random.random_sample((500,))*len(tokens)
    cleaned_tok = []
    for rand_n in rand_arr:
        cleaned_tok.append(tokens[int(rand_n)])
    tokens = cleaned_tok
    #### Filters tokens that are too small
    tokens = [token for token in tokens if len(token) > 4]
    #### Removes annoying characters from tokens
    tokens = [re.sub("ſ","s",token) for token in tokens]
    tokens = [re.sub('[\W_]+', "",token) for token in tokens]
    tokens = [token.encode('latin-1', 'ignore') for token in tokens]
    tokens = [token.decode('latin-1') for token in tokens]
    tokens = [re.sub(" ","", token) for token in tokens]
    #### Filters stop words
    tokens = [token for token in tokens if token not in en_stop]
    #### Ensures tokens are english words, removes empty tokens
    for i in range(len(tokens)):
        token = tokens[i]
        ##### Runs only if token is not empty
        if token and not token.isspace():
            len_tok = len(token)
            is_word = h.spell(token)
            sug = h.suggest(token)
            ###### Gets root of valid token
            if is_word:
                if len(h.stem(token)) > 0:
                    token = h.stem(token)[-1]
            ###### Gets suggestions for invalid token, finds root word based on most likely suggestion
            elif len(sug) > 0:
                tok_stem = h.stem(sug[0])
                if len(tok_stem) > 0:
                    token = h.stem(sug[0])[-1]
                else:
                    token = ""
            else:
                token = ""
        else:
            token = ""
        tokens[i] = token
    tokens = [token for token in tokens if token != ""]
    tokens = set(tokens)
    return tokens
### Function that takes a txt file name and returns a tokenized version of it
def txt_reader_to_tokens(txt_file_name):
    with open(txt_file_name, "rb") as f:
        raw_txt = f.read()
    raw_txt = str(raw_txt)
    cleaned_txt = re.sub('[^A-Za-z0-9]+', ' ', raw_txt)
    return prepare_text_for_modelling(tokenize(cleaned_txt), False)
### Function that takes a file suffix and returns all file paths associated with it in specific folder
def file_paths_grabber(suffix):
    file_paths = []
    for root, dirs, files in os.walk(file_locs):
        for file in files:
            if file.endswith(suffix):
                file_paths.append(os.path.join(root, file))
    return file_paths

count = 0
## Prepares HTRC corpus for comparison
text_data = pd.DataFrame(columns = ["title",
                                    "tokens",
                                    "url"])
if is_HTRC:
    ### Downloads the required files via a script created by HTRC ***INTO THE DIRECTORY IN WHICH YOU HAVE SAVED THE .SH FILE***
    # get_ipython().system('bash script.sh')
    ### List populated by all files just downloaded
    text_trap = io.StringIO()
    sys.stdout = text_trap
    file_paths = file_paths_grabber("json.bz2")
    num_vols = len(file_paths)
    ### Prepping HTRC Texts for LDA
    fr = FeatureReader(file_paths)
    sys.stdout = sys.__stdout__
    for vol in fr:
        tokens = prepare_text_for_modelling(vol, True)
        text_data = text_data.append({
            "title": vol.title,
            "tokens": tokens,
            "url": vol.handle_url
        }, ignore_index = True)
        count+=1
        print("Loading HTRC files: " + str(round((count/num_vols)*100,1)) + "%", end = "\r")

## Prepares .txt corpus for comparison
else:
    ### List populated by all txt files
    file_paths = file_paths_grabber("txt")
    num_vols = len(file_paths)
    text_data = pd.DataFrame(columns = ["title",
                                       "tokens"])
    ### Prepping texts for LDA
    for file_ in file_paths:
        tokens = txt_reader_to_tokens(file_)
        to_title = str(file_)
        to_title 
        text_data = text_data.append({
            "title": to_title.Title(),
            "tokens": tokens,
            "url": ""
        }, ignore_index = True)
        count+=1
        print("Loading .txt files: " + str(round((count/num_vols)*100,1)) + "%", end = "\r")

## Imports text for analysis
txt_for_analysis = txt_reader_to_tokens("file_for_analysis.txt")

# LDA with GenSim/Similarity
## Set-up
### Import statements
import gensim
from gensim import corpora
import pickle
### Further set-up
dictionary = corpora.Dictionary(text_data["tokens"])
corpus = [dictionary.doc2bow(text) for text in text_data["tokens"]]

## Document Similarity comparison
### Analysed doc to bag of words
query_doc_tf_bow = dictionary.doc2bow(txt_for_analysis)
### Building tfidf model and index of similarity
tf_idf = gensim.models.TfidfModel(corpus)
sims = gensim.similarities.Similarity("",tf_idf[corpus],
                                      num_features=len(dictionary))
### Similarity query against the corpus
query_doc_tf_idf = tf_idf[query_doc_tf_bow]
comp_res = sims[query_doc_tf_idf]

## Display results
### Creates HTML table with most similar documents and links
print("Building document similarity matrix...")
top_n_most_sim_index = comp_res.argsort()[-num_compare:][::-1]
sim_doc_df = text_data.iloc[top_n_most_sim_index]

pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')

## Modeling
### DataFrame to be populated by models
models = {}
## Populates array with models corresponding to below topics
print("Building topic models...")
for num_topics in n_t_array:
    print("Building topic model with " + str(num_topics) + " topics...")
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = num_topics, id2word = dictionary, passes = 15)
    ldamodel.save('model.gensim')
    topics = ldamodel.print_topics(num_words = 5)
    models[num_topics] = ldamodel

# Visualization with pyLDAvis
## Set-up
### Import statements
import pyLDAvis.gensim

### Further set-up
dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
corpus = pickle.load(open('corpus.pkl', 'rb'))## Display
### Creates dicts to be used later to display words, similarity metric, and lda html for each topic
sim_disp_dict = {}
word_disp_dict = {}
lda_vis_html = {}
print("Processing report...")
for num_topics in n_t_array:
    print("Building report for topic model with " + str(num_topics) + " topics...")
    ### Creates the two lists that comprise the dicts (one for each topic)
    sim_list = []
    word_list = []
    ### Gets list of topic similarity
    doc_comp_list = models[num_topics].get_document_topics(query_doc_tf_bow)
    ### Gets words which comprise topic
    topics_word_list = models[num_topics].print_topics(num_words = 5)
    for topics_word in topics_word_list:
        ### Sets sim at 0 in case topic has no overlap with doc
        sim = 0
        ### Finds index value for specific topic
        topic_ind = topics_word[0]
        for doc_comp in doc_comp_list:
            ### Finds sim value for specific topic
            if doc_comp[0] == topic_ind:
                sim = doc_comp[1]
                break
        ### Adds values for each to their respective lists
        sim_list.append(sim)
        word_list.append(topics_word[1])
    ### Adds list to their respective dict
    sim_disp_dict[num_topics] = sim_list
    word_disp_dict[num_topics] = word_list
    print("Added similarity metrics and words for topic model with " + str(num_topics) + " topics.")
    lda = models[num_topics]
    lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)
    ### Adds raw html to lda vis dict
    lda_vis_html[num_topics] = pyLDAvis.prepared_data_to_html(lda_display).\
    replace('<link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/bmabey/pyLDAvis/files/ldavis.v1.0.0.css">',"")
    print("Added similarity visualization for topic model with "+ str(num_topics) + " topics.")
## Populates dict with top 10 docs per topic
### Creates final dict for n number of different models
print("Building report for top 10 documents...")
top_10_docs_each_topic_dict = {}
for num_top_diff_model in n_t_array:
    #### Creates dict populated by each model 0,1,...,n-1
    temp_dict = {}
    for num_top_w_in_model in range(num_top_diff_model):
        ##### Creates dict value associated with each topic
        temp_dict[str(num_top_w_in_model)] = [[None, None]]
    for num_doc in range(len(text_data)):
        ##### Gets each document's topic weights
        doc_topic_weights = models[num_top_diff_model][corpus[num_doc]]
        ##### Goes through each topic, adds both doc data and topic weight to temp dict
        for num_doc_topic in range(len(doc_topic_weights)):
            topic_num = doc_topic_weights[num_doc_topic][0]
            topic_weight = doc_topic_weights[num_doc_topic][1]
            temp_dict[str(num_doc_topic)].append([topic_weight, text_data.iloc[num_doc]])
    #### Resets value
    num_top_w_in_model = 0
    for num_top_w_in_model in temp_dict:
        ##### Removes null value
        del(temp_dict[num_top_w_in_model][0])
        ##### Sorts temp dict, gets top 5 docs per topic
        temp_dict[num_top_w_in_model] = sorted(temp_dict[num_top_w_in_model], key = lambda x: x[0])[-6:-1]
    top_10_docs_each_topic_dict[str(num_top_diff_model)] = temp_dict

print("Writing report...")
# HTML report
## Creates/overwrites HTML report
f = open("report.html","w")
## Begins building text to be written to HTML
### Reintroduces (only once, however) the header text importing the LDA vis css
report = '''
<html>
<head>
<link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/bmabey/pyLDAvis/files/ldavis.v1.0.0.css">'''
### Begins adding the proper headings and style
report = report + '''
<style>
#documents {
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#documents td, #customers th {
  border: 1px solid #ddd;
  padding: 8px;
}

#documents tr:nth-child(even){background-color: #f2f2f2;}

#documents tr:hover {background-color: #ddd;}

#documents th {
  padding-top: 12px;
  padding-bottom: 12px;
  padding-right:12px;
  text-align: left;
  background-color: #de5253;
  color: white;
}
 a:link { color:#417ab1; }
 a:visited { color:#203d58; }
 a:hover { color:#de5253; }
 a:active { color:#de5253; }
* {font-family: sans-serif;}</style>
</head>
<h1>Text Similarity and Modeling Report</h1>
For an explanation of how this script works and how this report was generated, please view the project's <a href="https://github.com/bleonardi/text_similarity_and_modeling">GitHub</a>.
<h2 style="color:#203d58;">Document Similarity</h2>'''
report = report + "Below is a list of the top " + str(num_compare) + " documents most similar to the highlighted document, arranged from most similar to least."
report = report + '''<table id="documents">
  <tr>
      <th>Order</th>
      <th>Link</th>
  </tr>'''
### Creates table listing topics, their titles, urls in order of similarity
count = 1
for index, row in sim_doc_df.iterrows():
    report = report + '''
    <tr>
        <td>{}</td>
        <td><a href="{}">{}</a></td>
    </tr>'''.format(str(count),row["url"],row["title"])
    count = count+1
report = report + '</table><h2 style="color:#203d58;">Topic Modeling</h2>'
for num_topics in n_t_array:
    report = report + '<h3 style="color:#de5253;">' + str(num_topics) + ' Topics</h3>'
    for index in range(num_topics):
        top_text = 'Topic ' + str(index+1) + ' ' 
        report = report + '<h4 style="color:#5299de">' + top_text + '</h4>'
        report = report + '<h5>% Similarity of Highlighted Document to ' + top_text + ":" + str(round(100*sim_disp_dict[num_topics][index],2)) + '%</h5>'
        report = report + '<h5>5 Most Representative Documents of ' + top_text
        curr_topic_top_10 = top_10_docs_each_topic_dict[str(num_topics)][str(index)]
        report = report + '''<table id="documents">
        <tr>
            <th>Order</th>
            <th>Link</th>
            <th>% Representative of Topic # {}</th>
        </tr>'''.format(str(index + 1))
        for rank in range(len(curr_topic_top_10)-1,-1,-1):
            act_rank = 10-rank
            text_obj = curr_topic_top_10[rank][1]
            percent = round(curr_topic_top_10[rank][0]*100,2)
            title = text_obj.loc["title"]
            url = text_obj.loc["url"]
            report = report + '''
            <tr>
                <td>{}</td>
                <td><a href="{}">{}</a></td>
                <td>{}%</td>
            </tr>'''.format(str(act_rank),url,title,str(percent))
        report = report + '</table>'
    report = report + lda_vis_html[num_topics]
f.write(report)
f.close()
