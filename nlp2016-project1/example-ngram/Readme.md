# 作業一

先 `make prep` 安裝必要套件

```
python collocation.py  # generate collocation.json, term_stat.json and collocation_lr.json
python count_top10.py  # generate Top 10 collocations for each emoticon
```

# 作業二

## KenLM

```
make prep
make all  # generate prediction.csv
```

## Topic modeling

```
python topic_train.py  # 產生 training_corpus.json 及相關檔案. p.s. 會跑非常久 e.g. 2x hours
python topic_test.py  # 產生 testing_corpus.json, 只產出相似度 >0.9 的預測結果. p.s.會跑非常久 e.g. 2x hours
python combine.py  # 用 testing_corpus.json 裡面的資料去取代 KenLM 的結果
```

## 與範例檔案不同處:

## Makefile

ORDER = 6, pip install -r requirement.txt

### maxprob.py

只輸出前三高機率結果

### preprocess.py

`sanitize()`: 斷詞之前先過濾特殊字元, 移除重複空白, 換掉全形標點等. 斷詞改用較大的字典檔

