
#  Example code in python programming language demonstrating some of the features of an inverted index.

#  In this example, we scan a directory containing the corpus of files. (In this case the documents are reports on articles

#  and authors submitted to the Journal "Communications of the Association for Computing Machinery" 

#  In this example we see each file being read, tokenized (each word or term is extracted) combined into a sorted

#  list of unique terms. 

#  We also see the creation of a documents dictionary containing each document in sorted form with an index assigned to it.

#  Each unique term is written out into a terms dictionary in sorted order with an index number assigned for each term. 

#  From our readings we know that to complete teh inverted index all that we need to do is create a third file that will

#  coorelate each term with the list of documents that it was extracted from.  We will do that in a later assignment.

#  We can further develop this example by keeping a reference for each term of the documents that it came from and by

#  developing a list of the documents thus creating the term and document dictionaries.

#  As you work with this example, think about how you might enhance it to assign a unique index number to each term and to

#  each document and how you might create a data structure that links the term index with the document index.

 

 

import sys,os,re

import time

 

# define global variables used as counters

tokens = 0

documents = 0

terms = 0

termindex = 0

docindex = 0

 

# initialize list variable

alltokens = []

alldocs = []


# Capture the start time of the routine so that we can determine the total running

# time required to process the corpus

t2 = time.localtime()  

 

 

# set the name of the directory for the corpus


dirname = "c:\users\datai\cacm"

 

# For each document in the directory read the document into a string


all = [f for f in os.listdir(dirname)]

for f in all:

    documents+=1

    with open(dirname+'/'+f, 'r') as myfile:

        alldocs.append(f)

        data=myfile.read().replace('\n', '') 

        for token in data.split():

            alltokens.append(token)

                    tokens+=1

 

 

# Open for write a file for the document dictionary


documentfile = open(dirname+'/'+'documents.dat', 'w')

alldocs.sort()

for f in alldocs:

  docindex += 1

  documentfile.write(f+','+str(docindex)+os.linesep)

documentfile.close()

 

# Sort the tokens in the list

alltokens.sort()



# Define a list for the unique terms 

g=[]

 

# Identify unique terms in the corpus

for i in alltokens:   

    if i not in g:

       g.append(i)

       terms+=1

 

terms = len(g)

 

# Output Index to disk file. As part of this process we assign an 'index' number to each unique term. 


indexfile = open(dirname+'/'+'index.dat', 'w')

for i in g:

  termindex += 1

  indexfile.write(i+','+str(termindex)+os.linesep)

indexfile.close()
 

 

# Print metrics on corpus


print 'Processing Start Time: %.2d:%.2d' % (t2.tm_hour, t2.tm_min)

print "Documents %i" % documents

print "Tokens %i" % tokens

print "Terms %i" % terms

 

t2 = time.localtime()  

print 'Processing End Time: %.2d:%.2d' % (t2.tm_hour, t2.tm_min)
