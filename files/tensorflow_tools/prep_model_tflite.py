''' 
https://gist.github.com/omimo/5d393ed5b64d2ca0c591e4da04af6009

- reference 1. https://stackoverflow.com/questions/45382917/how-to-optimize-for-inference-a-simple-saved-tensorflow-1-0-1-graph freeze and optimize

- reference 2. https://www.tensorflow.org/mobile/tflite/devguide freeze graph and toco
- referebce 3. - python tensorflow/python/tools/import_pb_to_tensorboard.py --model_dir resnetv1_50.pb --log_dir /tmp/tensorboard
- reference 4. toco_convert protos https://www.tensorflow.org/versions/r1.5/api_docs/python/tf/contrib/lite/toco_convert
'''
import sys
import tensorflow as tf 
from tensorflow.python.tools import freeze_graph 
from tensorflow.python.tools import optimize_for_inference_lib 


from tensorflow.core.framework import graph_pb2 as gdb
from google.protobuf import text_format as pbtf

def freeze_and_optimize_graph(model_name,
                              input_graph_path,
                              ckpt_path,
                              input_nodes,
                              output_nodes):
    
    MODEL_NAME = model_name
    
    
    # freeze_graph
    
    input_saver_def_path = ''
    input_binary = False 
    restore_op_name = "save/restore_all"
    filename_tensor_name = "save/Const:0"
    output_frozen_graph_name = 'frozen_' + MODEL_NAME + '.pb'
    output_optimized_graph_name = 'optimize_' + MODEL_NAME + '.pb'
    clear_device = True 
    
    '''//=======================display variable info====================='''
    tf.reset_default_graph()
    with open(input_graph_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_str = f.read()
        pbtf.Parse(graph_str, graph_def)
    with tf.Graph().as_default() as g:
        tf.import_graph_def(graph_def)
        with tf.Session(graph=g) as sess:
            ops = sess.graph.get_operations()
            print('=============%s==Graph def==============================' % model_name)
            for op in ops:
                if op.type in ['Placeholder', 'VariableV2']:
                    for j in op.outputs:
                        print(op.name, j.get_shape())   
            print('=============%s==meta data============================' % model_name)
            saver_tf = tf.train.import_meta_graph(ckpt_path+'.meta')#Saver(vars_list)
            saver_tf.restore(sess, ckpt_path)
            for op in tf.get_collection(tf.GraphKeys.VARIABLES):
                print(op.name, op.shape)
    '''=======================display variable info=====================//'''

    # 1. freeze graph
    freeze_graph.freeze_graph(input_graph_path,
                              input_saver_def_path,
                              input_binary,
                              ckpt_path,
                              output_nodes,
                              restore_op_name,
                              filename_tensor_name,
                              output_frozen_graph_name,
                              clear_device,
                              "")
    
    # Optimize for inference
    input_graph_def = tf.GraphDef()
    with tf.gfile.Open(output_frozen_graph_name, "rb") as f:
        data = f.read()
        input_graph_def.ParseFromString(data)
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(input_graph_def, name='')


    # get tensor name
    x = graph.get_tensor_by_name(input_nodes[0] + ":0")
    y = []
    for outputname in output_nodes.split(','):
        y.append(graph.get_tensor_by_name(outputname + ":0"))

    with tf.Session(graph=graph) as sess:
        a,b= tf.contrib.lite.build_toco_convert_protos(sess.graph_def,
                                    [x], 
                                    y,
                                    input_format=tf.contrib.lite.constants.TENSORFLOW_GRAPHDEF,
                                    output_format=tf.contrib.lite.constants.TFLITE
                                    )
                                    '''quantized_input_stats=None, #only neede for QUANTIZED_UINT8
                                    default_ranges_stats=None,
                                    drop_control_dependency=True,
                                    reorder_across_fake_quant=False,
                                    allow_custom_ops=False,
                                    change_concat_input_ranges=False,
                                    quantize_weights=False'''
        tflite_model = tf.contrib.lite.toco_convert(sess.graph_def,
                                    [x], 
                                    y)
                                    '''inference_type=tf.contrib.lite.constants.FLOAT,
                                    input_format=tf.contrib.lite.constants.TENSORFLOW_GRAPHDEF,
                                    output_format=tf.contrib.lite.constants.TFLITE,
                                    quantized_input_stats=None, #only neede for QUANTIZED_UINT8
                                    default_range_stats=None,
                                    drop_control_dependency=True,
                                    reorder_across_fake_quant=False,
                                    allow_custom_ops=False,
                                    change_concat_input_ranges=False,
                                    quantize_weights=False,'''
                                    ) 


    # 2. optimize graph
    '''output_graph_def = optimize_for_inference_lib.optimize_for_inference(
            input_graph_def,
            input_nodes, # as array of input nodes
            output_nodes.split(','), # as arrat of output nodes
            tf.float32.as_datatype_enum)


    # 3. transform 
    #from tensorflow.python.framework import dtypes
    #from tensorflow.python.framework import tensor_util
    #from tensorflow.python.platform import test
    from tensorflow.tools.graph_transforms import TransformGraph

    out_graph='transform_' + output_frozen_graph_name
    tranform_graph = TransformGraph(input_graph_def=output_graph_def,
                                #out_graph='transform_' + output_frozen_graph_name,
                                inputs=input_nodes,
                                outputs=output_nodes.split(','),
                                transforms=['add_default_attributes',
                                            'strip_unused_nodes',
                                            'remove_nodes(op=Identity,op=CheckNumerics)',
                                            'fold_constants(ignore_errors=true)',
                                            'fold_batch_norms',
                                            'quantize_weights',
                                            'quantize_nodes',
                                            'sort_by_execution_order'])
                       

    
    

    # Save the optimized graph  
    
    with tf.gfile.FastGFile(output_optimized_graph_name, "w") as f:
        f.write(output_graph_def.SerializeToString())
    with tf.gfile.FastGFile(out_graph, "w") as f:
        f.write(tranform_graph.SerializeToString())
    print('save frozen model to %s' % output_frozen_graph_name)
    print('saved optimized model to %s'% output_optimized_graph_name)
    print('saved transformed model to %s'% out_graph)'''

if __name__ == '__main__':
    freeze_and_optimize_graph(model_name="PNet",
                              input_graph_path="P_Net.pbtxt",
                              ckpt_path="../data/MTCNN_model_0807/PNet_landmark/PNet-22",
                              input_nodes=["input"],
                              output_nodes="cls_prob,bbox_pred,landmark_pred")
    freeze_and_optimize_graph(model_name="RNet",
                              input_graph_path="R_Net.pbtxt",
                              ckpt_path="../data/MTCNN_model_0807/RNet_landmark/RNet-16",
                              input_nodes=["input"],
                              output_nodes="cls_fc/Softmax,bbox_fc/BiasAdd,landmark_fc/BiasAdd")
    freeze_and_optimize_graph(model_name="ONet",
                              input_graph_path="O_Net.pbtxt",
                              ckpt_path="../data/MTCNN_model_0807/ONet_landmark/ONet-14",
                              input_nodes=["input"],
                              output_nodes="cls_fc/Softmax,bbox_fc/BiasAdd,landmark_fc/BiasAdd")





