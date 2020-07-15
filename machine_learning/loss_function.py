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

def categorical_focal_loss_with_logits(alpha, gamma=2.):
    """
    Parameters:
      alpha -- the same as weighing factor in balanced cross entropy. Alpha is used to specify the weight of different
      categories/labels, the size of the array needs to be consistent with the number of classes.
      gamma -- focusing parameter for modulating factor (1-p)
    Default value:
      gamma -- 2.0 as mentioned in the paper
      alpha -- 0.25 as mentioned in the paper
    References:
        Official paper: https://arxiv.org/pdf/1708.02002.pdf
        https://www.tensorflow.org/api_docs/python/tf/keras/backend/categorical_crossentropy
    """

    alpha = np.array(alpha, dtype=np.float32)

    def categorical_focal_loss(y_true, y_pred, return_type=0):
        """
        :param y_true: A tensor of the same shape as `y_pred`
        :param y_pred: A tensor resulting from a softmax
        :param return_type: return type of loss tensor 0: total loss, 1: loss per prediction 2: loss per class of
        :return: Output tensor.
        """

        # Scale predictions so that the class probas of each sample sum to 1
        y_pred /= K.sum(y_pred, axis=-1, keepdims=True)

        # Clip the prediction value to prevent NaN's and Inf's
        epsilon = K.epsilon()
        y_pred = K.clip(y_pred, epsilon, 1. - epsilon)

        # Calculate Cross Entropy
        cross_entropy = -y_true * K.log(y_pred)

        # Calculate Focal Loss
        loss = alpha * K.pow(1 - y_pred, gamma) * cross_entropy

        # Compute mean loss in mini_batch
        if return_type == 0: # totoal loss
            return K.mean(K.sum(loss, axis=-1))
        elif return_type == 1: # loss per prediction
            return K.sum(loss, axis=-1)
        else:
            return loss # loss per each class of a prediction
        
    return categorical_focal_loss

def case_binary_focal_loss_with_logits():
    # setup
    R = 1000
    NS = np.linspace(0,1.0,R)
    a = K.constant(np.vstack([np.ones((1,R)),np.zeros((1,R))]))
    b=  K.constant(np.vstack([np.expand_dims(NS,0),np.expand_dims(NS,0)]))
    
    # create loss
    gammas = [0.5, 1, 2, 3, 4]
    c0_5 = binary_focal_loss_with_logits(0.5, -1)(a, b, 1)
    c1 = binary_focal_loss_with_logits(1, -1)(a, b, 1)
    c2 = binary_focal_loss_with_logits(2, -1)(a, b, 1)
    c3 = binary_focal_loss_with_logits(3, -1)(a, b, 1)
    c4 = binary_focal_loss_with_logits(4, -1)(a, b, 1)
    ce = keras.backend.binary_crossentropy(a, b)
    
    d = [K.eval(c) for c in [c0_5, c1, c2, c3, c4]]
    dce = K.eval(ce)
    
    # plot
    import matplotlib.pyplot as plt
    for i in range(5):
        plt.plot(NS, d[i][0], label='focal_loss[%.1f,noweight]' % gammas[i])
    plt.plot(NS, dce[0],color='black',label='cross_entropy')
    plt.ylim([0,5])
    plt.legend()
    plt.title("binary loss on ground truth is 1")
    plt.show()
    # we can observe the curve is similar to the one in the paper

def case_categorical_focal_loss_with_logits():
    R = 1000
    NS = np.linspace(0,1.0,R)
    a = K.constant(np.vstack([np.ones((1,R)),np.zeros((1,R))]).T)
    b=  K.constant(np.vstack([np.expand_dims(NS,0),np.ones((1,R))*0.5]).T)
    gammas = [0.5, 1, 2, 3, 4]
    c0_5 = categorical_focal_loss_with_logits(1, 0.5)(a, b, 1)
    c1 = categorical_focal_loss_with_logits(1, 1)(a, b, 1)
    c2 = categorical_focal_loss_with_logits(1, 2)(a, b, 1)
    c3 = categorical_focal_loss_with_logits(1, 3)(a, b, 1)
    c4 = categorical_focal_loss_with_logits(1, 4)(a, b, 1)
    ce = keras.backend.categorical_crossentropy(a, b)
    
    d = [K.eval(c) for c in [c0_5, c1, c2, c3, c4]]
    dce = K.eval(ce)

    import matplotlib.pyplot as plt
    for i in range(5):
        plt.plot(NS, d[i], label='focal_loss[%.1f,noweight]' % gammas[i])
    plt.plot(NS, dce,color='black',label='cross_entropy')
    plt.ylim([0,5])
    plt.legend()
    plt.title("binary loss on ground truth is 1")
    plt.show()

if __name__ == '__main__':
    main()
