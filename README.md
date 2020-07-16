# Text Similarity and Modeling
A poorly-maintained document similarity and topic modeling script. Allows one to use HathiTrust Research Center (HTRC) worksets, or simply collections of .txt documents to compare with a target document also in .txt format.

## Steps
From the command line, run `text_sim_model.py is_HTRC file_locs`.
### is_HTRC
Either “True” or “False,” depending on whether the analysis is being conducted on a corpus of HTRC volumes or a local directory of text files.
### file_locs
A string (i.e., surrounded by quotes) pointing to the location of either the [HTRC-provided Extracted Features Download Helper](https://analytics.hathitrust.org/algorithms) saved as `"script.sh"` file _or_ the directory of .txt files for analysis (must be in absolute format - the full address of the directory e.g., `“C:/Users/USER/Documents”`)
***Use forward slashes***

## Required Files
### For _both_ HTRC and local .txt corpi
The text of the document you wish to “highlight” (e.g., Newton’s _de Gravitatione_) must be saved as `“file_for_analysis.txt”`
### For HTRC corpi
### For local.txt corpi
