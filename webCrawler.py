"""

Example webcrawler or 'spider' code.   This spider integrates both of the code routines provided including:

PorterStemmer - implements a porter stemmer. 

BeautifulSoup -  is a python module allowing text to be read from a html page. 
                 returns the text of the html page with all of the HTML tags
and other formatting removed making providing a simple string containing the contents of a web page
that can be parsed and indexed by our indexer code.  
"""
import sys, os, re

# import urllib2

import urllib.request
# import requests
# import urlparse
import urllib.parse
import sqlite3
import math
import time
# from BeautifulSoup4 import BeautifulSoup4, NavigableString
import bs4
# from bs4 import beautifulsoup
import nltk

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

stopwords = ['the', 'of', 'and', 'to', 'in', 'you', 'it', 'with', 'that', 'or', 'was', 'he', 'is', 'for', 'this', 'his', 'as', 'not', 'at', 'by', 'all', 'they', 'but', 'be', 'on', 'from', 'had', 'her', 'work', 'are', 'any', 'she', 'if', 'said', 'so', 'which', 'have', 'do', 'we', 'no', 'my', 'were', 'them', 'their', 'him', 'one', 'will', 'me', 'there', 'who', 'up', 'other', 'an', 'its', 'when', 'what', 'can', 'may', 'into', 'out', 'must', 'your', 'then', 'would', 'could', 'more', 'now', 'has', 'like', 'down', 'where', 'been', 'through', 'did', 'away', 'these', 'such', 'set', 'back', 'some', 'than', 'way', 'made', 'our', 'after', 'well', 'should', 'get', 'even', 'am', 'go', 'saw', 'just', 'put', 'while', 'ever', 'off', 'here', 'also']

# regular expression for: extract words, extract ID from path, check for hexa value
chars = re.compile(r'\W+')
pattid= re.compile(r'(\d{3})/(\d{3})/(\d{3})')


# the higher ID
tokens = 0
documents = 0
terms = 0

#
# We will create a term object for each unique instance of a term
#
class Term():
        termid = 0
        termfreq = 0
        docs = 0
        docids = {}

# split on any chars
def splitchars(line) :
        return chars.split(line)

def stripTags(s): 
    intag = False
    s2 = ""    
    for c in s:
        if c == '<':
            intag = True
        elif c == '>':
            intag = False
        if intag != True:
            s2 = s2+c      
    return(s2)

def printText(tags):
        for tag in tags:
                if tag.__class__ == bs4.element.NavigableString:
                        print(tag)
                else:
                        printText(tag)
        print("tag:%d"%tag)


# process the tokens of the source code
def parsetoken(db, line):
        global documents
        global tokens
        global terms
        #
        # Create instance of the porterstemmer object we will call the stemmer method in this
        # object to 'stem' the tokens extracted from the line.
        #
        p = PorterStemmer()

        # this replaces any tab characters with a space character in the line
        # read from the file
        line = line.replace('\t',' ')
        line = line.strip()

        #
        # This routine splits the contents of the line into tokens
        l = splitchars(line)
        print("l:%i"%l)

        # for each token in the line process 
        for elmt in l:
                # This statement removes the newline character if found 
                elmt = elmt.replace('\n','')

                # This statement converts all letters to lower case
                lowerElmt = elmt.lower().strip()
                print("lower Element %i " %lowerElmt)

                #
                # Increment the counter of the number of tokens processed.  This value will
                # provide the total size of the corpus in terms of the number of terms in the
                # entire collection
                #
                tokens += 1

                # if the token is less than 2 characters in length we assume
                # that it is not a valid term and ignore it
                #
                if len(lowerElmt) <2:
                        continue

                #
                # if the token is in the stopwords list then do not include in the term
                # dictionary and do not index the term.
                #
                if (lowerElmt in stopwords):
                        continue

                #
                # This section of code will check to see if the term is a number and will not
                # add a number to the index.  This is accomplished by attempting to convert
                # the term into an integer and assigning it to a variable.  If the term is not
                # a number meaning it contains non numeric characters this will fail and we can
                # catch this error and continue processing the term.  If the term is a number
                # it will not fail and we can then ignore the term (the continue statement will
                # continue with the next item retrieved from the 'for' statement)
                #
                try:
                    dummy = int(lowerElmt)               
                except ValueError:
                        # Value is not a number so we can index it
                        stemword = lowerElmt 
                else:
                        # value is a number so we will NOT add it to the index
                        continue

                #
                # In this following short section of the code we call the porter stemmer code
                # that we have included in our indexer process.  This algorithm will stem the
                # the tokens which will reduce the size of our data dictionary. 
                #
                lowerElmt = p.stem(stemword, 0,len(stemword)-1)

                # if the term doesn't currently exist in the term dictionary
                # then add the term 
                if not (lowerElmt in db.keys()):
                        terms+=1
                        db[lowerElmt] = Term()
                        db[lowerElmt].termid = terms
                        db[lowerElmt].docids = dict()
                        db[lowerElmt].docs = 0
                  
                # if the document is not currently in the postings
                # list for the term then add it
                #
                if not (documents in db[lowerElmt].docids.keys()):
                        db[lowerElmt].docs += 1
                        db[lowerElmt].docids[documents] = 0
                        
                # Increment the counter that tracks the term frequency 
                db[lowerElmt].docids[documents] += 1
        return l

#
#  Create the inverted index tables.
#
#  Insert a row into the TermDictionary for each unique term along with a termid which is
#  a integer assigned to each term by incrementing an integer
#
#  Insert a row into the posting table for each unique combination of Docid and termid
#        
def writeindex(db):        
        for k in db.keys():
                cur.execute('insert into TermDictionary values (?,?)', (k, db[k].termid))
                docfreq = db[k].docs
                ratio = float(documents) / float(docfreq)
                idf = math.log10(ratio)

                for i in db[k].docids.keys():
                        termfreq = db[k].docids[i]
                        tfidf = float(termfreq) * float(idf)
                        if tfidf > 0:
                                cur.execute('insert into Posting values (?, ?, ?, ?, ?)', (db[k].termid, i, tfidf, docfreq, termfreq))




if __name__ == '__main__':

    #
    # Get the starting URL to crawl
    #
    line = input("Enter URL to crawl (must be in the form http://www.domain.com): ")
 
    # r  = requests.get("http://" +line)

    # data = r.text
    # print("data: %i"%data)f
 
    # the database is a simple dictionnary 
    db = {'keys':'djjdjdjdd', 'termid':'bac21', 'term':'community'}
    #(DocumentName text, DocId
    #Posting (TermId int, DocId int, tfidf real, docfreq int, termfreq int)
    #TermDictionary (Term text, TermId int)
    #DocumentDictionary (DocumentName text, DocId int)
 
    #
    # Capture the start time of the routine so that we can determine the total running
    # time required to process the corpus
    #
    t2 = time.localtime()   
    print('Start Time: %.2d:%.2d' % (t2.tm_hour, t2.tm_min))
    
    #
    # Create a sqlite database to hold the inverted index.  The isolation_level statment turns
    # on autocommit which means that changes made in the database are committed automatically
    #
    #   con = sqlite3.connect("c:\webcrawler.db")
    con = sqlite3.connect("/Data/SourceCode/infoRetrieval/indexer_part2.db")
    con.isolation_level = None
    cur = con.cursor()

    #
    # In the following section three tables and their associated indexes will be created.
    # Before we create the table or index we will attempt to drop any existing tables in
    # case they exist
    #
    # Document Dictionary Table 
    cur.execute("drop table if exists DocumentDictionary")
    cur.execute("drop index if exists idxDocumentDictionary")
    cur.execute("create table if not exists DocumentDictionary (DocumentName text, DocId int)")
    cur.execute("create index if not exists idxDocumentDictionary on DocumentDictionary (DocId)")

    # Term Dictionary Table 
    cur.execute("drop table if exists TermDictionary")
    cur.execute("drop index if exists idxTermDictionary")
    cur.execute("create table if not exists TermDictionary (Term text, TermId int)")
    cur.execute("create index if not exists idxTermDictionary on TermDictionary (TermId)")
        
    # Postings Table
    cur.execute("drop table if exists Posting")
    cur.execute("drop index if exists idxPosting1")
    cur.execute("drop index if exists idxPosting2")
    cur.execute("create table if not exists Posting (TermId int, DocId int, tfidf real, docfreq int, termfreq int)")
    cur.execute("create index if not exists idxPosting1 on Posting (TermId)")
    cur.execute("create index if not exists idxPosting2 on Posting (Docid)")

    #
    # Initialize variables  
    #
    crawled = ([])              # contains the list of pages that have already been crawled
    tocrawl = [line]            # contains the queue of url's that will be crawled
    links_queue = 0             # counts the number of links in the queue to limit the depth of the crawl
    crawlcomplete = True        # Flat that will exit the while loop when the craw is finished
    #
    # Crawl the starting web page and links in the web page up to the limit.
    #
    while crawlcomplete:

        #
        # Pop the top url off of the queue and process it. 
        #
        try:
                crawling = tocrawl.pop()
                #print("test:"
        except:
                crawlcomplete = False
                continue

        l = len(crawling)
        print("L:%.2d" %l)
        ext = crawling[l-4:l]
        if ext in ['.pdf', '.png', '.jpg', '.gif', '.asp']:
                crawled.append(crawling)
                continue
        
        #
        # Print the current length of the queue of URL's to crawl
        #
        print("URL")
        print(len(tocrawl),crawling)

        #
        # Parse the URL and open it.
        #
        url = urllib.parse.urlparse(crawling)
        try:
            response = urllib.request.urlopen(crawling).read()
        except:
            continue
        
        #
        # Use BeautifulSoup modules to format web page as text that can
        # be parsed and indexed
        #
        soup = bs4.BeautifulSoup(response)
        tok = "".join(soup.findAll("p", text=re.compile(".")))
        # pass the text extracted from the web page to the parsetoken routine for indexing
        parsetoken(db, tok)
        documents += 1
       

        #
        # For each unique instance of a document assign a document id (documents) and store in the documentdictionary
        #
        cur.execute("insert into DocumentDictionary values (?, ?)", (documents, crawling))
                     
        #
        # Find all of the weblinks on the page put them in the stack to crawl through
        #
        if links_queue < 500:
                links = re.findall('''href=["'](.[^"']+)["']''', response, re.I)

                for link in (links.pop(0) for _ in xrange(len(links))):
                    if link.startswith('/'):
                        link = 'http://' + url[1] + link
                    elif link.startswith('#'):
                        link = 'http://' + url[1] + url[2] + link
                    elif not link.startswith('http'):
                        link = 'http://' + url[1] + '/' + link
                    if link not in crawled:
                        links_queue += 1
                        tocrawl.append(link)
        crawled.append(crawling)
    print("Links_queue %i" %links_queue)
    #
    # Display the time that the indexing process is complete, and the process of writing
    #
    t2 = time.localtime()   
    print('Indexing Complete, write to disk: %.2d:%.2d' % (t2.tm_hour, t2.tm_min))

    #
    # Write the inverted index to disk
    #
    writeindex(db)

    #
    # Commit and close the database 
    #
    con.commit()
    con.close()

    #
    # Print processing statistics
    # Documents - every document opened and read by the indexer
    # Terms - each token that was extracted from the file. 
    #
    print("Documents %i" % documents)
    print("Terms %i" % terms)
    print("Tokens %i" % tokens)
    t2 = time.localtime()   
    print('End Time: %.2d:%.2d' % (t2.tm_hour, t2.tm_min))
