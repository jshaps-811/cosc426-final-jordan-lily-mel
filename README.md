# cosc426-final-jordan-lily-mel
Final project for CS 426 looking at genre classification of song lyrics across various languages

The sequence of steps to go from dataset to sample .tsv files is as follows:
- Use the train.csv file at the linked page and create python scripts that filter by language to create a new two new training files; one will only contain English songs and the other will contain English, Spanish, and Portuguese song lyrics.
- Then create a script to modify both files such that the distribution of number of examples across genres, as well as overall length, is the same for both the English-only and mulitlingual datasets.
- Lastly, we will split these two modified train files into a 90:10 split so that we have two train and two validate .tsv files.

To get from the output of NLPScholar to our evaluation metrics table and figures: 
- Use the output tsv file from NLPScholar to compare the predicted genre with the target genre.
- Organize these individual predictions (accurate or not) by language and by genre.
- Create a table that displays the accuracies organized first by language and then by genre.
- Create a matrix that has each language as rows, and each genre as columns, and displays the accuracy for each cross section. We can also have an overall accuracy for each row/ column.
