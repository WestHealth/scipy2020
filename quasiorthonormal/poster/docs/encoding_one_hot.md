---
no_toc: True
slim: True
---

## One Hot Encoding

Our example with the Japanese car makes:

|Make       |Ordinal|One-Hot|
|-----------|:-----:|-------------|
|Toyota     | 1     | (1,0,0,0,0) |
|Honda      | 2     | (0,1,0,0,0) |
|Subaru     | 3     | (0,0,1,0,0) |
|Nissan     | 4     | (0,0,0,1,0) |
|Mitsubishi | 5     | (0,0,0,0,1) |

This is the most common encoding used in machine learning. [One hot
encoding]("for completeness there is a one-cold encoding where the '1' and '0' switch roles") takes a category with cardinality $N$ and encodes each
categorical value with an `N`-dimensional vector with a single '1'
and the remainder '0's. Take as an example encoding five makes of Japanese
Cars: Toyota, Honda, Subaru, Nissan, Mitsubishi. Table above shows a comparison of coding between ordinal and one-hot encodings.

The advantage is that one hot encoding does not induce an implicit
ordering or between categories. The primary disadvantage is that the
dimensionality of the problem has increased with corresponding increases
in complexity, computation and "the curse of high dimensionality".
This easily leads to the high dimensionality low sample size (HDLSS)
situation, which is a problem for most machine learning methods.

Back to [Classic Encodings](encodings.md)