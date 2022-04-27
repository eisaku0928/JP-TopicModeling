# JP-TopicModeling
LDA topic modeling on Japanese news corpus, utilizing MeCab and gensim.
News corpus comes from a popular news website known as "Live Door News".
[Topic Modeling](https://en.wikipedia.org/wiki/Topic_model) is an unsupervised machine learning technique used to statistically detect clusters of words and similar expressions to classify a set of text data or documents. In this case, each document is one news post, and there are 7367 Japanese news present within the corpus. 

```JpTopicModeling.ipynb``` contains the wholesome process of preprocessing japanese text data, gaining POS tags, applying LDA on the tokenized corpus by defining stopwords and identifying nouns and proper nouns, and finally visualizing the output using wordclouds and pyLDAvis.

```MeCabBasics.ipynb``` will contain the basic operations for tokenization and part-of-speech identification that is done by using the MeCab library. 

## Usage
Install required libraries using:
```
pip install mojimoji
pip install MeCab
```
