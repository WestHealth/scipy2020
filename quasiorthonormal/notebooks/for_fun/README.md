# Just For Fun
I think it is just as important to publish or display failed ideas. Ideas of curiosity in addition to successes. Two major reasons, first this allows others to avoid the same mistakes and second sometimes the core idea is a good one and others might find a way to make it viable.

In that spirit, there are a bunch of notebooks presented here.

  * Why crossentropy loss and not MSE 
     - [What happens if you try MSE on one-hot-encoding](one-hot-mse.ipynb)
  * How tough is the MNIST classification problem?
     - This [notebook](linear.ipynb) basically does a linear fit. 
  * Why is ordinal so bad?
     - This [notebook](ordinal_mse.ipynb) tries classification in the most straightforward method with ordinal codes.
     - This [notebook](ordinal_sce.ipynb) tries classification but converts the output to a probability density so that crossentropy loss can be used.
  * How about binary codes?
      - [Binary codes using MSE](binary.ipynb)
      - [Binary codes treated as a basis](binary_qsoftmax_sce.ipynb)
      - [Binary codes with sparse crossentropy loss](binary_sce.ipynb)
  
  * A reviewer asked what about random vectors since random vectors generate near orthogonal pairs. [So why not?](random_4.ipynb)
  
  Since this is just for fun here are some percentages from the various notebooks. Bear in mind due to the random nature of machine learning the accuracies can vary from run to run, but not greatly. Also, since these notebooks have been run subsequent to the paper and poster publication the numbers vary slightly.
  
### Fun results after 20 epochs

|Experiment | Dimensions | Accuracy |
|:---|:---:|:---:|
|Reference (One-Hot Encoding)|10|97.580% (98.055%)|
|Linear Model (One-Hot Encoding)| 10|92.320% (92.515%)|
|MSE (One-Hot Encoding)|10|96.340% (97.247%) |
|Quasiorthonormal|7|97.380% (97.620%)|
|Quasiorthonormal|4|95.850% (96.150%)|
|Sphere Code|5|96.610% (97.258%)|
|Sphere Code|3|95.750% (95.812%)|
|Ordinal with MSE|1|59.330%(62.492%)|
|Ordinal with Crossentropy| 1|63.750% (54.750%)|
|Binary Code with MSE|4|94.740% (96.023%)|
|Binary Code with Crossentropy and `qsoftmax`|4|96.140% (96.320%)|
|Binary Code with Crossentropy|4|96.290% (96.232%)|
|Random Code |4|95.790% (96.273%)|

### Surprisingly

While preparing this page, I discovered that four this particular circumstance binary codes with proper calculation of logits fares the best among the 4 dimensional codings. Bear in mind both the dimension and the cardinality come into play so this might be best for 4 dimensions and 10 categories, but may not fare as well for say 4 dimensions and 12 categories.