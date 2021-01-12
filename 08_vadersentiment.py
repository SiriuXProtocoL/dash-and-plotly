#/usr/bin/python3 -m pip install vadersentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import io
#Some basics Understanding
#analyzer = SentimentIntensityAnalyzer()
#vs = analyzer.polarity_scores("VADER Sentiment looks interesting, I have high hopes!")
#print(vs)
analyzer = SentimentIntensityAnalyzer()

pos_count = 0
pos_correct = 0

threshold = 0.5

with io.open("data/positive.txt","r", encoding='latin-1') as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)

        if not vs['neg'] > 0.1:
            if vs['pos']-vs['neg'] > 0:
                pos_correct += 1
            pos_count +=1


neg_count = 0
neg_correct = 0

with io.open("data/negative.txt","r", encoding='latin-1') as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if not vs['pos'] > 0.1:
            if vs['pos']-vs['neg'] <= 0:
                neg_correct += 1
            neg_count +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))