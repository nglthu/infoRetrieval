# Index

[Biword Index](https://github.com/nglthu/infoRetrieval/wiki/Biword-index)

[Phrase Index](https://github.com/nglthu/infoRetrieval/wiki/phrase-index)

[Positional Index](https://github.com/nglthu/infoRetrieval/wiki/Positional-Index-vs-Inverted-Index#positional-index)

[Inverted Index](https://github.com/nglthu/infoRetrieval/wiki/Positional-Index-vs-Inverted-Index#inverted-index)

[Positional Index vs Inverted index](https://github.com/nglthu/infoRetrieval/wiki/Positional-Index-vs-Inverted-Index)

# Inverse Document Frequency
[Detail](https://github.com/nglthu/infoRetrieval/wiki/Inverse-Document-Frequency)

# Features of an inverted index.
## Key concept of index

1. Traversing a directory of documents
2. Reading the document and extracting and tokenizing all of the text
3. Computing counts of documents and terms
4. Building a dictionary of unique terms that exist within the corpus
5. Writing out to a disk file, a sorted term dictionary

## Inverted Index Construction
[Model](https://github.com/nglthu/infoRetrieval/wiki/Inverted-Index-Construction#inverted-index-construction)

+ Select doc, 
+ tokenize, 
+ add to dictionary, 
+ count occurrences, 
+ sort for searching.

## Report
### documents, terms, unique terms

![alt text](https://github.com/nglthu/infoRetrieval/blob/master/img/processingTime.png)

1. Number of documents processed

2. Total number of terms parsed from all documents

3. Total number of unique terms found and added to the index

### documents

[here](https://github.com/nglthu/infoRetrieval/blob/master/cacm/documents.dat)

### index

[here](https://github.com/nglthu/infoRetrieval/blob/master/cacm/index.dat)

# Map-reduce

Implementation of hadoop
Search technology
Simple db keeping track of dictionary

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


## Alogrithm
+ Take all output, combine and reduce them
+ Map (key=url, val=contents):
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

e.g. finding hello &rightarrow; hello$, ello$h, lo$hel, o$hell
execute different kind of search. 

Cons: increase number of term in the dictionary

##	Permuterm query processing
+ rotate query wild-card to the right
+ use B-tree lookup
+ Permuterm problem : = quadruples lexicon size

Pros: use a lot more space for indexes

##	Bigram (k-gram) indexes
Finds term based on a query consisting of k-grams

# Index Compression

## Key Terms

1. Dictionary compression
```
Aims to fit in the memory with an at least large portion of dictionaries. 

The dictionary as a string that sorts the vocabulary lexicographically and stores it in an array of fixed-width entries or blocked storage by grouping terms into the string into blocks of size k and keeping a term pointer for the first term of each blog
```
2. Rule of 30
```
The 30 most common words account for 30% of the tokens in the written text. 

Thus, the lossy method could be used for compression without losing its effectiveness in encoding the data.
```

3. Lossy Compression
```
Amount of data is lost during this process
```

4. Lossless Compression
```
No data is lost during compression
```

5. Heap’s law
```
 To estimate the number of unique terms in a collection based upon constants k and b and the number of terms or tokens (T) parsed from all documents.

  M = kT<sup>ß</sup>
  
  in which T is the number of tokens in a collection, k and ß are parameters values
```
![alt text](https://github.com/nglthu/infoRetrieval/blob/master/Heap_law/sizeOfM.png)

6. Zipf’s law
```
cfi = ci<sup>k</sup> as one of the types of the power law
```
7. Power law

8. Front Coding

9. Variable Byte Encoding

10. Nibble

11. Unary Code
```
A string of n 1s followed by a 0
```
12. Encoding
```
Two type of methods such as bytewise and bitwise. 

As such variable byte encoding uses the integral number of byte to encode a gap instead of docID. 
```

13. Entropy

14. δ Codes
```
Asymptotically optimal for entropy H(P) → ∞
```

# Web crawler

##	What is involved in creating a web crawler?  
Purpose: to get the information that is available on a website
Process: As described by Manning (2009, chapter 15)
+ Begin with URL(s) constituting a seed set
+ Picking a URL from this seed set then fetches the web page at that URL
+ Parse the fetched page to extract links and texts
+ Feed the extracted texts to a text indexer
+ Add the extracted links to URL frontier
+ Corresponding pages-URL(s) are fetched by the crawler
+ URL frontier contains seed set
+ Corresponding URL are deleted from URL frontier when pages are fetched.
+ Entire process as traversing the web graph
 
 ![alt text](https://github.com/nglthu/infoRetrieval/blob/master/img/basicCrawlerArchitecture.png)

Figure : The basic crawler architecture extracted from Figure 20.1 (Manning, 2009, chapter 19)

## Static vs dynamic web content

Static: the same prebuilt content each time the page is loaded
Dynamic: content is changed and can be generated on the fly. 

# Query

[Query Type](https://github.com/nglthu/infoRetrieval/wiki/Query-in-Information-Retrieval-(IR)#type-of-query-to-use)

[Boolean Retrieval vs Wildcard Queries vs Phrase Queries](https://github.com/nglthu/infoRetrieval/wiki/Query-in-Information-Retrieval-(IR)#the-differences-between-boolean-retrieval-wildcard-queries-and-phrase-queries)

[Improve of Computing Score and Rank](https://github.com/nglthu/infoRetrieval/wiki/Query-in-Information-Retrieval-(IR)#some-techniques-that-can-improve-the-efficiency-of-computing-scoring-and-ranking-in-search-systems)

# References: 
Manning, C.D., Raghaven, P., & Schütze, H. (2009). An Introduction to Information Retrieval (Online ed.). Cambridge, MA: Cambridge University Press. Available at http://nlp.stanford.edu/IR-book/information-retrieval-book.html 

