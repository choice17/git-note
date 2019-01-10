"""Print frozen network to dot file
Reference: 
https://github.com/tensorflow/tensorflow/blob/master/tensorflow/tools/quantization/graph_to_dot.python

Objective: load .pb/.pbtxt and generate .dot file 
@ input: .pb/ .pbtxt file path
@ output: .dot file

dot file to png/pdf
$ dot -Tpng <file>.dot -o <outputfile>.png
$ dot -Tpdf <file>.dot -o <outputfile>.pdf

author: tcyu@umich.edu
"""
from google.protobuf import text_format 
from tensorflow.core.framework import graph_pb2
from tensorflow.python.platform import gfile 
import tensorflow as tf 

import sys 
import re

def loadpb(fname):
    #gdef = graph_pb2.GraphDef()
    gdef = tf.GraphDef()
    with open(fname, "rb") as f:
        gdef.ParseFromString(f.read())
    return gdef
        
def loadpbtxt(fname):
    gdef = tf.GraphDef()
    with open(fname, "r") as f:
        gstr = f.read()
        text_format.Parse(gstr, gdef)
    return gdef


def main(fname):

    f_name, f_ext = fname.split('.')
    if not gfile.Exists(fname):
        print("input graph file {} is not exists".format(fname))
        return -1
    if fname.split('.')[-1] == 'pb':
        gdef = loadpb(fname)
    elif fname.split('.')[-1] == 'pbtxt':
        gdef = loadpbtxt(fname)

    with open(f_name + '.dot', "w") as f:
        print("digraph graphname {", file=f)
        print("  node [shape=record]", file=f)
        for node in gdef.node:
            output_name = node.name
            if node.op == 'Const':
                print("  \"" + output_name + "\" [gradientangle=\"90\", style=filled, fillcolor=\"white;0.5:green\", label=\"{" 
                + output_name + " | " + node.op + ' {}'.format([i.size for i in node.attr['value'].tensor.tensor_shape.dim]) + "}\"];", file=f)
            elif node.op == 'Placeholder':
                print("  \"" + output_name + "\" [gradientangle=\"90\", style=filled, fillcolor=\"white;0.5:green\", label=\"{" 
                + output_name + " | " + node.op + ' {}'.format([i.size for i in node.attr['shape'].shape.dim]) + "}\"];", file=f)
            else:
                print("  \"" + output_name + "\" [gradientangle=\"90\", style=filled, fillcolor=\"white;0.5:yellow\", label=\"{" 
                + output_name + " | " + node.op + "}\"];", file=f)

            for input_full_name in node.input:
                parts = input_full_name.split(":")
                input_name = re.sub(r"^\^", "", parts[0])
                print("  \"" + input_name + "\" -> \"" + output_name + "\";", file=f)
        print("}", file=f)
    print("Created DOT file '" + f_name + '.dot' + "'.")

    g = tf.Graph()
    with tf.Graph().as_default() as g:
        tf.import_graph_def(gdef)
        with tf.Session(graph=g) as sess:
            for op in g.get_operations():
                if op.type == 'Const':
                    print(op.values, op.outputs[0].get_shape())
                else:
                    print(op.values)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Input .pb or .pbtxt file path")
    fname = sys.argv[1]
    main(fname)

