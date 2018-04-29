
# coding: utf-8

# In[5]:


import nltk
from pyiwn import pyiwn


def overlapcontext( synset, sentence ):
    
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
    
    return len( gloss.intersection(sentence) )

def lesk( word, sentence ):
    
    bestsense = None
    maxoverlap = 0
    for x in range(len(iwn.synsets(word))):
        sense = iwn.synsets(word)[x];
        overlap = overlapcontext(sense,sentence)
        if overlap > maxoverlap:
                maxoverlap = overlap
                bestsense = x
    
    return bestsense

def test(sentence,words):
    count = [0,0,0]
    for i in words:
        j=i[:-2];
        if int(i[-1]) <= len(iwn.synsets(j)) :
            predicted = lesk(j,sentence);
            original = iwn.synsets(j)[int(i[-1])-1]
            if int(i[-1])-1 == predicted :
                count[0] = count[0] + 1;
            elif predicted!=None :
                count[1] = count[1] + 1;
            else:
                count[2] = count[2] + 1;
    
    return count


iwn= pyiwn.IndoWordNet('sanskrit');

file = open('/home/clabuser/Documents/nludivya/aaruni.txt',
              encoding='utf-8').read()
a=nltk.word_tokenize(file);

sentence=[];
words=[];
count= [0,0,0]

for i in a:
    if(i[-1].isdigit()):
        words.append(i);
        i=i[:-2]
    if(i=='।'):
        cc = test(sentence,words);
        count[0] = count[0] + cc[0];
        count[1] = count[1] + cc[1];
        count[2] = count[2] + cc[2];
        words[:]=[];
        sentence[:]=[];
    sentence.append(i);    

print("Number of correctly classified words :",count[0])
print("Number of wrongly classified word -",count[1])
print("Number of unclassified word(due to limitation of wordnet pyiwn)-",count[2])

print("Accuracy :", (count[0]/(count[0]+count[1]+count[2])))


# In[6]:


print("sda",count[0])


# In[9]:


print("Accuracy :", (count[0]/(count[0]+count[1]+count[2])))

