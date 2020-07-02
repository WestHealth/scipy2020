---
no_toc: True
slim: True
---

## Quasiorthonormal Encoding

Our example with the Japanese car makes:

|Make       | One-Hot     | Quasiorthonornal Code |
|-----------|:-----:|:---------:|
|Toyota     | (1,0,0,0,0) | (0.851, 0.000, -0.526) |
|Honda      | (0,1,0,0,0) | (0.526, -0.851, 0.000) |
|Subaru     | (0,0,1,0,0) | (0.000, -0.526, 0.851) |
|Nissan     | (0,0,0,1,0) | (0.851, 0.000, 0.526)  |
|Mitsubishi | (0,0,0,0,1) | (-0.526, -0.851, 0.000)|

If you think of one-hot encoding as encoding categories with unit vectors in $N$ dimensions ($\mathbb{R}^5$ in this case), then you are encoding your categories onto an orthonormal basis (the set of unit vectors in $\mathbb{R}^N$. Quasiorthonormal encoding relaxes the orthonormal requirement and substitute a quasiorthonormal "basis". The above table shows 5 quasiorthonormal vectors in 3 dimensions having a minimum mutual angle of aboout $63^\circ$.

There is substantial mathematical theory on what is quasiorthogonality and quasiorthonormality, how you construct it, how to decode it including a counterpart to the `softmax` function. All of which is presented in much greater detail in the accompanying proceedings paper.

Back to [Classic Encodings](encodings.md)