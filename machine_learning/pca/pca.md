## Principal Component Analysis  

## Reference

* **[covaranice matrix](https://www.visiondummy.com/2014/04/geometric-interpretation-covariance-matrix/)**  
* **[PCA intro](http://ufldl.stanford.edu/tutorial/unsupervised/PCAWhitening/)**  
* **[PCA example](https://medium.com/@jonathan_hui/machine-learning-singular-value-decomposition-svd-principal-component-analysis-pca-1d45e885e491)**    

PCA is essentially to solve dimension reduction problem, It typically descibes centered PCA, otherwise the algo is uncentered PCA.

* **[PCA as Feature Dimension Reduction](#PCA_feature_dimension_reduction)**  
* **[PCA whitening](#PCA_whitening)**  
* **[PCA eigenvector](#SVD_vs_Eigendecomposition)**  
* **[PCA weight](#PCA_explained_variance)**  

## PCA_feature_dimension_reduction   
1. let the problem be:  

`X with dimension {NxM}; where M is the data size, N is feature size`

`Reduce the dimension to n dimension, i.e.`  

`X_reduce is {nxM}`      

```
## example.

M = 100, N = 15
n = 2

X = np.random.rand(N, M)
X_center = X - np.mean(X, axis=1)

# covariance matrix definition
covX = X_center @ X_center.T / (M-1)

## Singular Vector decomposition 
# U - dimension {NxN} orthogonal matrix
# Z - diagonal(weight) matrix {NxM}
# V.T - dimension {MxM} orthogonal matrix
# note that the actual V is the transposed V at the output of the function

U, Z, V = np.linalg.svd(X_center)
E, U.T = (np.linalg.eigh(covX)) => go sorting

U_reduce = U[:,:n]

X_reduce = U_reduce.T @ X_center

```

## PCA_whitening  

* Rotation for X (whitening data/normalization)

```
# The rotation of X whiten the data , i.e. to be less correlated/provide more information for data(especially for image)
# Futher rescale the feature by the diagonal scale Z plus zero prevention epilson value ~1E-5

epilson = 1e-5
X_rot = (U.T @ X_center)
X_pca_whiten = X_rot / np.sqrt(E + epilson)

```

## SVD_vs_Eigendecomposition  


``` 
## Note 
# U matrix is as same as eigenvector of covariance(square) matrix 
# i.e.

# Covariance matrix covX

covX = X_center @ X_center.T / (M - 1)

### Singular Vector decomposition
# Uc = Vc.T

Uc, Zc, Vc = np.lingalg.svd(conX)

# Proof

# SVD representation
X = U @ Z @ V.T

X @ X.T  = (U @ Z @ V.T ) @ (V @ Z.T @ U.T) / (M - 1)
covX = (U @ Z @ Z.T @ U.T) / (M - 1)

# Note that E and Z are both diagonal matrix
# And E > 0, and for svd of covX, U = V.T
covX = U @ (E/(M-1)) @ U.T

### Eigenvector for covariance matrix
# let Y be diagonal eigenvalue, v be eigenvector
covX @ v = Y @ v

covX @ v = v @ Y

# v @ v.T = I as v is orthogonal as same as E 
covX @ v @ v.T = v @ Y @ v.T

```

## PCA_explained_variance  

While applying PCA to a dataset, the explained variance can be obtained by  

```
# let X be {NxM} matrix, N -> feature dimension, M->dataset size
# Z be {NxM} diagonal matrix

U, Z, V = np.linalg.svd(X)

# E is a diagonal matrix as well
E = (Z @ Z.T)/(M-1)

# Then the explained variance is the arranged from high to low
```



