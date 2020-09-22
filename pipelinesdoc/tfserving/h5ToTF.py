from keras import backend as K
from keras.models import load_model
import tensorflow as tf

# 首先使用tf.keras的load_model来导入模型h5文件
model_path = 'v7_resnet50_19-0.9068-0.8000.h5'
model = tf.keras.models.load_model(model_path, custom_objects=dependencies)
model.save('models/resnet/', save_format='tf')  # 导出tf格式的模型文件