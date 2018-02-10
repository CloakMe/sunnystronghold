from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
# from sklearn.feature_extraction.text import CountVectorizer

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        words = word_tokenize(doc)
        tokens = pos_tag(words)
        res = []
        for (word, pt) in tokens:
            wn_pt = self.get_wordnet_pos(pt)
            res.append(self.wnl.lemmatize(word, wn_pt))
        return res
    
    def get_wordnet_pos(self,treebank_tag):
        """
        return WORDNET POS compliance to WORDENT lemmatization (a,n,r,v) 
        """
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            # As default pos in lemmatization is Noun
            return wordnet.NOUN

# vect = CountVectorizer(tokenizer=LemmaTokenizer())

# text = "I'm fucking this bitch in the ass"
# print(LemmaTokenizer().__call__(text))