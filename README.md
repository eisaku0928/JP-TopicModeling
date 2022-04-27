# JP-TopicModeling
LDA topic modeling on Japanese news corpus, utilizing MeCab and gensim.
News corpus comes from a popular news website known as "Live Door News".

```JpTopicModeling.ipynb``` contains the wholesome process of preprocessing japanese text data, gaining POS tags, applying LDA on the tokenized corpus by defining stopwords and identifying nouns and proper nouns, and finally visualizing the output using wordclouds and pyLDAvis.

## Usage
Install required libraries using:
```
pip install mojimoji
pip install MeCab
```
