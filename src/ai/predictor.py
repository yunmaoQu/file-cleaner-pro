import tensorflow as tf
import numpy as np
from typing import List, Dict, Any
import logging
from .models import FileImportanceModel, DuplicateDetectionModel

class FilePredictor:
    def __init__(self, importance_model_path: str, duplicate_model_path: str):
        self.importance_model = FileImportanceModel()
        self.duplicate_model = DuplicateDetectionModel()
        self.logger = logging.getLogger(__name__)
        
        # 加载预训练模型
        try:
            self.importance_model.model = tf.keras.models.load_model(importance_model_path)
            self.duplicate_model.model = tf.keras.models.load_model(duplicate_model_path)
        except Exception as e:
            self.logger.error(f"Failed to load models: {str(e)}")
            raise

    def predict_file_importance(self, file_info: Dict[str, Any]) -> float:
        """预测文件重要性"""
        try:
            features = self.importance_model.prepare_features(file_info)
            importance_score = self.importance_model.model.predict(
                np.expand_dims(features, axis=0)
            )[0][0]
            return float(importance_score)
        except Exception as e:
            self.logger.error(f"Importance prediction failed: {str(e)}")
            return 0.5  # 返回默认中等重要性

    def find_similar_files(self, 
                         target_features: np.ndarray, 
                         candidate_features: List[np.ndarray],
                         threshold: float = 0.8) -> List[Tuple[int, float]]:
        """查找相似文件"""
        try:
            similar_files = []
            for idx, features in enumerate(candidate_features):
                similarity = self.compute_similarity(target_features, features)
                if similarity >= threshold:
                    similar_files.append((idx, float(similarity)))
            return sorted(similar_files, key=lambda x: x[1], reverse=True)
        except Exception as e:
            self.logger.error(f"Similar file detection failed: {str(e)}")
            return []

    def compute_similarity(self, features1: np.ndarray, features2: np.ndarray) -> float:
        """计算两个文件的相似度"""
        try:
            # 使用余弦相似度
            similarity = np.dot(features1, features2) / (
                np.linalg.norm(features1) * np.linalg.norm(features2)
            )
            return float(similarity)
        except Exception as e:
            self.logger.error(f"Similarity computation failed: {str(e)}")
            return 0.0

    def batch_predict_importance(self, file_infos: List[Dict[str, Any]]) -> List[float]:
        """批量预测文件重要性"""
        try:
            features_batch = np.array([
                self.importance_model.prepare_features(info)
                for info in file_infos
            ])
            importance_scores = self.importance_model.model.predict(features_batch)
            return [float(score) for score in importance_scores]
        except Exception as e:
            self.logger.error(f"Batch importance prediction failed: {str(e)}")
            return [0.5] * len(file_infos)

    def analyze_directory(self, file_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析目录中的所有文件"""
        try:
            results = {
                'importance_scores': [],
                'similar_groups': [],
                'statistics': {
                    'total_files': len(file_list),
                    'important_files': 0,
                    'duplicate_groups': 0
                }
            }

            # 预测重要性
            importance_scores = self.batch_predict_importance(file_list)
            results['importance_scores'] = importance_scores

            # 统计重要文件
            important_files = sum(1 for score in importance_scores if score > 0.7)
            results['statistics']['important_files'] = important_files

            # 查找相似文件组
            image_files = [
                (idx, file_info) for idx, file_info in enumerate(file_list)
                if self._is_image_file(file_info['path'])
            ]

            if image_files:
                similar_groups = self._find_similar_groups(image_files)
                results['similar_groups'] = similar_groups
                results['statistics']['duplicate_groups'] = len(similar_groups)

            return results

        except Exception as e:
            self.logger.error(f"Directory analysis failed: {str(e)}")
            return {
                'importance_scores': [],
                'similar_groups': [],
                'statistics': {
                    'total_files': 0,
                    'important_files': 0,
                    'duplicate_groups': 0
                },
                'error': str(e)
            }

    def _find_similar_groups(self, image_files: List[Tuple[int, Dict]]) -> List[List[Tuple[int, float]]]:
        """查找相似图片组"""
        try:
            similar_groups = []
            processed_indices = set()

            for idx1, (file_idx1, file_info1) in enumerate(image_files):
                if file_idx1 in processed_indices:
                    continue

                # 提取特征
                features1 = self._extract_image_features(file_info1['path'])
                if features1 is None:
                    continue

                # 查找相似文件
                current_group = []
                for idx2, (file_idx2, file_info2) in enumerate(image_files[idx1 + 1:]):
                    if file_idx2 in processed_indices:
                        continue

                    features2 = self._extract_image_features(file_info2['path'])
                    if features2 is None:
                        continue

                    similarity = self.compute_similarity(features1, features2)
                    if similarity >= 0.8:  # 相似度阈值
                        current_group.append((file_idx2, float(similarity)))
                        processed_indices.add(file_idx2)

                if current_group:
                    current_group.insert(0, (file_idx1, 1.0))  # 添加原始文件
                    similar_groups.append(current_group)
                    processed_indices.add(file_idx1)

            return similar_groups

        except Exception as e:
            self.logger.error(f"Similar group detection failed: {str(e)}")
            return []

    def _extract_image_features(self, image_path: str) -> Optional[np.ndarray]:
        """提取图像特征"""
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

    @staticmethod
    def _is_image_file(file_path: str) -> bool:
        """检查是否为图像文件"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        return os.path.splitext(file_path)[1].lower() in image_extensions