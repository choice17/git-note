import tensorflow as tf
from tensorflow.python.client import timeline

import numpy as np
import argparse
import time

def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the 
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    print('loaded file to graph!')
    # Then, we can use again a convenient built-in function to import a graph_def into the 
    # current default Graph
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(
            graph_def, 
            input_map=None, 
            return_elements=None, 
            name="", 
            op_dict=None, 
            producer_op_list=None
        )
    return graph


def profile(args):
    pbfile = args.pb
    if not args.check:
        outputfile = args.o
        if args.image is None:
            inputs = np.random.randint(0,255,args.input_shape)
        else:
            import cv2
            inputs = cv2.imread(args.image)
            if args.input_shape is not None:
                inputs = cv2.resize(inputs, dsize=tuple(args.input_shape[1:3]))
            inputs = inputs[:,:,::-1]
            inputs = np.expand_dims(inputs,0)
        input_ph = args.input_ph
        output_names = args.output_names.split(',')
    
    
    g = load_graph(pbfile)
    with tf.Session(graph=g) as sess:
        if args.check:
            for op in sess.graph.get_operations():
                print(op.name, op.type, op.values())
            return
        # add additional options to trace the session execution
        options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        run_metadata = tf.RunMetadata()
        if args.p is not None:        
            ProfileOptionBuilder = tf.profiler.ProfileOptionBuilder
            opts = ProfileOptionBuilder(ProfileOptionBuilder.time_and_memory()
                ).with_node_names(show_name_regexes=args.p.split(',')).build()
            tf.profiler.profile(
                tf.get_default_graph(),
                run_meta=run_metadata,
                cmd='code',
                options=opts)

            # Print to stdout an analysis of the memory usage and the timing information
            # broken down by operation types.
            tf.profiler.profile(
                tf.get_default_graph(),
                run_meta=run_metadata,
                cmd='op',
                options=tf.profiler.ProfileOptionBuilder.time_and_memory())
            return 
    
        output_tensors  = []
        for i in output_names:
            output_tensors.append(g.get_tensor_by_name(i))
        feed_dict = {input_ph:inputs}
        time_taken = []
        for i in range(args.c):
            ti = time.time()
            output = sess.run(output_tensors, options=options, feed_dict=feed_dict, run_metadata=run_metadata)
            time_taken.append(time.time() - ti)
        print('loop time: {0:d}, min:{1:.4f} max:{2:.4f} average:{3:.4f}'.format( \
                args.c, np.min(time_taken), np.max(time_taken), np.average(time_taken)))
        if type(output) == list:
            #print('checking output')
            #print(output[1][0])
            #print(output[0][0,:5])
            #print(output[2][0,:5])
            #print(output[3][0,:5,:])
            for i in output:
                print('shape:', i.shape)

        else:
            print('checking output')
            print(output.shape)
        # Create the Timeline object, and write it to a json file
        fetched_timeline = timeline.Timeline(run_metadata.step_stats)
        chrome_trace = fetched_timeline.generate_chrome_trace_format()
        print('run timeline saved to %s' % args.o)
        with open(args.o, 'w') as f:
            f.write(chrome_trace)
            
            
    print('finished!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process args for session.')
    parser.add_argument('--pb', type=str, help='pb frozen file')
    parser.add_argument('--o', default='model.json', type=str, help='benchmark json name')
    parser.add_argument('--input_ph', type=str, help='model input ph example """input:0" or "input"""')
    parser.add_argument('--input_shape', type=int, nargs='+', help='input shape ex. -input_shape 1 224 244 3')
    parser.add_argument('--output_names', type=str, help='output names, split with , if multiple outputs')
    parser.add_argument('--check', action='store_true', help='output names, split with , if multiple outputs')
    parser.add_argument('--image', type=str, help='input image')
    parser.add_argument('--p', type=str, help='flag to enable profiling and provide regex str split with , not working now')
    parser.add_argument('--c', default=1, type=int, help='loop times default 1 50 times may be more reliable as sess run need warmup')
    args = parser.parse_args()
    profile(args)
    