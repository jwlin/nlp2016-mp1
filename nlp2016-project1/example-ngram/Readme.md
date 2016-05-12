## 與範例檔案不同處:

### Makefile

ORDER = 6, pip install -r requirement.txt

### maxprob.py

只輸出前三高機率結果

### preprocess.py

`sanitize()`: 斷詞之前先過濾特殊字元, 移除重複空白, 換掉全形標點等. 斷詞改用較大的字典檔

### collocation 開頭檔案, count_top10.py, term_stat.json

作業一找相關詞用的(Likelyhood Ratio)

### topic_train.py, topic_test.py

作 topic modeling 用的, 可不用管
