import tensorflow as tf
from typing import Tuple, List, Dict
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from datetime import datetime
import os
import logging
from .models import FileImportanceModel, DuplicateDetectionModel

class ModelTrainer:
    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        self.importance_model = FileImportanceModel()
        self.duplicate_model = DuplicateDetectionModel()
        self.logger = logging.getLogger(__name__)

    def train_importance_model(self, training_data: List[Dict]) -> Dict[str, float]:
        """训练文件重要性模型"""
        try:
            # 准备训练数据
            X = np.array([
                self.importance_model.prepare_features(item['file_info'])
                for item in training_data
            ])
            y = np.array([item['importance_label'] for item in training_data])

            # 分割训练集和验证集
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # 训练模型
            history = self.importance_model.model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val),
                epochs=50,
                batch_size=32,
                callbacks=[
                    tf.keras.callbacks.EarlyStopping(
                        patience=5,
                        restore_best_weights=True
                    )
                ]
            )

            # 保存模型
            model_path = os.path.join(
                self.model_dir,
                f'importance_model_{datetime.now().strftime("%Y%m%d_%H%M%S")}.h5'
            )
            self.importance_model.model.save(model_path)

            # 返回训练结果
            return {
                'val_accuracy': float(max(history.history['val_accuracy'])),
                'val_loss': float(min(history.history['val_loss'])),
                'model_path': model_path
            }

        except Exception as e:
            self.logger.error(f"Importance model training failed: {str(e)}")
            raise

    def train_duplicate_model(self, image_pairs: List[Tuple[str, str, float]]) -> Dict[str, float]:
        """训练图像相似度模型"""
        try:
            # 准备训练数据
            pairs_data = []
            labels = []

            for img1_path, img2_path, similarity in image_pairs:
                try:
                    # 提取特征
                    features1 = self._load_and_extract_features(img1_path)
                    features2 = self._load_and_extract_features(img2_path)
                    
                    if features1 is not None and features2 is not None:
                        pairs_data.append((features1, features2))
                        labels.append(similarity)
                except Exception as e:
                    self.logger.warning(f"Failed to process image pair: {str(e)}")
                    continue

            if not pairs_data:
                raise ValueError("No valid training data available")

            # 转换为numpy数组
            X1 = np.array([pair[0] for pair in pairs_data])
            X2 = np.array([pair[1] for pair in pairs_data])
            y = np.array(labels)

            # 构建孪生网络
            siamese_model = self._build_siamese_network()

            # 分割训练集和验证集
            X1_train, X1_val, X2_train, X2_val, y_train, y_val = train_test_split(
                X1, X2, y, test_size=0.2, random_state=42
            )

            # 训练模型
            history = siamese_model.fit(
                [X1_train, X2_train],
                y_train,
                validation_data=([X1_val, X2_val], y_val),
                epochs=30,
                batch_size=32,
                callbacks=[
                    tf.keras.callbacks.EarlyStopping(
                        patience=5,
                        restore_best_weights=True
                    )
                ]
            )

            # 保存模型
            model_path = os.path.join(
                self.model_dir,
                f'duplicate_model_{datetime.now().strftime("%Y%m%d_%H%M%S")}.h5'
            )
            siamese_model.save(model_path)

            return {
                'val_accuracy': float(max(history.history['val_accuracy'])),
                'val_loss': float(min(history.history['val_loss'])),
                'model_path': model_path
            }

        except Exception as e:
            self.logger.error(f"Duplicate model training failed: {str(e)}")
            raise

    def _build_siamese_network(self) -> tf.keras.Model:
        """构建孪生网络"""
        input_shape = (128,)  # 特征向量维度

        # 定义共享网络
        shared_network = tf.keras.Sequential([
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(32, activation='relu')
        ])

        # 输入层
        input_a = layers.Input(shape=input_shape)
        input_b = layers.Input(shape=input_shape)

        # 处理两个输入
        processed_a = shared_network(input_a)
        processed_b = shared_network(input_b)

        # 计算相似度
        distance = layers.Lambda(
            lambda x: tf.keras.backend.abs(x[0] - x[1])
        )([processed_a, processed_b])

        # 输出层
        outputs = layers.Dense(1, activation='sigmoid')(distance)

        # 构建模型
        model = tf.keras.Model(inputs=[input_a, input_b], outputs=outputs)
        
        # 编译模型
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        return model

    def _load_and_extract_features(self, image_path: str) -> np.ndarray:
        """加载图像并提取特征"""
        try:
            image = tf.keras.preprocessing.image.load_img(
                image_path,
                target_size=(224, 224)
            )
            image_array = tf.keras.preprocessing.image.img_to_array(image)
            return self.duplicate_model.extract_features(image_array)
        except Exception as e:
            self.logger.error(f"Feature extraction failed for {image_path}: {str(e)}")
            return None

    def evaluate_models(self, test_data: Dict) -> Dict[str, Any]:
        """评估模型性能"""
        results = {
            'importance_model': {},
            'duplicate_model': {}
        }

        try:
            # 评估重要性模型
            if 'importance_test_data' in test_data:
                X_test = np.array([
                    self.importance_model.prepare_features(item['file_info'])
                    for item in test_data['importance_test_data']
                ])
                y_test = np.array([
                    item['importance_label']
                    for item in test_data['importance_test_data']
                ])
                
                importance_scores = self.importance_model.model.evaluate(X_test, y_test)
                results['importance_model'] = {
                    'test_loss': float(importance_scores[0]),
                    'test_accuracy': float(importance_scores[1])
                }

            # 评估相似度模型
            if 'duplicate_test_data' in test_data:
                test_pairs = test_data['duplicate_test_data']
                X1_test = []
                X2_test = []
                y_test = []

                for img1_path, img2_path, similarity in test_pairs:
                    features1 = self._load_and_extract_features(img1_path)
                    features2 = self._load_and_extract_features(img2_path)
                    if features1 is not None and features2 is not None:
                        X1_test.append(features1)
                        X2_test.append(features2)
                        y_test.append(similarity)

                if X1_test:
                    siamese_model = self._build_siamese_network()
                    duplicate_scores = siamese_model.evaluate(
                        [np.array(X1_test), np.array(X2_test)],
                        np.array(y_test)
                    )
                    results['duplicate_model'] = {
                        'test_loss': float(duplicate_scores[0]),
                        'test_accuracy': float(duplicate_scores[1])
                    }

        except Exception as e:
            self.logger.error(f"Model evaluation failed: {str(e)}")

        return results

    def save_training_metrics(self, metrics: Dict[str, Any]):
        """保存训练指标"""
        try:
            metrics_path = os.path.join(
                self.model_dir,
                f'training_metrics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            )
            with open(metrics_path, 'w') as f:
                json.dump(metrics, f, indent=4)
            
            self.logger.info(f"Training metrics saved to {metrics_path}")
        except Exception as e:
            self.logger.error(f"Failed to save training metrics: {str(e)}")