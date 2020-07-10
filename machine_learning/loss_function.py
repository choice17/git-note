import tensorflow.keras.backend as K
from tensorflow import keras

def binary_focal_loss_with_logits(gamma=2.0, alpha=0.5):
    if alpha >= 0:
        alpha_t0 = alpha
        alpha_t1 = 1 - alpha
    else:
        alpha_t0 = 1
        alpha_t1 = 1
    def binary_focal_loss(y_true, y_pred, return_type=0):
        epsilon = K.epsilon()
        # clip to prevent NaN's and Inf's
        y_pred = K.clip(y_pred, epsilon, 1.-epsilon)
        #pt_1 = K.clip(pt_1, epsilon, 1. - epsilon)
        #pt_0 = K.clip(pt_0, epsilon, 1. - epsilon)
        if return_type==0:
            return -K.mean(y_true * alpha_t0 * K.pow(1. - y_pred, gamma) * K.log(y_pred)) \
               -K.mean((1 - y_true) * alpha_t1 * K.pow(y_pred, gamma) * K.log(1. - y_pred))
        else:
            return -(y_true * alpha_t0 * K.pow(1. - y_pred, gamma) * K.log(y_pred)) \
               -((1 - y_true) * alpha_t1 * K.pow(y_pred, gamma) * K.log(1. - y_pred))
    return binary_focal_loss

def main():
    R = 1000
    a = K.constant(np.vstack([np.ones((1,R)),np.zeros((1,R))]))
    b=  K.constant(np.vstack([np.expand_dims(np.linspace(0,1.0,R),0),np.expand_dims(np.linspace(0,1.0,R),0)]))
    
    gammas = [0.5, 1, 2, 3, 4]
    c0_1 = binary_focal_loss_with_logits(0.5, -1)(a, b, 1)
    c1 = binary_focal_loss_with_logits(1, 0.75)(a, b, 1)
    c2 = binary_focal_loss_with_logits(2, 0.75)(a, b, 1)
    c3 = binary_focal_loss_with_logits(3, 0.75)(a, b, 1)
    c4 = binary_focal_loss_with_logits(4, 0.75)(a, b, 1)
    ce = keras.backend.binary_crossentropy(a, b)
    
    d = [np.clip(K.eval(c),0,5) for c in [c0_1, c1, c2, c3, c4]]
    dce = np.clip(K.eval(ce),0,5)
    
    import matplotlib.pyplot as plt
    for i in range(5):
        plt.plot(d[i][0], label='focal_loss[%.1f,noweight]' % gammas[i])
    plt.plot(dce[0],color='orange',label='cross_entropy')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
