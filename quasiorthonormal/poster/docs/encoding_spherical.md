---
no_toc: True
slim: True
---


## Spherical Encoding

Our example with the Japanese car makes:

|Make       | One-Hot     | Spherical Code |
|-----------|:-----:|:---------:|
|Toyota     | (1,0,0,0,0) | (1,0,0)  |
|Honda      | (0,1,0,0,0) | (-1,0,0) |
|Subaru     | (0,0,1,0,0) | (0,1,0)  |
|Nissan     | (0,0,0,1,0) | (0,-1,0) |
|Mitsubishi | (0,0,0,0,1) | (0,0,1)  |

Spherical encoding is similar to [quasiorthonormal encoding](encoding_quasiorthonormal.md) (QOE) except it uses points antipodal to those in a quasiorthonormal basis. In principle twice as many vectors can be squeezed into the same dimension as QOE (or the minimum mutual angle can be increased). Much more on the theory is described in the accompanying proceedings paper.

Back to [Classic Encodings](encodings.md)