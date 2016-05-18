ans = list()
with open('../prediction-filter-punc-dict-pseg-6gram.csv', 'r') as f:
    for line in f:
        if line.startswith('Id'):
            continue
        ele = {
            'id': line.split(',')[0],
            'emot':line.split(',')[1].split()
        }
        ans.append(ele)

topic_ans = dict()
with open('../prediction-all-corpus-0.9.csv', 'r') as f:
    for line in f:
        if line.startswith('Id'):
            continue
        topic_ans[line.split(',')[0]] = line.split(',')[1].split()


with open('../prediction-6gram-all-0.9.csv', 'w') as f:    
    f.write('Id,Emoticon\n')
    for e in ans:
        f.write(e['id'] + ',')
        if topic_ans[e['id']]:
            new_emot = list()
            for e_id in topic_ans[e['id']]:
                if e_id not in new_emot:
                    new_emot.append(e_id)
            for e_id in e['emot']:
                if len(new_emot) == 3:
                    break
                else:
                    if e_id not in new_emot:
                        new_emot.append(e_id)
        else:
            new_emot = e['emot']
        f.write(' '.join(new_emot) + '\n')

