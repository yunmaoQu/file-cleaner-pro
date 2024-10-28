import tensorflow as tf
import numpy as np
from PIL import Image

class AIModels:
    def __init__(self):
        self.image_model = None
        self.importance_model = None
        self.load_models()
    
    def load_models(self):
        try:
            # 加载预训练的图像识别模型
            self.image_model = tf.keras.applications.MobileNetV2(
                weights='imagenet',
                include_top=False
            )
            
            # 加载文件重要性评估模型
            # 这里使用简单的示例模型，实际应用中需要训练专门的模型
            self.importance_model = tf.keras.Sequential([
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dense(32, activation='relu'),
                tf.keras.layers.Dense(1, activation='sigmoid')
            ])
        except Exception as e:
            print(f"Error loading models: {str(e)}")
    
    def get_image_features(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((224, 224))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
            img_array = np.expand_dims(img_array, axis=0)
            features = self.image_model.predict(img_array)
            return features.flatten()
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None