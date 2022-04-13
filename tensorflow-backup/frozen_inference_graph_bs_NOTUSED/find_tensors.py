import tensorflow as tf
'''
with tf.io.gfile.GFile("freeze_graph.pb", "rb") as f:
#with tf.compat.v2.io.gfile.GFile("freeze_graph.pb", "rb") as f:
  graph_def = tf.compat.v1.GraphDef()
  graph_def.ParseFromString(f.read())

with tf.Graph().as_default() as graph:
  tf.import_graph_def(graph_def)

for op in graph.get_operations():
  print(op.name, [inp for inp in op.inputs])
'''


def load_model():
    with tf.io.gfile.GFile(path, "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())

    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name="")
    return graph

if __name__=='__main__':
    path = "exported-models/my_model/saved_model/saved_model.pb"
    graph = load_model()
    with tf.Session(graph=graph) as sess:
        for op in graph.get_operations():
            print(op.name)


'''
def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the 
    # unserialized graph_def
    with tf.io.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and return it 
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="prefix")
    return graph

graph = load_graph('freeze_graph.pb')

k = 0
for op in graph.get_operations(): 
    k += 1
    print('{}:\tOut name: {}\n'.format(k, op.name))
'''
