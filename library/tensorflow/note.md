# Tensorflow note

## 2.X  

* Remove global variables and scope  
* Redefine model saver  
* Heavily use Keras interface  

## 1.X  

* Graph/Config is inside session
* Node in session graph_def means the edge (tensor)  
* Operations in session.graph.operation means the operation iteself  

* Get node by namescope  
```
sorted([n.name for n in sess.graph_def.node if 'pnet' in n.name]))
```

* Get value by tensor name  
```
sess.run(sess.graph.get_tensor_by_name('pnet/prob1:0'))
```

* Get operation in graph  
```
sorted([op.name for op in sess.graph.get_operations()])
```

* define empty graph  

```
tf.reset_default_graph()
orig_graph = tf.Graph()
with orig_graph as g:
    # define graph
    sess = tf.Session(graph=g, config=config)
```

* freeze session to pb file  

User must convert variable to constant first  
```
g = tf.graph_util.convert_variables_to_constants(
sess,
sess.graph_def,
[i.name.split(':')[0] for i in outs[i]],
variable_names_blacklist=None,
variable_names_whitelist=None)
with tf.gfile.FastGfile('frozen_%s.pb' % name, 'w') as f:
    f.write(g.SerializeToString())
```

* optimize graph to remove training operation  
```
See https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/tools/optimize_for_inference.py

from tensorflow.python.tools import optimize_for_inference_lib

outputGraph = optimize_for_inference_lib.optimize_for_inference(
              inputGraph,
              ["inputTensor"], # an array of the input node(s)
              ["output/softmax"], # an array of output nodes
              tf.int32.as_datatype_enum)
```







