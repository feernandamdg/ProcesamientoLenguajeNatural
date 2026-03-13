import nltk
nltk.download('wordnet')
nltk.download('Omw-1.4')

from nltk.corpus import wordnet as wn
word='tree'
car_syns=wn.synsets(word)

#The definition of each synset of car synsets
print(car_syns)
syns_defs = print('\t', [car_syns[i].definition() for i in range(len(car_syns))],'\n')

# Get the lemmas for the first Synset
car_lemmas = car_syns[1].lemmas()
print('\t',car_lemmas, '\n')
# Let's get hypernyms for the a Synset (general superclass)
syn = car_syns[1]
print("Hiperónimo")
print('\t', syn.hypernyms()[0].name(), '\n')

# Let's get hyponyms for a Synset (specific subclass)
syn = car_syns[1]
print("Hipónimo")
print('\t', syn.hyponyms()[0].name(), '\n')

# Let's get part-holonyms for the third "car"
# Synset (specific subclass)

print("Holonimos")
print('\t',[holo.name() for holo in syn.part_holonyms()[:]], '\n')

word2 = 'table'
dog_syns = wn.synsets(word2)

syns_defs = print('\t', [dog_syns[i].definition() for i in range(len(dog_syns))],'\n')