# Features of an inverted index.
## Key concept of index

1. Traversing a directory of documents
2. Reading the document and extracting and tokenizing all of the text
3. Computing counts of documents and terms
4. Building a dictionary of unique terms that exist within the corpus
5. Writing out to a disk file, a sorted term dictionary

## Report

1. Number of documents processed

2. Total number of terms parsed from all documents

3. Total number of unique terms found and added to the index


# Map-reduce

Implementation of hadoop
Search technology
Simple db keeping track of dictionary
## Index construction:
+ Select doc, 
+ tokenize, 
+ add to dictionary, 
+ count occurrences, 
+ sort for searching.

## Problem:

+ Both memory and time consuming at internet scale
+ Potentially billions of documents
+ Need more efficient solution
e.g. : document of (see bob run see spot throw)
+ count term: in order to reduce by combine and summerize
```
see 2
bob 1
spot 1
throw 1
```
+ key every term then count
+ Then merge each output toghether
+ Then sort them


### alogrithm
Take all output, combine and reduce them
Map (key=url, val=contents):
For each word w in contents, emit (w, "1")
Reduce(key=word, values=uniq_counts):
Sum all "1"s in value list
Emit result "(word, sum)"

# DFS : data file system
Automatic parallel execution in mapReduce
MapReduce in Hadoop
 
# Dictionary Data Structures
+ To store the term vocabulary, 
+ document frequency, 
+ pointers to each postings list

![alt text](https://github.com/nglthu/infoRetrieval/blob/master/img/nativeDic.png)

Example: An array of struct as a naïve dictionary


## options for dictionary structure:
+ Hashtables
```
Each vocabulary term is hashed to an interger
Pros: faster lookup than tree
Cons: no easy way to find minor variants; no prefix search; expensive operation of rehasing.
```
+ Trees
```
Simplest: Binary tree
More usual: B-trees
Pros: solves the prefix problem
Cons: 
+ Slower O(logM)
+ Rebalancing binary tree is expensive, but B-trees mitigate the rebalancing problem.
```
e.g. binary tree in sort order
 
![alt text](https://github.com/nglthu/infoRetrieval/blob/master/img/binaryTree.png)

Always slipping into half for searching. 

Every node always has two outputs

e.g. B-Tree

 
![alt text](https://github.com/nglthu/infoRetrieval/blob/master/img/BTree.png)

every node has a number of children

 
Any particular level may have two or more outcomes.
Level multiple options.

#	Tolerant Retrieval
##	Wild-card queries

e.g. *mon: fine words ending with mon

##	Query processing

+ Find everything that maches with term
e.g Find word related to home: home*
+ This result in the execution of many Boolean and queries
e.g. home* AND house*
+ Handle wildcard:
```
B-trees handle * at the end of query
Permuterm index: handle * at the middle
```

e.g. finding hello-> hello$, ello$h, lo$hel, o$hell
execute different kind of search. 

Cons: increase number of term in the dictionary

##	Permuterm query processing
+ rotate query wild-card to the right
+ use B-tree lookup
+ Permuterm problem : = quadruples lexicon size

Pros: use a lot more space for indexes

##	Bigram (k-gram) indexes
Finds term based on a query consisting of k-grams

