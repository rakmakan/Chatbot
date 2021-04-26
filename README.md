# Chatbot


### In this project there are two algorithms 
1. Rules based algorithm
  * The rule based algorithm is accessible by running the rule_based.py
  * It reads data from the CSV file which can be updated with domain specific data
  * In case the chatbot doesnot have any answer then the question can be sent to the csv file "no_ans.csv"
  * In this the chat bot replies based on the word matching


2. Model based algorithm
  * This part of the bot is under developement. Currently it uses SBERT model to derive the sentence vectors
  * The cosine similarity between the input and the stored data is matched to produce an output
 
