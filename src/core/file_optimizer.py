from PIL import Image
import os

class FileOptimizer:
    def __init__(self):
        self.compression_quality = {
            'high': 85,
            'medium': 60,
            'low': 40
        }
    
    def optimize_image(self, image_path, quality='medium'):
        """优化图片文件"""
        try:
            img = Image.open(image_path)
            
            # 获取原始文件大小
            original_size = os.path.getsize(image_path)
            
            # 创建优化后的文件路径
            output_path = os.path.splitext(image_path)[0] + '_optimized.jpg'
            
            # 保存压缩后的图片
            img.save(output_path, 'JPEG', quality=self.compression_quality[quality])
            
            # 获取优化后的文件大小
            optimized_size = os.path.getsize(output_path)
            
            return {
                'original_path': image_path,
                'optimized_path': output_path,
                'original_size': original_size,
                'optimized_size': optimized_size,
                'saved_space': original_size - optimized_size
            }
        except Exception as e:
            print(f"Error optimizing image {image_path}: {str(e)}")
            return None
    
    def suggest_optimizations(self, scan_results):
        """根据扫描结果提供优化建议"""
        suggestions = []
        
        # 处理大文件
        for file_info in scan_results['large_files']:
            suggestions.append({
                'type': 'large_file',
                'path': file_info['path'],
                'suggestion': 'Consider compressing or archiving this large file'
            })
        
        # 处理重复文件
        for hash_value, duplicate_files in scan_results['duplicates'].items():
            suggestions.append({
                'type': 'duplicate',
                'files': duplicate_files,
                'suggestion': 'These files are identical. Consider removing duplicates'
            })
        
        # 处理旧文件
        for file_info in scan_results['old_files']:
            suggestions.append({
                'type': 'old_file',
                'path': file_info['path'],
                'suggestion': 'This file has not been accessed for a long time. Consider archiving or removing'
            })
        
        return suggestions

    def get_format_suggestions(self, file_path):
        """获取文件格式转换建议"""
        extension = os.path.splitext(file_path)[1].lower()
        size = os.path.getsize(file_path)
        
        suggestions = []
        
        if extension in ['.jpg', '.jpeg', '.png'] and size > 1000000:  # 1MB
            suggestions.append({
                'current_format': extension,
                'suggested_format': '.webp',
                'reason': 'WebP format offers better compression while maintaining quality'
            })
        
        if extension in ['.mp4', '.avi'] and size > 100000000:  # 100MB
            suggestions.append({
                'current_format': extension,
                'suggested_format': '.mkv',
                'reason': 'MKV format provides better compression for video files'
            })
            
        return suggestions