import tensorflow as tf 
import sys
from google.protobuf import text_format as pbtf
from tensorflow.core.framework import graph_pb2
import os

def save_event_pbtxt(in_, logdir):
    gdef = tf.GraphDef()
    with open(in_, 'r') as f:
        gstr = f.read()
        pbtf.Parse(gstr, gdef)
        with tf.Graph().as_default() as g:
            tf.import_graph_def(gdef)
            with tf.Session(graph=g) as sess:
                writer = tf.summary.FileWriter(logdir)
                writer.add_graph(sess.graph)


def save_event_pb(in_, logdir):
    with open(in_, 'rb') as f:
        gdef = graph_pb2.GraphDef()
        gdef.ParseFromString(f.read())
        with tf.Graph().as_default() as g:
            tf.import_graph_def(gdef)
            with tf.Session(graph=g) as sess:
                writer = tf.summary.FileWriter(logdir)
                writer.add_graph(sess.graph)

def main(in_):
    logdir = 'log_graph'
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    if in_.split('.')[-1] == 'pbtxt':
        save_event_pbtxt(in_, logdir)
    elif in_.split('.')[-1] == 'pb':
        save_event_pb(in_, logdir)

if __name__ == '__main__':
    fname = sys.argv[1]
    main(fname)
