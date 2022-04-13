https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html
https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/training.html

# Install TensorFlow:
pip install tensorflow
# Verify it works:
python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
# Install TensorFlow Object Detection API (See above links)
pain in the ass https://github.com/Azure/azure-iot-sdk-python/issues/82

# Windows shortcuts
cd Desktop\python\seraphs-last-stand-aimbots\tensorflow-bot\TensorFlow\models\research
cd Desktop\python\seraphs-last-stand-aimbots\tensorflow-bot\TensorFlow\workspace\training_demo

# Bash shortcuts
cd Desktop/python/seraphs-last-stand-aimbots/tensorflow-bot/TensorFlow/models/research
cd Desktop/python/seraphs-last-stand-aimbots/tensorflow-bot/TensorFlow/workspace/training_demo

# Create train data:
python 03_generate_tfrecord.py -x C:/Users/Puter/Desktop/python/seraphs-last-stand-aimbots/tensorflow-bot/TensorFlow/workspace/training_demo/images/train -l Desktop/python/seraphs-last-stand-aimbots/tensorflow-bot/TensorFlow/workspace/training_demo/annotations/label_map.pbtxt -o Desktop/python/seraphs-last-stand-aimbots/tensorflow-bot/TensorFlow/workspace/training_demo/annotations/train.record

# Create test data:
python 03_generate_tfrecord.py -x C:/Users/Puter/Desktop/python/seraphs-last-stand-aimbots/tensorflow-bot/TensorFlow/workspace/training_demo/images/test -l Desktop/python/seraphs-last-stand-aimbots/tensorflow-bot/TensorFlow/workspace/training_demo/annotations/label_map.pbtxt -o Desktop/python/seraphs-last-stand-aimbots/tensorflow-bot/TensorFlow/workspace/training_demo/annotations/test.record

# Train:
cd Desktop\python\seraphs-last-stand-aimbots\tensorflow-bot\TensorFlow\workspace\training_demo
python 04_model_main_tf2.py --model_dir=models\my_ssd_resnet50_v1_fpn --pipeline_config_path=models\my_ssd_resnet50_v1_fpn\pipeline.config

Fix Numpy error: https://stackoverflow.com/questions/66060487/valueerror-numpy-ndarray-size-changed-may-indicate-binary-incompatibility-exp (Upgrade Numpy)
Fix .dll load error: https://stackoverflow.com/questions/70552632/tensorflow-gpu-cudnn-cnn-infer64-8-dll-not-recognised-error-code-193 (need CUDNN 8.1 (old version) from the docs. Newest CUDA kit is fine.)

# Monitor training:
cd Desktop\python\seraphs-last-stand-aimbots\tensorflow-bot\TensorFlow\workspace\training_demo
tensorboard --logdir=models\my_ssd_resnet50_v1_fpn

my_model_1 Ran for like 8 hours. Loss/total_loss': 0.15672287
my_model Ran for like 7 hours. Loss/total_loss': 0.1492

# Exporting a trained model:
python .\05_exporter_main_v2.py --input_type image_tensor --pipeline_config_path .\models\my_ssd_resnet50_v1_fpn\pipeline.config --trained_checkpoint_dir .\models\my_ssd_resnet50_v1_fpn\ --output_directory .\exported-models\my_model




