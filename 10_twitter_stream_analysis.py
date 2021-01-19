import sqlite3
import pandas as pd

conn = sqlite3.connect('twitter.db')
c = conn.cursor()

#grabing a term from the database
#loading it into a dataframe
#unix decending to get latest tweets
#1000 to limit the quantity
df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE '%stock%' ORDER BY unix DESC LIMIT 1000", conn)

#sorting
df.sort_values('unix', inplace=True)

#smoothing the sentiment column using a moving avaerage method
#divide by 5 is 1000/5 , = 200 data avg, we could do even smaller values
df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()

#dropping the null values
df.dropna(inplace=True)

print(df.tail())