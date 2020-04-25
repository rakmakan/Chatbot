import nltk
import re
from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from itertools import permutations
from sklearn.naive_bayes import MultinomialNB
from nltk.stem import WordNetLemmatizer
from itertools import permutations
import math
from sklearn.metrics import accuracy_score
import csv
from difflib import SequenceMatcher
from flask import Flask
lemmatizer = WordNetLemmatizer() 
stop_words = set(stopwords.words("english"))


def query(statement):
    parse_st = sent_tokenize(statement)
    parse_words = []
    key_words_stop = []
    for i in parse_st:
        j = word_tokenize(i)
        parse_words.append(j)
    for i in parse_words:
        for j in i:
            if j not in stop_words:
                key_words_stop.append(j)
    return key_words_stop

def ques_suggestion():
    df_qs  = pd.read_csv('ques_ans.csv',encoding = "ISO-8859-1")
    qus_array = np.array(df_qs['A'])
    parse_words = []
    key_words_stop_ques = []
    for i in qus_array:
        j = word_tokenize(i)
        parse_words.append(j)
    for i in parse_words:
        for j in i:
            if j not in stop_words:
                key_words_stop_ques.append(j)
    
    return print(key_words_stop_ques)



def tagger(statement):
    tokenized = sent_tokenize(statement)
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            print(tagged)
            array = np.array(tagged)
            key_words = []
            ##print(array)
            for row in array:
                for i in range(len(row)):
                    if (row[i] == 'JJ' or row[i]=='JJR' or row[i]=='JJS' or row[i]=='VBG' or row[i]=='MD'
                        or row[i]=='VB' or row[i]=='VBN' or row[i]=='NNS' or row[i]=='NNP'):
                        row[1]='NN'
                
            ##print(array)
            for row in array:
                ##print(row)
                ##print(len(row))
                for i in range(len(row)):
                    ##print(row[i])
                    if (row[i]=='NN'):
                        key_words.append(row[0].lower())

    except Exception as e:
        print(str(e))
    ##print(key_words)
    return key_words


def statement_type(statement):
    df_train =  pd.read_csv('simple converstion.csv') ##entering the test date base(csv)
    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(df_train['question'].values)
    classifier = MultinomialNB()
    target = df_train['type'].values
    classifier.fit(counts,target)
    example = sent_tokenize(statement)
    example_counts = vectorizer.transform(example)
    predictions = classifier.predict(example_counts)
    return predictions


def database_cleaning():
        df =  pd.read_csv('ques_ans.csv',encoding = "ISO-8859-1")
        words = []
        lines = np.array(df['A'])
        for i in lines:
            word = word_tokenize(i)
            tagged = nltk.pos_tag(word)
            
            words.append(tagged)
        ## print(words)
        word_array = np.array(words)

        word_refesh = []
        for j in range(len(words)):
            row_list = []
            for row in words[j]:
                my_list = list(row)
                for i in range(len(my_list)):                    
                    if (my_list[i] == 'JJ' or my_list[i]=='JJR' or
                        my_list[i]=='JJS' or my_list[i]=='VBG' or my_list[i]=='MD' or
                        my_list[i]=='VB' or my_list[i]=='VBN' or my_list[i]=='PRP$' or my_list[i]=='NNS' or my_list[i]=='NNP'):
                        my_list[1]='NN'
                row_list.append(my_list)
            word_refesh.append(row_list)
                
        ##print(word_refesh)
        key = []      
        for j in range(len(word_refesh)):
            mylist = []
            for row in word_refesh[j]:
                for i in range(len(row)):
                    if (row[i]=='NN'):
                        mylist.append(row[0].lower())    
            key.append((mylist))
        ##print(mylist)
        ##print(key)
        df['key'] = key
        df.to_csv('ques_ans.csv', sep=',',index = False,encoding = "ISO-8859-1")
        return key





def response_struct(prediction,key_words,key_words_stop,key,Comb_Array,statement):
    
        df =  pd.read_csv('ques_ans.csv',encoding = "ISO-8859-1")
        df_combination = pd.read_csv('all_combinations.csv')
        ##33print(words)
        
        count = []
        
        result = 0
        join_keywords = (' ').join(key_words)
        join = str(join_keywords)
        myarray = np.array(df_combination['col'])
        
        for i in myarray:
            count.append(int((SequenceMatcher(None,join,i).ratio())*10))

        ##print(count)

        
        if 8 in count or 9 in count or 10 in count or 7 in count or 6 in count or 5 in count:
            vectorizer = CountVectorizer()
            count1 = vectorizer.fit_transform(df['key'].values)
            classifier = MultinomialNB()
            target = df['B'].values
            classifier.fit(count1,target)
            example = sent_tokenize(join_keywords)
            example_counts = vectorizer.transform(example)
            predictions = classifier.predict(example_counts)
            c = 0
            DEMO = []
            if len(key_words)==1:
                #print(key)
                for k in key_words:
                    for i in key:
                    ##print(i)
                        for j in i:
                        ##print(j,)
                            if j == k:
                                DEMO.append(i)
                ##print(DEMO)
                DEMO2 = []
                for i in DEMO:
                    DEMO2.append(" ".join(i))
                print(df)
                df_test = df.loc[df['type'] == 'G']
                print(df_test)
                array = np.array(df_test['key'])
                ##print(array)
            
                ##print(DEMO2)
                vectorizer = CountVectorizer()
                count1 = vectorizer.fit_transform(df['key'].values)
                classifier = MultinomialNB()
                target = df['B'].values
                classifier.fit(count1,target)
                example_counts = vectorizer.transform(array)
                predi = classifier.predict(example_counts)
                ##print(predi)

                predi = str(predi)
                predi = predi.replace('[',' ')
                predi = predi.replace(']',' ')
                predi = predi.replace('\'','<br/>')
                predi = predi.replace('\n','')
                print(predi)
                return predi

            else:
                for i in predictions:
                    return i
            

        else:
            a = "not found"
            df2  = pd.DataFrame([[statement]], columns=list('A'))
            df_n_ans =  pd.read_csv('no_ans.csv')
            df_n_ans = df_n_ans.append(df2)            
            df_n_ans.to_csv('no_ans.csv',index = False)
            return a

       

def comb_for_four(key):
    list_all_comb_four = []
    list4 = []
    for i in key:
        if len(i)==4:
          list4.append(i)
    #print(list4)
    for i in list4:
        for x in permutations(i):
            v = list(x)
            list_all_comb_four.append(" ".join(v))
    return list_all_comb_four

def comb_for_three(key):
    list_all_comb_three = []
    list3 = []
    for i in key:
        if len(i)==3:
          list3.append(i)
    #print(list3)
    for i in list3:
        for x in permutations(i):
            v = list(x)
            list_all_comb_three.append(" ".join(v))
    return list_all_comb_three

def comb_for_two(key):
    list_all_comb_two = []
    list2 = []
    for i in key:
        if len(i)== 2:
          list2.append(i)
    #print(list2)
    for i in list2:
        for x in permutations(i):
            v = list(x)
            list_all_comb_two.append(" ".join(v))
    return list_all_comb_two

def comb_for_one(key):
    list_all_comb_one = []
    list1 = []
    for i in key:
        if len(i)== 1:
          list1.append(i)
    return list1
    

def comb_for_five(key):
    list_all_comb_five = []
    list5 = []
    for i in key:
        if len(i)==5:
          list5.append(i)
    #print(list5)
    for i in list5:
        for x in permutations(i):
            v = list(x)
            list_all_comb_five.append(" ".join(v))
    return list_all_comb_five


def all_comb_csv(list_all_comb_four,list_all_comb_three,list_all_comb_two,list_all_comb_five,list_all_comb_one):
    f = open("all_combinations.csv", "w")
    f.truncate()
    columnTitleRow = [["col"]]
    writer = csv.writer(f)
    writer.writerows(columnTitleRow)
    f.close()
    
    df_comb =  pd.read_csv('all_combinations.csv')

    df_comb4 = pd.DataFrame({'col':list_all_comb_four})

    df_comb3  = pd.DataFrame({'col':list_all_comb_three})

    df_comb1  = pd.DataFrame({'col':list_all_comb_one})
   
    df_comb2  = pd.DataFrame({'col':list_all_comb_two})
    
    df_comb5  = pd.DataFrame({'col':list_all_comb_five})
    
    df_comb   = df_comb.append(df_comb4)
    
    df_comb   = df_comb.append(df_comb3)
    
    df_comb   = df_comb.append(df_comb1)

    df_comb   = df_comb.append(df_comb2)
    
    df_comb   = df_comb.append(df_comb5)

    df_comb.to_csv('all_combinations.csv', sep=',')
    Comb_Array = np.array(df_comb['col'])
    ##print(Comb_Array.shape)
    Comb_Array = Comb_Array.reshape((len(Comb_Array),1))
    ##print(Comb_Array.shape)
    ##Comb_list = list(Comb_Array)
    return Comb_Array



###ques_suggestion()


from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.HTML")

@app.route("/get")
def get_bot_response():
    statement = request.args.get('msg')
    print(statement)
    statement = statement.lower()
    key = database_cleaning()
    four = comb_for_four(key)
    ##print(four)
    three = comb_for_three(key)
    two = comb_for_two(key)
    five = comb_for_five(key)
    one = comb_for_one(key)
    Comb_Array = all_comb_csv(four,three,two,five,one)
    key_words_stop = query(statement)
    key_words = tagger(statement)
    pred = statement_type(statement)
    result = response_struct(pred,key_words,key_words_stop,key,Comb_Array,statement)
    return str(result)

if __name__ == '__main__':
   app.run(debug = True)
#'''C:\Users\rmaka\Downloads\chatbot\index3 (1).HTML'''