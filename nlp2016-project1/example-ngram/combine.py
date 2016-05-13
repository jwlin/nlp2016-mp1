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
with open('prediction-0.9.csv', 'r') as f:
    for line in f:
        if line.startswith('Id'):
            continue
        topic_ans[line.split(',')[0]] = line.split(',')[1].split()


with open('prediction-6gram-topic0.9-reverse.csv', 'w') as f:    
    f.write('Id,Emoticon\n')
    for e in ans:
        f.write(e['id'] + ',')
        if topic_ans[e['id']]:
            '''
            new_emot = topic_ans[e['id']]
            for e_id in e['emot']:
                if e_id not in new_emot:
                    new_emot.append(e_id)
                    if len(new_emot) == 3:
                        break
            '''
            new_emot = e['emot']
            if topic_ans[e['id']][0] not in new_emot[:2]:
                new_emot[2] = topic_ans[e['id']][0]
        else:
            new_emot = e['emot']
        f.write(' '.join(new_emot) + '\n')

