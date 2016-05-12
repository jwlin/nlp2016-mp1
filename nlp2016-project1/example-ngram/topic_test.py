import os
import jieba
jieba.load_userdict('dict.txt.big')
import time
import json
from gensim import corpora, models, similarities
from preprocess import sanitize


with open('stop_words.txt', 'r') as f:
    stopwords = list()
    for line in f:
        stopwords.append(line.split()[0])
    stopwords.append(' ')
    stopwords.append('EMOTICON')


def main():
    t_start = time.time()
    if os.path.exists('testing_corpus.json'):
        with open('testing_corpus.json', 'r') as f:
            testing_corpus_data = json.load(f)
    else:
        testing_corpus_data = {}
    with open('../test.tsv', 'r') as f:
        index = 0
        for line in f:
            rid, emot, text = line.strip().split('\t', maxsplit=2)
            #print('raw:', rid, emot, text)
            print(rid)
            if rid in testing_corpus_data.keys():
                doc = testing_corpus_data[rid]['feature']
            else:
                doc = list( w for w in jieba.cut(sanitize(text)) if w not in stopwords)
                testing_corpus_data[rid] = dict()
                testing_corpus_data[rid]['feature'] = doc
            testing_corpus_data[rid]['emot'] = []
            testing_corpus_data[rid]['index'] = index
            #print('sanitized:', doc)
            index += 1
    t_end = time.time()
    print('time elapsed for building corpus: %f minutes' % ((t_end-t_start)/60.0))
    with open('testing_corpus.json', "w") as f:
        json.dump(testing_corpus_data, f, indent=2, ensure_ascii=False, sort_keys=True)

    print('Inferring')
    dictionary = corpora.Dictionary.load('train.dict')
    corpus_bow = corpora.MmCorpus('train.mm')
    tfidf = models.TfidfModel.load('train.tfidf')
    lsi = models.LsiModel.load('train.lsi')
    #lda = models.ldamodel.LdaModel.load('train.lda')
    index = similarities.MatrixSimilarity.load('train.index')
	
    with open('training_corpus.json', 'r') as f:
        training_corpus_data = json.load(f)
    
    '''
    training_corpus = list()
    with open('top50.txt') as f:
        for line in f:
            line = line.replace('\n', '')
            line = line.split('\t')
            training_corpus.append(line)
    '''
    c=0
    for testing_id in testing_corpus_data.keys():
        #print(testing_id, testing_corpus_data[testing_id]['feature'])
        vec_bow = dictionary.doc2bow(testing_corpus_data[testing_id]['feature'])
        vec_tfidf = tfidf[vec_bow]
        vec_lsi = lsi[vec_tfidf]  # convert the query to LSI space
        sims = index[vec_lsi]  # perform a similarity query against the corpus
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        #print(sims)
        top3 = [ele[0] for ele in sims[:3]]
        print('top 6:', sims[:6])
        for training_index in top3:
            for training_id in training_corpus_data.keys():
                if training_corpus_data[training_id]['index'] == training_index:
                    #print(training_corpus_data[training_id]['feature'])
                    testing_corpus_data[testing_id]['emot'].append(training_corpus_data[training_id]['emot'])
                    break
            #testing_corpus_data[testing_id]['emot'].append(training_corpus[training_index][0])
            #print(testing_corpus_data[testing_id]['feature'])
            #print(training_corpus[training_index])
        print(c)
        #input()
        c+=1
    with open('testing_corpus.json', "w") as f:
        json.dump(testing_corpus_data, f, indent=2, ensure_ascii=False, sort_keys=True)

    with open('prediction.csv', 'a') as pf:
        pf.write('Id,Emoticon\n')
        with open('../test.tsv') as f:
            for line in f:
                rid, emot, text = line.strip().split('\t', maxsplit=2)
                pf.write('{rid},{prediction}\n'.format(rid=rid, prediction=" ".join(testing_corpus_data[rid]['emot'])))


if __name__ == '__main__':
    main()
