
import tensorflow as tf
from tensorflow.keras import layers, models
from typing import Tuple, List
import numpy as np
from config.settings import AI_CONFIG

class FileImportanceModel:
    def __init__(self):
        self.model = self._build_model()
        self.input_size = AI_CONFIG['input_size']
        self.batch_size = AI_CONFIG['batch_size']

    def _build_model(self) -> models.Model:
        """构建文件重要性评估模型"""
        model = models.Sequential([
            layers.Dense(128, activation='relu', input_shape=(10,)),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model

    def prepare_features(self, file_info: dict) -> np.ndarray:
        """准备文件特征"""
        features = [
            file_info.get('size', 0) / 1e6,  # 文件大小（MB）
            file_info.get('access_count', 0),  # 访问次数
            file_info.get('last_access_days', 0),  # 最后访问距今天数
            file_info.get('creation_days', 0),  # 创建距今天数
            file_info.get('modification_days', 0),  # 最后修改距今天数
            file_info.get('is_system_file', 0),  # 是否系统文件
            file_info.get('is_hidden', 0),  # 是否隐藏文件
            file_info.get('is_temporary', 0),  # 是否临时文件
            file_info.get('has_similar', 0),  # 是否有相似文件
            file_info.get('extension_importance', 0),  # 文件扩展名重要性
        ]
        return np.array(features, dtype=np.float32)

class DuplicateDetectionModel:
    def __init__(self):
        self.model = self._build_model()

    def _build_model(self) -> models.Model:
        """构建文件相似度检测模型"""
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=False,
            weights='imagenet'
        )
        
        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(1024, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(512, activation='relu'),
            layers.Dense(128, activation='relu')
        ])
        
        return model

    def extract_features(self, image: np.ndarray) -> np.ndarray:
        """提取图像特征"""
        image = tf.image.resize(image, (224, 224))
        image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
        features = self.model.predict(np.expand_dims(image, axis=0))
        return features[0]

class ContentAnalysisModel:
    def __init__(self):
        self.importance_model = FileImportanceModel()
        self.duplicate_model = DuplicateDetectionModel()
        self.logger = logging.getLogger(__name__)

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """分析文件内容和重要性"""
        try:
            # 获取文件基本信息
            file_info = self._get_file_info(file_path)
            
            # 评估文件重要性
            importance_features = self.importance_model.prepare_features(file_info)
            importance_score = self.importance_model.model.predict(
                np.expand_dims(importance_features, axis=0)
            )[0][0]
            
            # 如果是图像文件，进行相似度分析
            if self._is_image_file(file_path):
                image_features = self._extract_image_features(file_path)
                file_info['image_features'] = image_features.tolist()
            
            return {
                'path': file_path,
                'importance_score': float(importance_score),
                'file_info': file_info
            }
            
        except Exception as e:
            self.logger.error(f"File analysis failed for {file_path}: {str(e)}")
            return None

    def _get_file_info(self, file_path: str) -> Dict[str, Any]:
        """获取文件详细信息"""
        stats = os.stat(file_path)
        current_time = time.time()
        
        return {
            'size': stats.st_size,
            'access_count': 0,  # 需要额外跟踪
            'last_access_days': (current_time - stats.st_atime) / (24 * 3600),
            'creation_days': (current_time - stats.st_ctime) / (24 * 3600),
            'modification_days': (current_time - stats.st_mtime) / (24 * 3600),
            'is_system_file': self._is_system_file(file_path),
            'is_hidden': self._is_hidden_file(file_path),
            'is_temporary': self._is_temporary_file(file_path),
            'has_similar': False,  # 需要后续分析
            'extension_importance': self._get_extension_importance(file_path)
        }

    @staticmethod
    def _is_image_file(file_path: str) -> bool:
        """检查是否为图像文件"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        return os.path.splitext(file_path)[1].lower() in image_extensions

    @staticmethod
    def _is_system_file(file_path: str) -> bool:
        """检查是否为系统文件"""
        system_patterns = {
            'thumbs.db',
            '.ds_store',
            'desktop.ini',
            'system volume information'
        }
        return os.path.basename(file_path).lower() in system_patterns

    @staticmethod
    def _is_hidden_file(file_path: str) -> bool:
        """检查是否为隐藏文件"""
        return os.path.basename(file_path).startswith('.')

    @staticmethod
    def _is_temporary_file(file_path: str) -> bool:
        """检查是否为临时文件"""
        temp_patterns = {'.tmp', '.temp', '~', '.bak'}
        return any(file_path.lower().endswith(pat) for pat in temp_patterns)

    def _get_extension_importance(self, file_path: str) -> float:
        """获取文件扩展名的重要性权重"""
        extension_weights = {
            '.doc': 0.8, '.docx': 0.8, '.pdf': 0.9,
            '.jpg': 0.7, '.png': 0.7,
            '.mp4': 0.8, '.mov': 0.8,
            '.tmp': 0.1, '.temp': 0.1,
            '.txt': 0.5
        }
        ext = os.path.splitext(file_path)[1].lower()
        return extension_weights.get(ext, 0.5)

    def _extract_image_features(self, image_path: str) -> np.ndarray:
        """提取图像特征"""
        try:
            image = tf.keras.preprocessing.image.load_img(
                image_path,
                target_size=(224, 224)
            )
            image_array = tf.keras.preprocessing.image.img_to_array(image)
            return self.duplicate_model.extract_features(image_array)
        except Exception as e:
            self.logger.error(f"Image feature extraction failed: {str(e)}")
            return np.zeros(128)  # 返回零向量作为默认特征