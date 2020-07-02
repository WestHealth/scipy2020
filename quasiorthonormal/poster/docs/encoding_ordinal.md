---
no_toc: True
slim: True
---

## Ordinal Coding

Our example with the Japanese car makes:

|Make       |Ordinal|
|-----------|:-----:|
|Toyota     | 1     | 
|Honda      | 2     | 
|Subaru     | 3     | 
|Nissan     | 4     | 
|Mitsubishi | 5     | 

Ordinal encoding or sometimes known as label encoding is the simplest
and perhaps most naive approach encoding for a categorical feature ---
one simply assigns a number to each member of a category. This is
often how data from surveys are encoded into spreadsheets for easy storage and
calculation of basic statistics. An associated data dictionary is used
to convert the values back and forth between a number and a category.
Take for example the case of gender, male could be encoded as 1 and
female as 2, with a data dictionary as follows:
:code:`{'male': 1, 'female': 2}`

Suppose we have three categories of ethnic groups: White, Black, and
Asian. Under ordinal encoding, suppose White is encoded as 1, Black is
encoded as 2 and Asian is encoded as 3. If a machine learning
classification is somehow confused between Asian and White and decides
to split the difference and report the in-between value (2) which
encodes Black. The issue is that arbitrary gradation between 1 and 3
introduces a natural interpolation (2) that may be nonsense. Thus, the
natural ordering of the numbers imposes an ordered geometrical
relationship between the categories that does not apply.

Nonetheless there are situations where ordinal encoding makes sense. For
example, a \`rate your satisfaction' survey typically encodes five levels
(1) terrible, (2) acceptable (3) mediocre, (4) good, (5) excellent.

Back to [Classic Encodings](encodings.md)