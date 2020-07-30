[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/bleonardi/text_similarity_and_modeling/master)
# Text Similarity and Modeling
A document similarity and topic modeling script. Allows one to use HathiTrust Research Center (HTRC) worksets, or simply collections of .txt documents to compare with a target document also in .txt format. Both the similarity metric and topic modeling use a combination of Python's [NLTK](https://www.nltk.org/) and [GenSim](https://radimrehurek.com/gensim/) packages, and the visualization software used is [pyLDAvis](https://github.com/bmabey/pyLDAvis). An example report (what is created upon the succesful completion of the script) is visible [here](https://htmlpreview.github.io/?https://github.com/bleonardi/text_similarity_and_modeling/blob/master/report.html).
## Algorithms
This script uses GenSim's built-in [_Term Frequency Inverse Document-Frequency_](https://radimrehurek.com/gensim/models/tfidfmodel.html) model in order to build out a list of the most similar documents to the highlighted document, and uses [_Latent Dirichilet Allocation_](https://radimrehurek.com/gensim/models/ldamodel.html) to create topic models trained on the specified corpus.

## Steps
Before beginning, download and extract the `setup_files.zip` in the directory of your choosing, and ensure that you run `python setup.py`. Note: this requires pip to be installed on your machine. Then, from the command line, run `text_sim_model.py`_`is_HTRC has_custom_stop file_locs num_compare num_topics`_.
### _`is_HTRC`_
A boolean (with value either `True`or `False`) stating whether the analysis is being conducted on a corpus of HTRC volumes or a local directory of text files.
### _`has_custom_stop`_
A boolean (with value either `True` or `False`) stating whether the user is passing a custom stopwords file (saved as `custom_stop.txt`) listing words to be excluded from the model, simply seperated by spaces.
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
You must have the documents to which you'd like to compare the highlighted text saved in any format that will be recognizable to you.

## Example
`python text_sim_model.py False True “C:/Users/USER/Documents/The_files_are_in_THIS_directory” 10 4 8 16` would execute a .txt analysis on all .txt files in the `The_files_are_in_THIS_directory`, highlighting the document at `The_files_are_in_THIS_directory/file_for_analysis.txt`, excluding the words contained in `custom_stop.txt`, and comparing it to 10 other documents, while generating 3 topic models with 4, 8, and 16 topics, respectively.
