import json

with open('collocation.json', 'r') as f:
    emot_dict = json.load(f)

with open('collocation_lr.json', 'r') as f:
    lr_data = json.load(f)

stoplist = [line.lower().split()[0] for line in open('stop_words.txt', 'r')]
stoplist += ['喔', '啦', '很', '我', '你', '唷', '囉', 'ㄉ', 'ㄌ', '呢', '真是','吧', '也', '阿', '啊', '真的', '在', '又', 'ㄚ','哦','他']

data = dict()
for emot, v_dict in emot_dict.items():
    term_list = list()
    for term, count in v_dict.items():
        if count > 4:
            term_list.append((term, count))
    term_list = sorted(term_list, key=lambda x:-x[1])
    data[emot] = dict()
    data[emot]['freq'] = term_list[:10]
for emot, v_dict in lr_data.items():
    term_list = list()
    for term, lr in v_dict.items():
        if term not in stoplist:
            term_list.append((term, lr, emot_dict[emot][term]))
    term_list = sorted(term_list, key=lambda x:-x[1])
    data[emot]['lh_ratio'] = term_list[:10]

for k, v_dict in data.items():
    l = [e[0] for e in v_dict['lh_ratio']]
    print('%s\t%s' % (k, '\t'.join(l)))

#with open('collocation_top10.json', 'w') as f:
#    json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
