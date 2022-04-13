##### The following is the old method. Never got this to work. 
Might need later:
xml_to_csv.py: https://gist.github.com/iKhushPatel/ed1f837656b155d9b94d45b42e00f5e4
create_tfrecord.py updates: https://gist.github.com/iKhushPatel/5614a36f26cf6459cc49c8248e8b5b48

Now we need a frozen graph file.

"I found a solution, just convert saved_model.pb to frozen_graph.pb."
https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/tools/freeze_graph.py

python freeze_graph.py --input_graph=exported-models\my_model\saved_model\saved_model.pb --input_checkpoint=exported-models\my_model\checkpoint\ckpt-0 --output_graph=exported-models\my_model\frozen_graph.pb

! Not working. Possible issue, need to use Tensorflow instead of OpenCV: https://forum.opencv.org/t/cant-open-pb-in-cv-readnetfromtensorflow/360/7
Or import and save with keras then use OpenCV?

Frozen graphs are apparently deprecated in TF2

Found original tutorial that I used for the tensorflow-test on the city street images: https://jeanvitor.com/tensorflow-object-detecion-opencv/
Going to try script from here to create frozen graph pbtxt.

! Found solution to create frozen graph: https://github.com/tensorflow/tensorflow/issues/46740
epsilon11101 commented on Apr 27, 2021 with a new script to convert saved model to frozen graph. 

# Converting saved model to frozen graph:
python convert_saved_model_to_frozen_graph.py

[] Alternate methods to save model and freeze graph: https://stackoverflow.com/questions/45382917/how-to-optimize-for-inference-a-simple-saved-tensorflow-1-0-1-graph

Move new file 'freeze_graph.pb' from main dir to exported-models/my_model/

# Now we need to create pbtxt file:
python generate_pbtxt.py --input=freeze_graph.pb --output=textgraph.pbtxt --config=exported-models\my_model\pipeline.config

error. maybe need to optimize frozen graph? https://stackoverflow.com/questions/45382917/how-to-optimize-for-inference-a-simple-saved-tensorflow-1-0-1-graph

# Find tensors on freeze graph (input/output names for next command)
python find_tensors.py

! Alternate create freeze graph:
python -m tensorflow.python.tools.freeze_graph --input_graph exported-models\my_model\saved_model\saved_model.pb --input_checkpoint exported-models\my_model\checkpoint\ckpt-0 --output_graph freeze_graph_2.pb --output_node_names=y

# Optimize frozen graph for inference:
python -m tensorflow.python.tools.optimize_for_inference --input freeze_graph.pb --output graph_optimized.pb --input_names="Placeholder" --output_names="final_result"
python -m tensorflow.python.tools.optimize_for_inference --input freeze_graph.pb --output graph_optimized.pb --input_names="Mul" --output_names="Softmax"
