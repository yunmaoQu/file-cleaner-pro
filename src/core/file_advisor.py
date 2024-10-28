import os
from datetime import datetime

class FileAdvisor:
    def __init__(self, ai_models):
        self.ai_models = ai_models
        self.importance_thresholds = {
            'high': 0.7,
            'medium': 0.4,
            'low': 0.2
        }
    
    def analyze_file_importance(self, file_path):
        """分析文件重要性"""
        try:
            # 获取文件统计信息
            stats = os.stat(file_path)
            
            # 构建特征向量
            features = [
                stats.st_size,  # 文件大小
                stats.st_atime,  # 最后访问时间
                stats.st_mtime,  # 最后修改时间
                stats.st_ctime,  # 创建时间
            ]
            
            # 使用AI模型预测重要性
            importance_score = self.ai_models.importance_model.predict([features])[0][0]
            
            # 确定重要性级别
            importance_level = 'low'
            for level, threshold in self.importance_thresholds.items():
                if importance_score >= threshold:
                    importance_level = level
                    break
            
            return {
                'path': file_path,
                'importance_score': float(importance_score),
                'importance_level': importance_level
            }
        except Exception as e:
            print(f"Error analyzing file importance {file_path}: {str(e)}")
            return None
    
    def generate_recommendations(self, scan_results):
        """生成文件管理建议"""
        recommendations = []
        
        # 分析每个文件的重要性
        for category, files in scan_results['classified_files'].items():
            for file_path in files:
                importance = self.analyze_file_importance(file_path)
                if importance:
                    if importance['importance_level'] == 'high':
                        recommendations.append({
                            'file': file_path,
                            'action': 'backup',
                            'reason': 'High importance file should be backed up'
                        })
                    elif importance['importance_level'] == 'low':
                        recommendations.append({
                            'file': file_path,
                            'action': 'review',
                            'reason': 'Low importance file could be removed'
                        })
        
        # 处理重复文件
        for hash_value, duplicates in scan_results['duplicates'].items():
            recommendations.append({
                'files': duplicates,
                'action': 'remove_duplicates',
                'reason': f'Found {len(duplicates)} duplicate files'
            })
        
        return recommendations