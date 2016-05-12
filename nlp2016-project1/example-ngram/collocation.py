#!/usr/bin/env python3
import sys
import time
import json
import os
import math
from preprocess import load_dataset

def add_term(term, data_dict):
    if term not in data_dict.keys():
        data_dict[term] = 1
    else:
        data_dict[term] += 1
    return data_dict


def log_comb(n, r):
    # nCr = n! / (n-r)! * r! = n*(n-1)*...*(r+1) / 1*2*3*...*r
    tmp = 0.0
    for i in range(r+1, n+1):
        tmp += math.log(i)
    for i in range(1, r+1):
        tmp -= math.log(i)
    return tmp


def calculate_L(n, c1, c2, c12):
    p = c2 / float(n)
    p1 = c12 / float(c1)
    p2 = (c2-c12) / float(n-c1)
    
    if c1 == c12 or c2 == c12:  # p1=1 (1-p1=0) or p2=0 (1-p2=1) --> L_h2 = 0 --> L = -infinite
        return -99999
    
    L_h1 = log_comb(c1, c12) + (c12*math.log(p)) + ((c1-c12)*math.log(1-p)) + log_comb(n-c1, c2-c12) + ((c2-c12)*math.log(p)) + ((n-c1-c2+c12)*math.log(1-p))
    L_h2 = log_comb(c1, c12) + (c12*math.log(p1)) + ((c1-c12)*math.log(1-p1)) + log_comb(n-c1, c2-c12) + ((c2-c12)*math.log(p2)) + ((n-c1-c2+c12)*math.log(1-p2))
    return (-2)*(L_h1 - L_h2)


if __name__ == '__main__':
    import jieba
    tokenizer = jieba.Tokenizer(dictionary='dict.txt.big')
    tokenizer.tmp_dir = "."
    
    emot_dict = dict()
    stat = dict()
    offset = 5
    t_start = time.time()
    if os.path.exists('collocation.json') and os.path.exists('term_stat.json'):
        with open('collocation.json', 'r') as f:
            emot_dict = json.load(f)
        with open('term_stat.json', 'r') as f:
            stat = json.load(f)
    else:
        for rid, text, pos in load_dataset(sys.stdin, transform=True, tokenizer=tokenizer):
            print(rid)            
            # stat
            emot = text[pos]
            for t in text:
                add_term(t, stat)
            # collocation
            left = pos-offset if pos-offset >= 0 else 0
            right = pos+offset if pos+offset <= len(text)-1 else len(text)-1
            if emot not in emot_dict.keys():
                emot_dict[emot] = dict()
            for t in text[left:right+1]:
                #print(t)
                if t != emot:
                    add_term(t, emot_dict[emot])            
            #print('---')
        with open('collocation.json', 'w') as f:
            json.dump(emot_dict, f, indent=2, ensure_ascii=False, sort_keys=True)
        with open('term_stat.json', 'w') as f:
            json.dump(stat, f, indent=2, ensure_ascii=False, sort_keys=True)

    t_end = time.time()
    print('time elapsed for scanning corpus: %f minutes' % ((t_end-t_start)/60.0))

    # post process
    n = 0
    for k, v in stat.items():
        n += v
    #print(n)

    # count likelyhood ratio
    lr_data = dict()
    if os.path.exists('collocation_lr.json'):
        with open('collocation_lr.json', 'r') as f:
            lr_data = json.load(f)
    
    for emot, v_dict in emot_dict.items():
        print(emot)
        if emot not in lr_data.keys():
            lr_data[emot] = dict()
        
        term_list = list()
        for term, count in v_dict.items():
            if count > 4:
                term_list.append((term, count))
        #term_list = sorted(term_list, key=lambda x:-x[1])
        
        total = len(term_list)
        #term_list_with_L = list()
        i = 1
        for term, count in term_list:
            if term not in lr_data[emot].keys():
                # count likelyhood ratio: w1=term, w2=emoticon
                c1 = stat[term]
                c2 = stat[emot]
                c12 = count
                lr = calculate_L(n, c1, c2, c12) + calculate_L(n, c2, c1, c12)
                #print(term, count, lr)
                #term_list_with_L.append((term, count, lr))
                lr_data[emot][term] = lr            
            print('%d/%d' %(i, total))
            i += 1
        with open('collocation_lr.json', 'w') as f:
            json.dump(lr_data, f, indent=2, ensure_ascii=False, sort_keys=True)

