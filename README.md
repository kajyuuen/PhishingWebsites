# SecHack365 福岡回

### 説明

URLを与えるとそのサイトがどのくらい，フィッシングサイトだと思われるか測定します.

`/kajyuuen`にはデータ検証したときのJupyterNotebookが入っております．

### 起動方法

`/demo`内にて `python start.py`

### データセット元

Machine Learning Repositotyの[Phishing Websites Data Set](https://archive.ics.uci.edu/ml/datasets/phishing+websites)を利用してモデルを作成しています．

### アルゴリズム

コメントにてアルゴリズムについて知りたいとあったので，少し書きます．

今回はロジスティック回帰というものを使っております．確率を出せると面白いかなと思いましたが二値分類でもいいのでは無いかという意見もあったので，今後はSVMを使うかもしれません．

### 今後
  
  - データセットそのものが古いため，更新を行う
  - 提供されている特徴量以外も探してみたい
  - 精度を高めたい
