from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://postgres:root@localhost:5432/findata_sentimentanalysis')
dataflair_read_table=pd.read_sql('select headline from stock_news_sentiment_scores',con=engine)

comment_words = ''
stopwords = set(STOPWORDS)

for val in dataflair_read_table.headline:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()
     
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size =10).generate(comment_words)
 
# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()
