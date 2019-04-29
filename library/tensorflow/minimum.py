    # MNIST For ML Beginners!

# This tutorial is intended for readers who are new to both machine learning and TensorFlow.
# Just like programming has Hello World, machine learning has MNIST.
# MNIST is a simple computer vision dataset. It conssists of images of handwritten digits.
# Source: https://goo.gl/rLXVsR

# Please help us to improve this section by sending us your
# feedbacks and comments on: https://docs.google.com/forms/d/16fH20Qf8gJ2o31Vnlss2uLJ7wL9vq76TeUGqghTY0uI/viewform

# Importing input data
# @by tcyu.umich.edu 2019/04/30
import random
import sys
import numpy as np
import datetime
from dataprocessing import MNIST_Loader
import tensorflow as tf
import traceback
import os

train_file = 'data/MNIST/train.csv'
test_file = 'data/MNIST/test.csv'
mnist_loader = MNIST_Loader(train_file, test_file)
x_train_valid, y_train_valid, _ = mnist_loader.get_data()
train_data = x_train_valid.copy()
label_data = y_train_valid.copy()
del x_train_valid
del y_train_valid, MNIST_Loader, mnist_loader
NUM = train_data.shape[0]
LR_step = [0,500,1000, 1300, 1600, 2000]
LR_rate = [0.01, 0.001, 0.0001, 0.01, 0.001, 0.0001]
MINI_BATCHSIZE = 64
CURRENT_MINI = 0
CURRENT_EPOCH = 0
EPOCH = 4
UPDATE = 10
SAVE_UPDATE = 10
#train_data = train_data.reshape(-1,28,28,1)

################################
# Enter your code between here #
################################

tf_init_w = lambda shape: tf.truncated_normal(shape=shape, stddev=0.1)
tf_init_b = lambda shape: tf.constant(0.1, shape=shape)
tf_conv = lambda x, w, b: tf.nn.relu(tf.nn.conv2d(x, w, strides=[1,1,1,1], padding='SAME')+b)
tf_maxpool = lambda x: tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
reg_constant = 0.01

def define_variable():
    input_ph = tf.placeholder(tf.float32, shape=[None,28,28,1])
    label_ph = tf.placeholder(tf.float32, shape=[None,10])
    w1 = tf.Variable(tf_init_w([3,3,1,16]))
    b1 = tf.Variable(tf_init_b([1,1,1,16]))
    w2 = tf.Variable(tf_init_w([3,3,16,16]))
    b2 = tf.Variable(tf_init_b([1,1,1,16]))
    w3 = tf.Variable(tf_init_w([3,3,16,32]))
    b3 = tf.Variable(tf_init_b([1,1,1,32]))
    w4 = tf.Variable(tf_init_w([3,3,32,64]))
    b4 = tf.Variable(tf_init_b([1,1,1,64]))
    w5 = tf.Variable(tf_init_w([7*7*64,10]))
    b5 = tf.Variable(tf_init_b([1,10]))
    lr = tf.placeholder(dtype=tf.float32, name="learn_rate")

    return input_ph, w1, b1, w2, b2, w3, b3, w4, b4, w5, b5, label_ph, lr
    
def create_graph():
    tf.reset_default_graph()
    myGraph = tf.Graph()
    with myGraph.as_default():

        input_ph, w1, b1, w2, b2, w3, b3, w4, b4,w5, b5, label_ph, lr = define_variable()
        norm_data = input_ph
        conv1 = tf_conv(norm_data, w1, b1)
        conv2 = tf_conv(conv1, w2, b2)
        pool2 = tf_maxpool(conv2)
        conv3 = tf_conv(pool2, w3, b3)
        pool3 = tf_maxpool(conv3)
        conv4 = tf_conv(pool3, w4, b4)
        flatten = tf.layers.flatten(conv4)
        fc5 = tf.matmul(flatten, w5) + b5
        #globalpool = tf.reduce_mean(conv4, axis=[1,2])
        pred_prob = tf.nn.softmax(fc5)

        net_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=fc5,labels=label_ph))
        reg_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
        total_loss = net_loss + reg_constant * sum(reg_losses)
        tr_step = tf.train.AdamOptimizer(lr).minimize(total_loss)
        pred_correct = tf.equal(tf.argmax(pred_prob, 1),
                            tf.argmax(label_ph, 1))
        accuracy = tf.reduce_mean(tf.cast(pred_correct, tf.float32))
        init_ = tf.global_variables_initializer()
        vars_list = [w1, b1, w2, b2, w3, b3, w4, b4,w5, b5]
    return total_loss, pred_prob, accuracy, tr_step, myGraph, input_ph, label_ph, lr, init_, vars_list

def get_mini_batch(train_dataset, train_label, iteration, train_len):
    isfinished_epoch = False
    startIdx = 0+iteration*MINI_BATCHSIZE
    endIdx = (1+iteration)*MINI_BATCHSIZE
    if startIdx > train_len-1 or endIdx > train_len-1:
        isfinished_epoch = True    
    if endIdx > train_len - 1:
        endIdx = train_len - 1
    

    train_batch = train_dataset[startIdx:endIdx,:,:,:]
    tr_label_batch = train_label[startIdx:endIdx,:]
    return train_batch, tr_label_batch, isfinished_epoch


def train_graph(sess, x_train_ph, y_train_ph, graph_keys):
    global CURRENT_EPOCH
    global CURRENT_MINI
    global EPOCH
    global LR_step
    global LR_rate
    global UPDATE
    global SAVE_UPDATE
    total_loss, pred_prob, accuracy, tr_step, input_ph, label_ph, lr, init_, vars_list = graph_keys
    shuffle_idx = np.arange(NUM)
    
    random.shuffle(shuffle_idx)
    train_idx = shuffle_idx[:-1000]
    train_len = len(train_idx)
    valid_idx = shuffle_idx[-1000:]
    train_dataset = train_data[train_idx,:,:,:]
    valid_dataset = train_data[valid_idx,:,:,:]
    train_label = label_data[train_idx,:]
    valid_label = label_data[valid_idx]
    val_loss_list = []
    tr_loss_list  = []
    save_val_loss = 999
    iteration = 0
    learning_rate = 0    
    sess.run(init_)
    saver_tf = tf.train.Saver({v.op.name: v for v in vars_list})

    while CURRENT_EPOCH < EPOCH: 
            train_batch, tr_label_batch, isfinished_epoch = get_mini_batch(train_dataset, train_label, iteration, train_len) 
            
            for i, value in enumerate(LR_step):
                if value == CURRENT_MINI:
                    learning_rate = LR_rate[i]   
            feed_dict_train = {x_train_ph:train_batch, y_train_ph:tr_label_batch, lr:learning_rate}
            feed_dict_valid = {x_train_ph:valid_dataset, y_train_ph:valid_label}
            try:
                _, loss_tr, _ = sess.run((tr_step,total_loss, accuracy), feed_dict = feed_dict_train )            
                if CURRENT_MINI % UPDATE == 0:
                    loss ,acc = sess.run((total_loss, accuracy), feed_dict = feed_dict_valid)
                    print('Iter:{ITER}, lr:{LR}, Train Loss: {LOSS0}, VAL Loss:{LOSS1}, Accuracy:{ACC}, Time:{TIME}'.format(
                            ITER=CURRENT_MINI, LR=learning_rate, LOSS0='%.04f'%loss_tr, LOSS1='%.04f'%loss, ACC='%.04f'%acc, TIME= datetime.datetime.now()))
                    val_loss_list.append(loss)
                    tr_loss_list.append(loss_tr)
                if CURRENT_MINI % SAVE_UPDATE == 0:
                    if loss < save_val_loss:
                        
                        path_name = os.path.join(os.getcwd(),'MODEL_SAVE')
                        file_name = '-'.join(['TRAIN','2018-07-29']) #%s'%datetime.datetime.now()]))
                        if not os.path.exists(path_name):
                            os.makedirs(path_name)
                        saver_tf.save(sess, os.path.join(path_name,file_name), global_step=CURRENT_MINI)
                        print('saved at step %s, valid loss: %.04f < prev: %.04f to %s'%(CURRENT_MINI, loss, save_val_loss,os.path.join(path_name,file_name)))
                        save_val_loss = loss
            except Exception:
                print(traceback.format_exc())
                print()
                CURRENT_EPOCH += 1 
                iteration = 0
                continue
            
            iteration += 1
            CURRENT_MINI += 1
            
            if isfinished_epoch:
                CURRENT_EPOCH += 1 
                iteration = 0
    file_save = 'MODEL_SAVE/mnist.npy'
    np.save(file_save,{'val_loss_list':val_loss_list,'tr_loss_list':tr_loss_list})
    print('finished!')

    

total_loss, pred_prob, accuracy, tr_step, myGraph, input_ph, label_ph, lr, init_, vars_list = create_graph()
sess = tf.Session(graph = myGraph)
graph_keys = total_loss, pred_prob, accuracy, tr_step, input_ph, label_ph, lr, init_, vars_list

train_graph(sess, input_ph,  label_ph, graph_keys)
 
    
    
    




#print (' '.join(map(str, [random.randint(0,9) for _ in range(len(mnist.validation.images))])))


########################
#        And here      #
########################


# Uncomment to get a prediction number for each image

#result = sess.run(tf.argmax(y,1), feed_dict={x: mnist.validation.images})
#print ' '.join(map(str, result))