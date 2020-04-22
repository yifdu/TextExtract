# TextExtract
Model:
- [x] TF-IDF
- [x] TextRank(三种形式)
- [x] TopicModel(LDA、LSI)
- [ ] RAKE
- [ ] SKE
- [x] KeyGraph
- [x] BM25

| Task     | Datasets| vocabulary |Model                   |Precision|Recall|F1 |
|----------|---------|------------|------------------------|---------|------|---|
|          |         |            |TFIDF                   |   0.170      |  0.285 | 0.213  |
|          |         |            |TextRank                |   0.186      |  0.311 |  0.233 |
|          |         |            |TextRank_withMultiWindow|   0.190      |  0.318 |  0.238 |
|          |         |            |TextRank_withTitle      |   0.180      |  0.301 |  0.225 |
|          |         |            |LDA                     |   0.053      |  0.088 |  0.066 |
|          |         |            |LSI                     |   0.137      |  0.230 |  0.172 |
|          |         |            |BM25                    |         |      |   |
|          |         |            |KeyProcessor            |         |      |   |
|          |         |            |KeyGraph                |   0.182      | 0.304  | 0.228  |
参考文献:https://github.com/topics/keyword-extraction?l=python
