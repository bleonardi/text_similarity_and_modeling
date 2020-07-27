# Text Similarity and Modeling
A document similarity and topic modeling script. Allows one to use HathiTrust Research Center (HTRC) worksets, or simply collections of .txt documents to compare with a target document also in .txt format. Both the similarity metric and topic modeling use a combination of Python's [NLTK](https://www.nltk.org/) and [GenSim](https://radimrehurek.com/gensim/) packages.
## Similarity Metrics
This script uses GenSim's built-in [_Term Frequency Inverse Document-Frequency_](https://radimrehurek.com/gensim/models/tfidfmodel.html) model in order to build out a list of the most similar documents to the highlighted document.
## Topic Modeling
For topic modeling, this utilizes GenSim's [Latent Dirichilet Allocation](https://radimrehurek.com/gensim/models/ldamodel.html) model trained on te specified corpus.

## Steps
From the command line, run `text_sim_model.py`_`is_HTRC has_custom_stop file_locs num_compare num_topics`_.
### _`is_HTRC`_
A boolean (with value either `True`or `False`) stating whether the analysis is being conducted on a corpus of HTRC volumes or a local directory of text files.
### _`has_custom_stop`_
A boolean (with value either `True` or `False`) stating whether the user is passing a custom stopwords file (saved as `custom_stop.txt`) listing (seperated by spaces) words to be excluded from the model.
### _`file_locs`_
A string (i.e., surrounded by quotes) pointing to the directory of either where the [HTRC-provided Extracted Features Download Helper](https://analytics.hathitrust.org/algorithms) saved a whole host of folders and files _or_ the directory of .txt files for analysis (must be in absolute format - i.e., the full address of the directory).
### _`num_compare`_
An integer stating the number of documents to which you would like your _highlighted document_ compared.
### _`num_topics`_
A list of the number of topics for each topic model.

## Required Files
### For _both_ HTRC and local .txt corpi
You must save the text of the document you wish to “highlight” (e.g., Newton’s _de Gravitatione_) as `“file_for_analysis.txt”`.
### For HTRC corpi
You must have run the above-mentioned [HTRC-provided Extracted Features Download Helper](https://analytics.hathitrust.org/algorithms) for your specific workset of volumes.
### For local .txt corpi
You must have the documents to which you'd like to compare the highlighted text saved in the format `author name-title of text.txt`, where the author's name and multi-word document titles are seperated from each other by a hyphen.

## Example
`python text_sim_model.py False True “C:/Users/USER/Documents/The_files_are_in_THIS_directory” 10 4 8 16` would execute a .txt analysis on all .txt files in the `The_files_are_in_THIS_directory`, highlighting the document at `The_files_are_in_THIS_directory/file_for_analysis.txt`, excluding the words contained in `custom_stop.txt`, and comparing it to 10 other documents, while generating 3 topic models with 4, 8, and 16 topics, respectively.
