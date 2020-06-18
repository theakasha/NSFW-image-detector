import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model('nsfw_model')
tflite_model = converter.convert()
open("converted_nsfw_model.tflite", "wb").write(tflite_model)

