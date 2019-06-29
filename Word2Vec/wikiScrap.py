import bs4 as bs  
import urllib.request  
import re  
import nltk
from gensim.models import Word2Vec

scrapped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')  
article = scrapped_data .read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:  
    article_text += p.text


#Now we have to PREPROCESS the text 

# Cleaing the text
processed_article = article_text.lower()  
processed_article = re.sub('[^a-zA-Z]', ' ', processed_article )  
processed_article = re.sub(r'\s+', ' ', processed_article)

# Preparing the dataset
all_sentences = nltk.sent_tokenize(processed_article)

all_words = [nltk.word_tokenize(sent) for sent in all_sentences]

# Removing Stop Words
from nltk.corpus import stopwords  
for i in range(len(all_words)):  
    all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]

#the all_words variable contains the list of all the words in the article

