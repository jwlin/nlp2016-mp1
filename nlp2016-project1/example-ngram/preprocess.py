#!/usr/bin/env python3
import sys
import argparse
import re

#import nltk

candidate = { i:'EMOTICON_+'+str(i) for i in range(1,41) }
punc_to_blank = list()
with open('punctuation-to-blank.txt', 'r') as f:
    for line in f:
        punc_to_blank.append(line.replace('\n', ''))
punc_to_empty = list()
with open('punctuation-to-empty.txt', 'r') as f:
    for line in f:
        punc_to_empty.append(line.replace('\n', ''))

rword = dict()
with open('replace_words.txt', 'r') as f:
    for line in f:
        line = line.replace('\n', '')
        line = line.split(' ')
        rword[line[0]] = line[1]

def load_dataset(infile, transform=None, tokenizer=None):
    for line in infile:
        rid, emot, text = line.strip().split('\t', maxsplit=2)
        if tokenizer:
            #text = HanziConv.toSimplified(text)
            text = HanziConv.toTraditional(text)
            #text = list( w for w in tokenizer.cut(sanitize(text)) if w != ' ' )
            new_text = list()
            word = ''
            for w in sanitize(text):
                if w == ' ':
                    if word:
                        new_text.append(word)
                        word = ''
                elif isEnglish(w):
                    word += w
                else:
                    if word:
                        new_text.append(word)
                        word = ''
                    new_text.append(w)
            if word:
                new_text.append(word)
            text = new_text
            try:
                pos  = text.index('EMOTICON')
                if transform:
                    text[pos] = candidate[int(emot)]

                yield rid, text, pos
            except ValueError: # no EMOTICON
                print("oops, sent #{} no emoticon!".format(rid), file=stderr)
        else:
            yield rid, text

def sanitize(text):
    # keep only Chinese/Korean/Japanese chars, a-zA-Z0-9 and spaces
    #print(text)
    expr = re.compile(r'[^\u2E80-\u9FFF\s\w]')
    text = re.sub(expr, ' ', text)
    text = re.sub(r'(\s)+', ' ', text)
    for p in punc_to_blank:
        text = text.replace(p, ' ')
    for p in punc_to_empty:
        text = text.replace(p, '')
    for k, v in rword.items():
        text = text.replace(k, v)
    return text


def isEnglish(s):
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True


if __name__ == '__main__':

    import jieba
    import jieba.posseg
    from hanziconv import HanziConv
    tokenizer = jieba.Tokenizer(dictionary='dict.txt.big')
    #tokenizer = jieba.Tokenizer()
    tokenizer.tmp_dir = "."
    
    if len(sys.argv) > 1:
        for rid, text, pos in load_dataset(sys.stdin, transform=False, tokenizer=tokenizer):
            for cand, cand_string in sorted(candidate.items()):
                text[pos] = cand_string
                print(' '.join(text))
    else:
        for rid, text, pos in load_dataset(sys.stdin, transform=True, tokenizer=tokenizer):
            print(' '.join(text))

