# cosc426-final-jordan-lily-mel
Final project for CS 426 looking at genre classification of song lyrics across various languages

The sequence of steps to go from dataset to sample .tsv files is as follows:
- Use the train.csv file at the linked page and create python scripts that filter by language to create a new two new training files; one will only contain English songs and the other will contain English, Spanish, and Portuguese song lyrics.
- Then create a script to modify both files such that the distribution of number of examples across genres, as well as overall length, is the same for both the English-only and mulitlingual datasets.
- Lastly, we will split these two modified train files into a 90:10 split so that we have two train and two validate .tsv files.

To get from the output of NLPScholar to our evaluation metrics table and figures: 
- Use the output tsv file from NLPScholar to obtain the accuracies for each language by target class
- Create an aggregated bar chart that groups each genre and displays bars for each language with accuracies on the y-axis to display each fine-tuned models' performance.
- Create a scatter plot that maps base model perplexity against finetuned model accuracy for each language.
