import numpy as np
from PIL import Image

DEB = 1

def distance(a, a_r, a_c, b):
    aa = np.reshape(a, [a_r, 1, a_c])
    dis = np.sqrt(np.sum(np.power(aa - b, 2), axis=2))
    return dis

class KMEANS(object):
    """KMEANS python implementation
    data - inputs are 2-D numpy array NxM
    N - number of data
    M - number of feature
    K - number of clusters
    tol - value of convergence tolerence
    """
    __slots__ = ('K', 'iter', 'data', 'num_feat', 'num_data', 'tol', 'Ks_data', 'K_idx')
    def __init__(self, K=4, iter_num=10, tol=1e-1):
        self.K = K
        self.iter = iter_num
        self.tol = tol

    def setData(self, data):
        self.data = data
        self.num_feat = data.shape[1]
        self.num_data = data.shape[0]

    def setIter(self, itera):
        self.iter = itera

    def setK(self, K):
        self.K = K

    def setTol(self, tol):
        self.tol = tol

    def run(self, DEB=0):
        """
        Ks - K cluster idx
        Ks_data - K cluster points
        dis - distance vector
        cluster_id - K cluster belonging
        """
        cluster_means = np.zeros((self.K, self.num_feat))
        Ks = np.random.randint(0, self.num_data, self.K)
        Ks_data = self.data[Ks, ...]
        ks_data_prev = Ks_data.copy()
        for _ in range(self.iter):
            if DEB: print("number : ", _)
            dis = distance(self.data, self.num_data, self.num_feat, Ks_data)
            ks_data_prev = Ks_data.copy()
            cluster_id = np.argmin(dis, axis=1)
            for i in range(self.K):
                Ks_data[i, ...] = np.mean(self.data[cluster_id==i, ...], axis=0)
            dis_move = np.sqrt(np.sum(np.power(ks_data_prev - Ks_data, 2)))
            if DEB: print("dis_move : ", dis_move)
            if dis_move < self.tol:
                break
        self.Ks_data = Ks_data
        self.K_idx = np.argmin(distance(self.data,  self.num_data, self.num_feat, Ks_data), axis=1)
        return self.Ks_data, self.K_idx

    def transform(data, Ks_data, K_idx):
        K = Ks_data.shape[0]
        for k in range(K):
            data[K_idx==k, ...] = Ks_data[k:k+1, ...]

def main():
    img_src = "../../files/VOC_2007_000733.jpg"
    img = np.array(Image.open(img_src))
    h, w, c = img.shape
    data = np.reshape(img, [h * w, c]).astype(float)

    K = 24
    iter_num = 100
    kmeans = KMEANS(K=K, iter_num=iter_num)
    kmeans.setData(data)
    Ks_data, K_idx = kmeans.run(DEB=1)

    KMEANS.transform(data, Ks_data, K_idx)
    n_img = np.reshape(data, [h, w, c]).astype(np.uint8)

    n_img = Image.fromarray(n_img)
    n_img.show()

if __name__ == '__main__':
    main()