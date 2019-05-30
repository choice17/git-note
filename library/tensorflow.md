# Tensorflow  

## content  
* **[intro](#intro)**  
* **[tools](#tools)**  
* **[lite](#lite)**  
* **[minimum_example](#minimumexample)**  


## intro

## abstractworkflow  

```
1. create graph  
1.1 create variables   
1.2 create graph network   
1.3 return I/O  
1.4 setup tensorboard summary   
2. create training graph   
2.1 get the O from graph   
2.2 create loss and optimizer    
2.3 mark logs and ckpt    
3. evaluation   
3.1 open tensorboard    
```

## variable  

`tf.Variable`   
`tf.get_variable`   

## placeholder 
`tf.placeholder`  

## initializer  

## constant 

## namescope  

## varscope  

## graph  

## graphdef 

## tfrecord  

## sess  
```python
with tf.Session(graph=graph) as sess:
	result = sess.run((val), feed_dict={})
```

## ops  
`matmul`  
`softmax`  
`conv2d`  
`reshape`  
`flatten`  
`max_pool`  
`avg_pool`  
`concat`   
`top_k`  
`cast`  
`reduce_mean`  
`reduce_sum` 

## train  

`softmax_with_logits_v2`  
`softmax_with_logits`  
`regularization`  
`online hard sample mining`   
`adam`
`gradientdescent`
`momentum`

## slim 

## tensorboard  

`summary`
`summary.merge`
`summary.histogram`
`sess.graph_def`

## ckpt  

## freezegraph 

## optimizegraph  

## porting  

## tools
[profiling](../files/tensorflow_tools/profiling_tool.py)

## lite  

typical workflow 

* Method 1. for floating point inference  
```
1. freeze graph from .pbtxt and .ckpt 
2. toco convert .pb to .tflite
```

* Method 2. for fixed point inference  
```
1. at training graph, add tf.contrib.quant.create_train_graph()
2. save .ckpt 
3. re declare graph and add tf.contrib.quant.create_eval_graph() and load the ckpt sess
4. freeze graph
5. toco convert .pb to tflite
```

* cross compile  
checkout tensorflow branch r1.11, and work on `tensorflow/tensorflow/contrib/lite/tools/make/Makefile`

* benchmark  
checkout `tensorflow/tensorflow/contrib/lite/tools/benchmark` note your have to build with -DWITH_PROFLIING_ENABLED 

* proj
checkout `tensorflow/tensorflow/contrib/lite/examples/label_image`


## minimumexample  

[example](./tensorflow/minimum.py)

