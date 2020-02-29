import numpy as np
import matplotlib.pyplot as plt
import math


class LINE(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.r = 0.
        self.theta = 0.
        self.votes = 0

    def getPolar(self):
        self.theta = -np.arctan(1./self.a)
        self.r = self.b * np.sin(self.theta)

    def genLine(ptsA, ptsB):
        x0, y0 = ptsA
        x1, y1 = ptsB
        line = LINE(0,0)
        line.a = (x1 - x0) / (y1 - y0)
        line.b = y0 - line.a * x0
        return line

    def getRTheta(x, y, theta):
        r = x * np.cos(theta) + y * np.sin(theta)
        return r

    def getRThetaS(pts, mag=1, num_theta = 180):
        """
        @params[in] pts: M x N (number of points X 2)
        @params[out] pts: M x num_theta (R at thetas)
        """
        m, _ = pts.shape
        theta = np.linspace(-np.pi/2, np.pi/2, num_theta)
        theta_space = np.empty((2, num_theta))
        theta_space[0,:] = np.cos(theta)
        theta_space[1,:] = np.sin(theta)
        _pts = pts @ theta_space # M x 2 @ 2 x N
        #return _pts.astype(int)
        return (_pts * mag).astype(int)

    def getRThetaVote(Rpts):
        """
        @params[in] Rpts: M x num_thetta
        """
        m, n = Rpts.shape
        _max = Rpts.max()
        _min = Rpts.min()
        Rpts -=  _min
        votes = np.zeros([_max-_min+1, n], dtype=np.uint8)
        for i in range(m):
            for j in range(n):
                votes[Rpts[i,j],j] +=1
        return votes, _min

    def genPoint(line, size, num_pts, noise=0):
        w, h = size
        pts = np.empty([num_pts, 2])
        _noise = (np.random.randn(num_pts)* noise).astype(int)
        pts_w = np.random.randint(0, w, num_pts)
        pts_h = line.a * pts_w + line.b + _noise
        pts[:,0] = pts_w     
        pts[:,1] = pts_h
        return pts

    def getResPtsFromVotes(votes, vote_min):
        return np.argwhere(votes>=vote_min)

    def convertResToLine(resPts, mag, minimum, num_theta, votes=None):
        res = resPts.astype(float)
        res[:,0] += minimum
        res[:,0] /= mag
        res[:,1] = res[:,1] * (np.pi/num_theta) - np.pi/2 
        vote_list = []
        try:
            for r in resPts:
                print(444, r)
                i, j = r
                vote_list.append(votes[i, j])
            print(777, resPts)
        except:
            pass
        return LINE.convertRThetaToLine(res, vote_list)

    def convertRThetaToLine(rTheta, vote_list=[]):
        """
        @param[in] rTheta [m,n] m-number of rtheta, n-dims(should be 2 [r,theta])
        """
        m, n = rTheta.shape
        lines = []
        for i in range(m):
            a = -1/np.tan(rTheta[i,1])
            b = rTheta[i,0] / np.sin(rTheta[i,1])
            line = LINE(a=a,b=b)
            if (vote_list!=[]):
                line.votes = vote_list[i]
            lines.append(line)
        return lines

    def __str__(self):
        return "LINE: y = %.2f * x + %.2f, r=%.2f theta=%.2f votes:%d"  % (self.a, self.b, self.r, self.theta, self.votes)

def minmaxVotes(votes):
    _max = votes.max()
    votes = votes.astype(float)
    votes = (votes / _max) * 255
    return votes.astype(np.uint8), _max

def test_0():
    size = [50,50]
    num_pts = 10
    num_theta = 360
    mag= 1
    noise = 0
    line = LINE.genLine([3,2], [4,6])
    pts = LINE.genPoint(line, size, num_pts, noise)
    print(0, pts)
    Rpts = LINE.getRThetaS(pts, mag=mag, num_theta=num_theta)
    votes, _min = LINE.getRThetaVote(Rpts)
    print(1111, np.unique(votes), "min:", _min)
    print(2222, votes)
    _v, _max = minmaxVotes(votes.copy())
    ResPts = LINE.getResPtsFromVotes(votes.copy(), vote_min=10)
    print(3333, ResPts.shape, ResPts)
    lines = LINE.convertResToLine(ResPts, mag=mag, minimum=_min, num_theta=num_theta, votes=votes)
    print(666)
    for l in lines:
        l.getPolar()
        print(l)
    line.getPolar()
    print("gt", line)


def test0():
    size = [360,240]
    num_pts = 10
    num_theta = 360
    noise = 0
    mag = 1
    vote_min = 7
    line = LINE.genLine([3,2], [4,6])
    pts = LINE.genPoint(line, size, num_pts, noise)
    line0 = LINE.genLine([4,3], [7,-2])
    pts0 = LINE.genPoint(line0, size, num_pts, noise)
    pts = np.vstack([pts, pts0])
    print(0, pts)
    Rpts = LINE.getRThetaS(pts, mag=mag, num_theta=num_theta)
    votes, _min = LINE.getRThetaVote(Rpts)
    print(1111, np.unique(votes), "min:", _min)
    print(2222, votes)
    _v, _max = minmaxVotes(votes.copy())
    ResPts = LINE.getResPtsFromVotes(votes, vote_min=vote_min)
    print(3333, ResPts.shape, ResPts)
    lines = LINE.convertResToLine(ResPts, mag=mag, minimum=_min, num_theta=num_theta, votes=votes)
    print(666)
    for l in lines:
        l.getPolar()
        print(l)
    line.getPolar()
    line0.getPolar()
    print("gt", line)
    print("gt", line0)
    fig = plt.figure()
    #plt.subplot('121')
    __v = _v.copy()
    __v = (255 - __v)
    plt.imshow(__v,cmap='gray', vmin=0, vmax=255)
    #plt.subplot('122')
    plt.plot()
    plt.show()


def test1():
    # fitting 3D points 
    pts = np.array([
        [0,0,1,1],
        [1,0,1,1],
        [1,1,2,1],
        [0,1,2,1],
        [0.01,1.01,2.002,1.002]])
    _,e,v = np.linalg.svd(pts)
    print(e)
    print(v.T / v[-1,-1])

def main():
    #test_0()
    test0()
    #test1()


if __name__ == '__main__':
    main()


