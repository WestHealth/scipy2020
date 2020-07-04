# Code and Experiments

## Code

The detailed examples expressed here use `tensorflow` to implement a classification experiment. This code presented via the link are the same as the code included in the proceedings. The main difference is that a `qsoftmax` function is substituted for the `softmax` activation function in the last layer. Since the `qsoftmax` layer has a different input and output shape, it can not be fed as an activation function to a `keras` `Dense` layer so a separate `keras` `Lambda` layer is used instead.

Source code for the metafunctions for `qsoftmax` can be found here:

  - [Numpy](https://github.com/WestHealth/scipy2020/blob/master/quasiorthonormal/notebooks/helpers/np_qsoftmax.py)
  - [Tensorflow](https://github.com/WestHealth/scipy2020/blob/master/quasiorthonormal/notebooks/helpers/tf_softmax.py)
  - [Pytorch](https://github.com/WestHealth/scipy2020/blob/master/quasiorthonormal/notebooks/helpers/pt_softmax.py)

## Validation Experiments

The basic experiment uses the basic MNIST classification handwriting dataset and classifies handwritten digits. This dataset is available as part of `keras`. 

The [notebook](https://github.com/WestHealth/scipy2020/blob/master/quasiorthonormal/notebooks/reference.ipynb) performs the basic classification almost identically to the example given by the `keras` quick start tutorial.

Additionally, we test to verify that if the standard orthogonal basis (e.g. ${(0,0,1), (0,1,0), (1,0,0)}$) is fed into the `qsoftmax` function as a lambda layer we get the same results as the standard model.

## Experiment with Quasiorthonormal Basis

The results compare the accuracy of two quasiorthonormal encodings with one hot encoding. This is summarized in the following table with the training accuracy in parenthesis. The results are linked to the respective notebooks, your results may vary due to the randomness in a deep neural network.

|Number of Epochs|One Hot Encoding|7-Dimensional QO|4-Dimensional QO|
|:---:|:---:|:---:|:---:|
|10|97.53% (97.30%)|97.24% (96.94%)|95.65% (95.15%)|
|20|[97.68% (98.02%)](https://github.com/WestHealth/scipy2020/blob/master/quasiorthonormal/notebooks/reference.ipynb)|[97.49% (97.75%)](https://github.com/WestHealth/scipy2020/blob/master/quasiorthonormal/notebooks/qo7.ipynb)|[95.94% (96.15%)](https://github.com/WestHealth/scipy2020/blob/master/quasiorthonormal/notebooks/qo4.ipynb)|

## Experiment with Spherical Codes

The results compare the accuracy of two spherical encodings with one hot encoding. This is summarized in the following table with the training accuracy in parenthesis. The results are linked to the respective notebooks. Once again your mileage may vary.

|Number of Epochs|One Hot Encoding|5-Dimensional SC|3-Dimensional SC|
|:---:|:---:|:---:|:---:|
|10|97.53% (97.30%)|96.51% (96.26%)|95.37% (94.83%)|
|20|[97.68% (98.02%)](https://github.com/WestHealth/scipy2020/blob/master/quasiorthonormal/notebooks/reference.ipynb)|[96.82% (97.11%)](https://github.com/WestHealth/scipy2020/blob/master/quasiorthonormal/notebooks/sp5.ipynb)|[95.74% (95.83%)](https://github.com/WestHealth/scipy2020/blob/master/quasiorthonormal/notebooks/sp3.ipynb)|

## Just for fun

We concocted some experiments with other coding. For instance, how bad is ordinal coding? See [here](https://github.com/WestHealth/scipy2020/tree/master/quasiorthonormal/notebooks/for_fun)

Find out [here](ordinal.ipynb)