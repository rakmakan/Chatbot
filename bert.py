import nltk
import re
from sentence_transformers import SentenceTransformer

s_bert_model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
s_bert_model.max_seq_length = 450
def s_bert(text):
    
    # s_bert_model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
    return s_bert_model.encode(text)

def vectorizer():
    
    encoded_sent = []
    sentences = []
    with open('corona_virus.txt',encoding='utf-8') as fp:
        for i in fp:
            # print("\n".join(i.split('. ')))
            text = re.sub('i\.e\.', 'that is', i)
            text = re.sub('[\[\d+\]]', '', text)
            text = re.sub('[A-Z]\.', '', text)
            text = re.sub('[^A-Za-z0-9\s\.]*', '', text)
            text = re.sub('([A-Z]{3,})', '', text)
            if text == '\n':
                continue
            for txt in text.split('. '):
                if len(txt) >= 100:
                    encoded_sent.append(s_bert(text))
                    sentences.append(text)
            
    
    return encoded_sent, sentences


