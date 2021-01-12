#/usr/bin/python3 -m pip install textblob vadersentiment
from textblob import TextBlob
import io

pos_count = 0
pos_correct = 0

with io.open("data/positive.txt","r", encoding='latin-1') as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)
        #the objectivity to subjectivity threshold
        if analysis.sentiment.subjectivity > 0.8:
            #the polarity threshold
            if analysis.sentiment.polarity > 0:
                pos_correct += 1
            pos_count +=1


neg_count = 0
neg_correct = 0

with io.open("data/negative.txt","r", encoding='latin-1') as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)
        #the objectivity to subjectivity threshold
        if analysis.sentiment.subjectivity > 0.8:
            #the polarity threshold
            if analysis.sentiment.polarity <= 0:
                neg_correct += 1
            neg_count +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))