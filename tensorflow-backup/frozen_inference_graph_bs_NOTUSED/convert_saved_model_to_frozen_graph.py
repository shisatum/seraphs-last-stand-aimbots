#import tensorflow as tf
'''
import keras
print(tf.__version__)

from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2

#loaded = tf.saved_model.load('exported-models\my_model\saved_model')
#infer = loaded.signatures['serving_default']
#f = tf.function(infer).get_concrete_function(flatten_input=tf.TensorSpec(shape=[None, 28, 28, 1], dtype=tf.float32))

loaded = keras.models.load_model('exported-models\my_model\saved_model')
f = tf.function(lambda x: loaded(x))
f = f.get_concrete_function(tf.TensorSpec(loaded.inputs[0].shape, loaded.inputs[0].dtype))

f2 = convert_variables_to_constants_v2(f)
graph_def = f2.graph.as_graph_def()

# Export frozen graph
with tf.io.gfile.GFile('frozen_graph.pb', 'wb') as f:
   f.write(graph_def.SerializeToString())
'''
'''
loaded = tf.saved_model.load('exported-models\my_model\saved_model')
infer = loaded.signatures['serving_default']
f = tf.function(infer).get_concrete_function(input_1=tf.TensorSpec(shape=[None, 416, 416, 3], dtype=tf.float32))
f2 = convert_variables_to_constants_v2(f)
graph_def = f2.graph.as_graph_def()

# Export frozen graph
with tf.io.gfile.GFile('frozen_graph.pb', 'wb') as f:
    f.write(graph_def.SerializeToString())
'''
import tensorflow as tf
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2_as_graph
from tensorflow.lite.python.util import run_graph_optimizations, get_grappler_config
import numpy as np

def convert_saved_model_to_pb(output_node_names, input_saved_model_dir, output_graph_dir):
    from tensorflow.python.tools import freeze_graph

    output_node_names = ','.join(output_node_names)

    freeze_graph.freeze_graph(input_graph=None, input_saver=None,
                              input_binary=None,
                              input_checkpoint=None,
                              output_node_names=output_node_names,
                              restore_op_name=None,
                              filename_tensor_name=None,
                              output_graph=output_graph_dir,
                              clear_devices=None,
                              initializer_nodes=None,
                              input_saved_model_dir=input_saved_model_dir)


def save_output_tensor_to_pb():
    output_names = ['StatefulPartitionedCall']
    save_pb_model_path = 'freeze_graph.pb'
    model_dir = 'exported-models/my_model/saved_model'
    convert_saved_model_to_pb(output_names, model_dir, save_pb_model_path)


save_output_tensor_to_pb()
