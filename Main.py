# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 17:54:23 2021

@author: User
"""

import pandas as pd
import numpy as np
import re
import string
import random


script= "Three Rings for the Elven-kings under the sky,seven for the Dwarf-lords \
in their halls of stone, nine for mortal men doomed to die, one for the dark \
lord on his dark throne in the land of Mordor where the shadows lie. One ring to \
rule them all, one ring to find them, one ring to bring them all, and in the \
darkness bind them, in the land of Mordor where the shadows lie."

#%%
# SETTING UP THE TEST SOURCE TEXT

# Reconstruction of sentences from component pieces.

# converting everything to lowercase
script = script.lower()

# Split the string up using re.findall
splitScript = np.array(re.findall(r"\w+|[^\w\s]", script, re.UNICODE))

# Now create the data array:
posInArr = np.arange(0,len(splitScript),1)

# create a list of punctuation to search
punc = np.array(re.findall(r"\w+|[^\w\s]", string.punctuation, re.UNICODE))

# Create an array of true/false statements to determine if the value is a 
# piece of punctuation.
isPunc = np.array([False]*len(splitScript))

for i in range(len(splitScript)):
    # Manipulate truthy and falsy python mechanic for quicker computation
    # Rather than loop through whole array, this helps vectorise a step.
    if np.sum(splitScript[i] == punc) > 0:
        isPunc[i] = True

# We can scramble the data so that it appears in a random order in the dataframe
# we construct.
random.seed(0) # setting a random seed insures reproducability.
randOrder = np.array(random.sample(range(len(splitScript)), len(splitScript)))



# Create the test dataframe:
testData = pd.DataFrame({"Word":splitScript[randOrder],\
                         "Order":posInArr[randOrder],\
                         "is_punctuation":isPunc[randOrder]})




#%%
# PART 1.



# Rather than including several if statements we can group rules by taking
# advantage of the truthy and falsey mechanics of python.
def CheckPunc(word):
    """
    Checks the type of punctuation the word represents and returns trigger 
    conditions to apply the correct rule.
    Simple for now, however can be edited to include additional puncutation
    terms.

    Parameters
    ----------
    word : string
        DESCRIPTION. The input word as a string type. This is checked against 
        predefined punctuation specifications and edited accordingly

    Returns
    -------
    breaker : string
        DESCRIPTION. Add a space after the word.
    sentenceStart : bool
        DESCRIPTION. Do we start a new sentence after this punctuation?

    """
    if sum(word == np.array(["-","'",'"',"(","$","£","{","["])) > 0:
        return "", False
    
    elif sum(word == np.array([".","!","?"])) > 0:
        return " ", True
    
    elif sum(word == np.array([":",",",";",")","}","]"])) > 0:
        return " ", False
    
    
    
# sort data by "Order" column
testData = testData.sort_values("Order")
sentence = '' # sentence to store the string


# Starting conditions
sentenceStart = True
breaker = " "


for i in range(len(testData['Word'])):
    word = testData['Word'].iloc[i]
    
    
    # Do we need to capitalize the first word? (Start condition)
    if sentenceStart == True:
        sentence += word.capitalize() + breaker
        sentenceStart = False

    
    # Test to see what type of punctuation rule we need to apply
    if testData["is_punctuation"].iloc[i] == True:
        breaker, sentenceStart = CheckPunc(word)
    else:
        breaker = " "
        
    # if the next word is a piece of punctuation, we will need to remove the 
    # breaker before the punctuation. Use a try statement as an error is raised
    # for the final word.
    try:
        if testData['is_punctuation'].iloc[i+1] == True:
            if sum(testData['Word'].iloc[i+1] == np.array(["(","$","£","{","["])) > 0:
                breaker = " "
            else:
                breaker = ""
    except:
        breaker = ""

        
    # Finally add the word with the relevant breaker onto the script.
    sentence += word + breaker
    
        
    
                
    
        
        
            
#%%
# PART 2.
     
   
        
def FindWord(sourceText, word):
    """
    returns the indicies of all occurences of a search term in a given
    source text.

    Parameters
    ----------
    sourceText : string
        DESCRIPTION. The source text which will be searched for the given search
        term
    word : string
        DESCRIPTION. The search term to be searched for in the sourceText

    Returns
    -------
    indices : numpy.ndarray
        DESCRIPTION. An array containing the indicies of all occurences of the
        word being searched, including punctuation.

    """
    
    
    # We could also just change the input to a string inside the function.
    if type(sourceText) != str:
        print("ERROR: Source text should be of type string")
    elif type(word) != str:
        print("ERROR: Search term should be of type string")
        
        
    # make everything lowercase
    sourceText = sourceText.lower()
    word = word.lower()
    
    
    # locate the start and end of arrays
    indices = [] # create an array to store the data
    for iteration in re.finditer(word, sourceText):
        # store the start and end indicies
        indices.append([iteration.start(),iteration.end()]) 
    
    
    # Here we check some conditions to finalise our index list
    toDelete = []
    for i in range(len(indices)):
        
        # We need to make sure that the search term is not part of a bigger
        # word. e.g "ring" is index 1-4 of "bring" to do that we use
        # an if-elif statement.
        
        #Surrounded by punctuation:
        if np.sum(np.array(sourceText[indices[i][1]]) == punc) >0 and \
            np.sum(np.array(sourceText[indices[i][0]-1]) == punc) >0:
            indices[i] = np.arange(indices[i][0]-1,indices[i][1]+1,1)
        # punctuation on the left
        elif np.sum(np.array(sourceText[indices[i][0]-1]) == punc) >0 and\
            np.array(sourceText[indices[i][1]]) == " ":
            indices[i] = np.arange(indices[i][0]-1,indices[i][1],1)
        # punctuation on the right
        elif np.sum(np.array(sourceText[indices[i][1]]) == punc) >0 and\
            np.array(sourceText[indices[i][0]-1]) == " ":
            indices[i] = np.arange(indices[i][0],indices[i][1]+1,1)
        # no punctuation
        elif sourceText[indices[i][1]] == " " and \
            sourceText[indices[i][0]-1] == " ":
            indices[i] = np.arange(indices[i][0],indices[i][1],1) 
        # if all these fail, then the index correspond to an instance of the
        # word within a larger word, so we remove that one from the list
        else:
            toDelete.append(i)
    
    if len(toDelete) > 0:
        indices = np.delete(indices, toDelete)
        
    
    return indices
       



#%%
# PART 3


# create function called checkBigram

def FindWordBigram(sourceText, word, bigrams):
    """
    

    Parameters
    ----------
    sourceText : string
        DESCRIPTION. The source text which will be searched for the given search
        term
    word : string
        DESCRIPTION. The search term to be searched for in the sourceText
    bigram : list of strings
        DESCRIPTION. A list of strings indicating the bigrams to be highlighted where 
        necessary

    Returns
    -------
    wordIndices : numpy.ndarray
        DESCRIPTION. An array containing the indicies of all occurences of the
        word being searched, or the bigram index, including punctuation.


    """
    
    
    wordIndices = FindWord(sourceText, word)
    
    # first check if the word is in a bigram

    
    for bigram in bigrams:
        # check to see if the word is part of a bigram
        if word in bigram:
            # return the index array of the bigram
            bigramIndices = FindWord(sourceText, bigram)
    
    # Now, if any of the word indices match any of the bigram indices, replace 
    # those in the index list.
    if len(bigramIndices) > 0:
        for bigramIndex in bigramIndices:
            None
            for n,wordIndex in enumerate(wordIndices):
                None
                # we only need to know if one of the indexes matches in the bigram
                # index.
                if wordIndex[0] in bigramIndex:
                    wordIndices[n] = bigramIndex
    
    return wordIndices

                
            
            
            
        




