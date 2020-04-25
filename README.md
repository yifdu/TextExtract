# TextExtract
Model:
- [x] TF-IDF
- [x] TextRank(三种形式)
- [x] TopicModel(LDA、LSI)
- [x] RAKE
- [x] KeyGraph
- [x] BM25


1. Top3

| Task     | Datasets| vocabulary |Model                   |Precision|Recall|F1 |
|----------|---------|------------|------------------------|---------|------|---|
|          |  神策       |            |TFIDF                   |   0.224      |  0.225 | 0.225  |
|          |  神策       |            |TextRank                |   0.251      |  0.252 |  0.252 |
|          |  神策     |            |TextRank_withMultiWindow|   0.255      |  0.256 |  0.256 |
|          |  神策       |            |TextRank_withTitle      |   0.246      |  0.246 |  0.246 |
|          |  神策       |            |LDA                     |   0.069      |  0.070 |  0.069 |
|          |  神策       |            |LSI                     |   0.192      |  0.192 |  0.192 |
|          |  神策       |            |RAKE                    |   0.092      |  0.092 |  0.092 |
|          |  神策       |            |KeyGraph                |   0.244      |  0.244 |  0.244 |

2. Top4

| Task     | Datasets| vocabulary |Model                   |Precision|Recall|F1 |
|----------|---------|------------|------------------------|---------|------|---|
|          |  神策       |            |TFIDF                   |   0.194      |  0.259 | 0.221  |
|          |  神策       |            |TextRank                |   0.214      |  0.287 |  0.245 |
|          |  神策       |            |TextRank_withMultiWindow|   0.217      |  0.290 |  0.248 |
|          |  神策       |            |TextRank_withTitle      |   0.209      |  0.280 |  0.239 |
|          |  神策       |            |LDA                     |   0.055      |  0.073 |  0.063 |
|          |  神策       |            |LSI                     |   0.209      |  0.280 |  0.239 |
|          |  神策       |            |RAKE                    |   0.085      |  0.113 |  0.097 |
|          |  神策       |            |KeyGraph                |   0.211      | 0.281  |  0.241 |






