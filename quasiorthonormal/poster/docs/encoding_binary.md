---
no_toc: True
slim: True
---

## Binary Encoding, Hash Encoding, BaseN Encoding

Our example with the Japanese car makes:

|Make       |Ordinal| as Binary | Binary Code|
|-----------|:-----:|:---------:|:---:|
|Toyota     | 1     | 001 |(0,0,1) |
|Honda      | 2     | 010 |(0,1,0) |
|Subaru     | 3     | 011 |(0,1,1) |
|Nissan     | 4     | 100 |(1,0,0) |
|Mitsubishi | 5     | 101 |(1,0,1) |


Between ordinal encoding and one-hot encoding Somewhere in between
these two are *binary encoding*, *hash encoding* and *baseN*
encoding. Binary encoding simply labels each category with a  
unique binary code and converts the binary code to a vector. Using the
previous example of the Japanese car makes, the above table shows
an example of binary encoding. BaseN encoding is a generalization of
binary encoding that uses a number base other than 2 (binary). 


Hash encoding assigns each category an ordinal value that is then
converted into a binary hash value that is encoded as an $n$-tuple
in the same fashion as the binary encoding. You can view hash encoding
as binary encoding applied to the hashed ordinal value. Hash encoding
has several advantages. First, it is open ended so new categories can be
added later. Second, the resultant dimensionality can be much lower than
one-hot encoding. The chief disadvantage is that categories can collide
if two categories accidentally map into the same hash value. This is a
*hash collision* and must be fixed separately using a resolution
mechanism. [Bernardi's
blog](https://booking.ai/dont-be-tricked-by-the-hashing-trick-192a6aae3087)
provides a good treatment of hash coding. 

A disadvantage of all three of these techniques is that while it does
reduce the dimension of the encoded feature, artificial geometric
relationships may creep in between unrelated categories. For example,
`(0.7,0.7)` may be confusion between Toyota and Honda or a weak Subaru
result, although the effect is not as pronounced as ordinal encoding.

Back to [Classic Encodings](encodings.md)