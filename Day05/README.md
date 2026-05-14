

## Description: ##
* The table is...

* What I did with the data is...

* By organizing the data in this format we can easily see and learn more about B‑cell lineage “destiny” and differentiation.
  We can identify the different clones, see which ones expanded the most, and think why those specific clones were selected - using also the seq we have.
  At the same time, the distribution of each clone across the various B‑cell derivative types helps us understand the functional role each clone adopted and why certain clones differentiated toward one fate while others followed a different path.
  
  * This structure turns the dataset into a clear view of clonal behavior, selection, and specialization within the immune response.

## Requiremment: ##
* Before runing the script, read the notes I added inside the script to get the wanted result.

## AI: ##
* My main prompt in ChatGPT was: Make a pythonc code that will take this data or any other excel date in the same format, and will: 1. Rank the clones based on the clone_count 2. For each clone make a table of the cluster_annotated for each group and the precent they are from the total groups within the groups. 3. Take all the clusters and make a table of the cluster_annotated (cell type) comparing the precentage againts all of the cells.
* After that I used the VC copilot to adjust the code