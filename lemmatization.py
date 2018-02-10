from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
# from sklearn.feature_extraction.text import CountVectorizer

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
        self.allowedSpecials = ['-','.','\'','`']
    def __call__(self, doc):
        words = word_tokenize(doc)
      
        tokens = pos_tag(words)
        res = []
        for (word, pt) in tokens:
            wn_pt = self.get_wordnet_pos(pt)
            word = word.lower()
            word = self.wnl.lemmatize(word, wn_pt)
            valid = True;
            if len(word) < 2:
                valid = False;
            for letter in word:
                if letter.isalnum() or (letter in self.allowedSpecials):
                    pass
                else:
                    valid = False;
            if bool(re.match("^[-.'`]+$", word)):
                valid = False
            # version numbers: 2.3.x
            if bool(re.match("^(\d+\.)+((\d+)|x)$", word)):
                valid = False
            if valid:
                res.append(word)
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