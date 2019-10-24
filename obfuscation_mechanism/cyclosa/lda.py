""" This file for train a lda model in wiki data
1. First, download the dump of all Wikipedia articles from http://download.wikimedia.org/enwiki/ 
(you want the file enwiki-latest-pagesarticles.xml.bz2, or enwiki-YYYYMMDD-pages-articles.xml.bz2 for date-specific dumps). 

2. Convert the articles to plain text (process Wiki markup) and store the result as sparse TF-IDF vectors. 
In Python, this is easy to do on-the-fly and we don’t even need to uncompress the whole archive to disk. 
There is a script included in gensim that does just that, run:
$ python -m gensim.scripts.make_wiki


"""


from gensim.test.utils import datapath
import gensim
import pdb

# load id->word mapping (the dictionary), one of the results of step 2 above
id2word = gensim.corpora.Dictionary.load_from_text('wiki/_wordids.txt.bz2')
# load corpus iterator
mm = gensim.corpora.MmCorpus('wiki/_tfidf.mm')

lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=100, update_every=1, passes=1)

#lda.save(save_file)
save_file = datapath("/hdd/OB-WSPES_git/obfuscation_mechanism/cyclosa/lda_model/lda")
lda.save(save_file)


#--------------------------------------------------
#   test 
#--------------------------------------------------
lda = gensim.models.ldamodel.LdaModel.load(save_file)
other_texts = [
    ['computer', 'time', 'graph'],
    ['survey', 'response', 'eps'],
    ['human', 'system', 'computer']
    ]
query_doc = [id2word.doc2bow(text) for text in other_texts]
unseen_doce = query_doc[0]
#pdb.set_trace()
print(unseen_doce)
vector = lda[unseen_doce]
print(vector)


#pdb.set_trace()