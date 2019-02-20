import os 
os.environ['CUDA_VISIBLE_DEVICES'] = "-1"
import sys 
sys.path.append(os.path.dirname(os.path.abspath(os.getcwd())))
import tensorflow as tf 

from train_models.mtcnn_model import P_Net, R_Net, O_Net

def generate_pbtxt():

    for name, net in zip(['P_Net', 'R_Net', 'O_Net'], [P_Net, R_Net, O_Net]):
        tf.reset_default_graph()
        with tf.Graph().as_default() as g:
            if name == 'P_Net':
                input_tf = tf.placeholder(tf.float32, shape=[None, 250, 250, 3], name='input')
            elif name == 'R_Net':
                input_tf = tf.placeholder(tf.float32, shape=[None, 24, 24, 3], name='input')
            elif name == 'O_Net':
                input_tf = tf.placeholder(tf.float32, shape=[None, 48, 48, 3], name='input')

            cls, box, pts = net(input_tf, training=False)
            
            with tf.Session(graph=g) as sess:
                for op in g.get_operations():
                    print(op.values())
                tf.train.write_graph(sess.graph_def, '.', ''.join([name, '.pbtxt']))
                train_writer = tf.summary.FileWriter(name)
                train_writer.add_graph(sess.graph)
                print('saved graph %s'%(''.join([name, '-event'])))
                print('saved %s'%(''.join([name, '.pbtxt'])))


if __name__ == '__main__':
    generate_pbtxt()
            




