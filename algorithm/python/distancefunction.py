import numpy as np

def L1Norm(v0, v1) -> float:
    return np.sum(np.abs(v0 - v1))

def L2Norm(v0, v1) -> float:
    val = np.abs(v0 - v1)
    return np.sqrt(np.sum(val * val))

def HammingDistance(v0, v1) -> int:
    """
    @brief Calculate Elementwise distance
    @param[in] v0 - dim N vector
    @param[in] v1 - dim N vector
    """
    return np.sum(v0 != v1)

def CosineSimilarity(v0, v1) -> float:
    """
    @brief Calculate Cosine Similarity -1 exact opposite, 0 - decorrelation, 1 - totally correlated
    @param[in] v0 - dim N vector
    @param[in] v1 - dim N vector
    """
    numerator = np.dot(v0, v1)
    denominator_v0 = np.sqrt(np.dot(v0, v0))
    denominator_v1 = np.sqrt(np.dot(v1, v1))
    return numerator / (denominator_v0 * denominator_v1)

dist_func_ptr_list = [L1Norm, L2Norm, HammingDistance, CosineSimilarity]
func_name_list = ["L1Norm", "L2Norm", "Hamming Distance", "CosineSimilarity"]

def main(args):
    if args[1] == "int":
        v0 = np.random.randint(0, 255, int(args[2])) - 128
        v1 = np.random.randint(0, 255, int(args[2])) - 128
    else:
        v0 = np.random.rand(int(args[2])) - 0.5
        v1 = np.random.rand(int(args[2])) - 0.5
   
    dist_func_ptr = dist_func_ptr_list[int(args[3])]
    dist_func_name = func_name_list[int(args[3])]
    print("v0:", v0)
    print("v1:", v1)
    print(dist_func_name, ":" , dist_func_ptr(v0, v1))

if __name__ == '__main__':
    import sys
    main(sys.argv)
