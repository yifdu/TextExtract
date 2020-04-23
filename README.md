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
|          |         |            |TFIDF                   |   0.224      |  0.225 | 0.225  |
|          |         |            |TextRank                |   0.251      |  0.252 |  0.252 |
|          |         |            |TextRank_withMultiWindow|   0.255      |  0.256 |  0.256 |
|          |         |            |TextRank_withTitle      |   0.246      |  0.246 |  0.246 |
|          |         |            |LDA                     |   0.069      |  0.070 |  0.069 |
|          |         |            |LSI                     |   0.192      |  0.192 |  0.192 |
|          |         |            |BM25                    |         |      |   |
|          |         |            |KeyGraph                |   0.244      | 0.244  | 0.244  |
参考文献:https://github.com/topics/keyword-extraction?l=python
