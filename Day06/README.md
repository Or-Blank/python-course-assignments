# Epitopes Sequences Comparison #

## Epitopes: ##
* Epitopes are short amino-acid sequences of an antigen that are the specific regions recognized by the immune system cells. 

* Comparing epitopes is important because similar sequences can trigger cross‑reactive immune responses, where the body reacts to different organisms as if they were the same. It’s interesting because these similarities can help explain allergy patterns and potential risks across related species with diffrent or similar epitopes.

## The sequences comparison: ##
* This project compares epitopes using global alignment from Biopython.

* The scroing system for the comparison:
Match = 1
Mismatch = 0
Gap = 0

* **Similarity -** The total number of matching amino acids in the alignment.

* **Identity -** The fraction of positions in the alignment where the amino acids are identical (matches_in_same_position / alignment_length).

* Example:
Seq1: KAEQVKASKEMGETLLRAVESYLLAHSDAYN
Seq2: NTALFKAIEAYLIAN
The sequences share 9 amino acids somewhere, so:
Similarity = 9
But none of these matches occur in the same aligned position once gaps are inserted, so:
Identity = 0.000

This happens because the scoring system I chose for this project, which allows unlimited gaps, that can maximize similarity even when identity remains low.

## Requiremment: ##
* pip install biopython
* pip install requests
* In the "Organism_Selection" file write the **ID** of the organisms you want to compare thier epitopes.
* To run the code, run from the "IEDB_Epitope_Comparison" file

## AI: ##
I used for this task the built in Copilot of VS and ChatGPT: 
* My main prompt in ChatGPT was: "I want to use the IEDB.org as a database for coding a python code for comparisons. I want a code as mush as using Biopython (as long as it neccecry and make sense to use), I want to get from the site the epitope of some food (from the same family like celery and carrot I chosed) and comapre the diffrent epitopes based on the sequencs by identity and similarity."
* After that I used the Copilot in order to fix problems I had - the main issue was the the the organism selection via name did not work; so I used the AI help to change it from name to by ID number.

 
