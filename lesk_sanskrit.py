
# coding: utf-8

# In[14]:


import nltk
import re, math
from pyiwn import pyiwn
from collections import Counter

def cosine_similarity(sent1, sent2): #
    """
    Calculates cosine between 2 sentences/documents.
    Thanks to @vpekar, see http://goo.gl/ykibJY
    """
    def get_cosine(vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(text):
        return Counter(text)

    vector1 = text_to_vector(sent1)
    vector2 = text_to_vector(sent2)
    cosine = get_cosine(vector1, vector2)
    return cosine


def overlapcontext( synset, sentence,cos_sim= False ):
    
    gloss = set(nltk.word_tokenize(synset.gloss()))
    for i in synset.examples():
        gloss=gloss.union(set(nltk.word_tokenize(i)))
    
    if isinstance(sentence, str):
        sentence = set(sentence.split(" "))
    elif isinstance(sentence, list):
        sentence = set(sentence)
    elif isinstance(sentence, set):
        pass
    else:
        return
    
    if cos_sim:
        value = (cosine_similarity(gloss, sentence))
    else:
        value = len( gloss.intersection(sentence) )
    return value
    
def lesk( word, sentence,cos_sim=False ):
    
    bestsense = None
    maxoverlap = 0
    
    for x in range(len(iwn.synsets(word))):
        sense = iwn.synsets(word)[x]
        overlap = overlapcontext(sense,sentence,cos_sim)
        if overlap > maxoverlap:
                maxoverlap = overlap
                bestsense = x
    
    return bestsense

def test(sentence,words,cos_sim=False):
    count = [0,0,0]
    for i in words:
        j=i[:-2]
        if int(i[-1]) <= len(iwn.synsets(j)) :
            predicted = lesk(j,sentence,cos_sim)
            original = iwn.synsets(j)[int(i[-1])-1]
            if int(i[-1])-1 == predicted :
                count[0] = count[0] + 1
            elif predicted!=None :
                count[1] = count[1] + 1
            else:
                count[2] = count[2] + 1
    
    return count


iwn= pyiwn.IndoWordNet('sanskrit')

file = open('path/labeled_data.txt',
              encoding='utf-8').read()
a=nltk.word_tokenize(file);

sentence=[]
words=[]
count= [0,0,0]

for i in a:
    if(i[-1].isdigit()):
        words.append(i)
        i=i[:-2]
    if(i=='।'):
        cc = test(sentence,words,cos_sim = True);
        count[0] = count[0] + cc[0]
        count[1] = count[1] + cc[1]
        count[2] = count[2] + cc[2]
        words[:]=[];
        sentence[:]=[]
    sentence.append(i)

print("Number of correctly classified words :",count[0])
print("Number of wrongly classified word -",count[1])
print("Number of unclassified word(due to limitation of wordnet pyiwn)-",count[2])

print("Accuracy :", (count[0]/(count[0]+count[1]+count[2])))


# In[6]:





# In[9]:




