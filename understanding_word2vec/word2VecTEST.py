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

word2vec = Word2Vec(all_words, min_count=2)  # A value of 2 for min_count specifies to include only those words in the Word2Vec model that appear at least twice in the corpus. 
vocabulary = word2vec.wv.vocab  #This variable contains all words in the entire text that appears at least twice in this one.


v1 = word2vec.wv['artificial']  #The vector v1 contains the vector representation for the word "artificial"


sim_words = word2vec.wv.most_similar('intelligence')  #this allow us to find all words similar to the word "intelligence"

print(sim_words) #Just for testing the library. From the output, you can see the words similar to "intelligence" along with their similarity index. The word "ai" is the most similar word to "intelligence" according to the model, which actually makes sense. Similarly, words such as "human" and "artificial" often coexist with the word "intelligence". 

