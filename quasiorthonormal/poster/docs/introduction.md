# Primer on Encodings

## Why Encodings?

Most popular machine learning methods such as deep learning
require numerical data as input. However, quite often categorical data is common. In health care, for example, a person's vitals could be a combination of both,
they could include height, weight (numerical) and gender, race
(categorical).

Quite simply if an ML system operates on numerical data, categorical data needs to be converted to a number or vector of numbers.

## Encodings for Inputs

The treatment appropriateness of the type of embedding can depend on how it is used in a system. For example, if an encoding is primarily used as a feature to feed as input to a ML system, then decoding a noisy number or vector back to the category is not important. However, even with this one should be cautious not to introduce implicit relationships between classes that aren't there. Examples are discussed with [ordinal encoding](encoding_ordinal.md). Furthermore, in this regard statistical related encodings might be appropriate such as contrast or Bayseian encoding as statistical relationships between categories may be desirable to preserve.

## Decoding Encodings

In some applications, such as classification, decoding an noisy
encoded number of vector to a category is very important. For example,
if you have a system that classifies animal images into the animals
they represent it is important to know what a given vector represents
especially when the resultant vector does not match precisely. Does
the vector `(0.1, 0.2, 0, 0.9)` decode to a panda when panda encodes
to `(0,0,0,1)`? What deep learning networks often do is apply a
`softmax` function which converts the output of the network into a
[probability density function]("Pet peeve: though mathematically the
word probability is appropriate it is more of a score rather than a
true measure of probability"). Quite often for categorical outputs,
a maximum likelihood loss function which requires a probability
density function is used rather than the more numerically oriented
mean square error.
## Types of Encoding

Coding methods can be categorized as *classic*, *contrast*,
*Bayesian* and [*word embeddings*](https://en.wikipedia.org/w/index.php?title=Word_embedding&oldid=951683288). Classic, contrast and Bayseian
encoding are given a good overview treatment by [Hale's blog](https://towardsdatascience.com/smarter-ways-to-encode-categorical-data-for-machine-learning-part-1-of-3-6dca2f71b159) with examples to be found as part of the [`scikit-learn` category
encoding package](http://contrib.scikit-learn.org/category_encoders/). Both
contrast encoding and Bayesian encoding use the statistics of the data
to facilitate encoding. These two categories may be of use when more
statistical analysis is required, however there has not been widespread
adoption of these encoding techniques for machine learning. Word
embeddings form a category in themselves and are very important when
machine learning is used for natural language processing, which is a
different discussion altogether.

## Dimensionality Issues

As a general rule, the higher the dimension the less geometric
atrifacts are induced by the encoding. Of course, this does not come
without cost. There is generally an increase in amount of complexity
in a neural network and corresponding computation resources
needed. Additionally, there are geometric issues such as ["the curse of
high
dimensionality"](https://en.wikipedia.org/w/index.php?title=Curse_of_dimensionality&oldid=942360605).

Also as a general rule for machine learning models, the higher the
dimension, the more samples are needed to train otherwise it leads to
a problem known as high dimensionality low sample size (HDLSS)
situation, which is a problem for most machine learning methods.

For high cardinality categories, there is a tradeoff between the use
(input vs output), drawbacks of high dimensionality and geometric
artifacts. The proper choice depends on your
situation. Quasiorthonormal encoding and spherical encoding may offer
a happy medium and is the central focus of this poster.