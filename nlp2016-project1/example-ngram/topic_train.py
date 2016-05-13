import os
import jieba
import jieba.posseg as pseg
jieba.load_userdict('dict.txt.big')
import time
import json
from gensim import corpora, models, similarities
from preprocess import sanitize


def main():
    t_start = time.time()
    if os.path.exists('training_corpus.json'):
        with open('training_corpus.json', 'r') as f:
            training_corpus_data = json.load(f)
    else:
        training_corpus_data = {}
    training_corpus = []
    with open('../train.tsv', 'r') as f:
        index = 0
        for line in f:
            rid, emot, text = line.strip().split('\t', maxsplit=2)
            print('raw:', rid, emot, text)
            if rid in training_corpus_data.keys():
                doc = training_corpus_data[rid]['feature']
            else:
                #doc = splitWord(text)
                doc = list( w for w in jieba.cut(sanitize(text)) if w not in [' ', 'EMOTICON'] )
                training_corpus_data[rid] = dict()
                training_corpus_data[rid]['feature'] = doc
            training_corpus_data[rid]['index'] = index
            training_corpus_data[rid]['emot'] = emot
            training_corpus.append(doc)
            print('sanitized:', doc)
            index += 1
    t_end = time.time()
    print('time elapsed for building corpus: %f minutes' % ((t_end-t_start)/60.0))
    with open('training_corpus.json', "w") as f:
        json.dump(training_corpus_data, f, indent=2, ensure_ascii=False, sort_keys=True)
    
    '''
    training_corpus = list()
    with open('top50.txt') as f:
        for line in f:
            line = line.replace('\n', '')
            line = line.split('\t')[2:]
            training_corpus.append(line)
    '''
    
    dictionary = corpora.Dictionary(training_corpus)
    stoplist = [line.lower().split()[0] for line in open('stop_words.txt', 'r')]
    # remove stop words and words that appear only once
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
    #once_ids = []
    dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    #print(dictionary)
    dictionary.save('train.dict')  # store the dictionary, for future reference
    
    corpus_bow = [dictionary.doc2bow(doc) for doc in training_corpus]
    corpora.MmCorpus.serialize('train.mm', corpus_bow) # store to disk, for later use
    
    tfidf = models.TfidfModel(corpus_bow) # initialize (train) a model
    tfidf.save('train.tfidf')
    corpus_tfidf = tfidf[corpus_bow]
    
    #lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, alpha='auto', num_topics=100)
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)
    lsi.save('train.lsi')
    #print(lsi.print_topics(300))
    corpus_lsi = lsi[corpus_tfidf]
    index = similarities.MatrixSimilarity(corpus_lsi)  # transform corpus to LSI space and index it
    index.save('train.index')
    

def splitWord(raw_doc):
    doc = []
    raw_doc = sanitize(raw_doc)
    for word, flag in pseg.cut(raw_doc):
        #if(flag in ['n', 'nr', 'ns', 'nt', 'nz', 'v', 'a', 'd', 'eng']) and (len(word)>1):
        if flag in ['n', 'nr', 'ns', 'nt', 'nz', 'v', 'a', 'd', 'eng']:
            if word != 'EMOTICON':
                doc.append(word)
    return doc


if __name__ == '__main__':
    main()
