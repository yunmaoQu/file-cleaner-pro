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
            
            # 确定输出格式和文件扩展名
            file_dir = os.path.dirname(image_path)
            file_name_with_ext = os.path.basename(image_path)
            file_name, ext = os.path.splitext(file_name_with_ext)
            
            # 如果文件名已经包含"_optimized"，则提示已优化
            if "_optimized" in file_name:
                print(f"File {image_path} appears to be already optimized")
                return {
                    'original_path': image_path,
                    'optimized_path': image_path,
                    'original_size': original_size,
                    'optimized_size': original_size,
                    'saved_space': 0,
                    'format': ext.upper().strip('.'),
                    'already_optimized': True
                }
            
            # 检查图像是否有透明通道
            if img.mode == 'RGBA':
                # PNG或WebP格式保留透明度
                if ext.lower() in ['.png', '.webp']:
                    output_format = ext.upper().strip('.')
                    output_ext = ext
                else:
                    # 使用PNG格式保存带透明通道的图像
                    output_format = 'PNG'
                    output_ext = '.png'
            else:
                # 没有透明通道的图像可以保存为JPEG
                output_format = 'JPEG'
                output_ext = '.jpg'
                
                # 如果图像不是RGB模式，转换为RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
            
            # 创建优化后的文件路径，确保使用正确的路径分隔符
            # 移除文件名中包含的 " - 副本" 或类似字样
            clean_name = file_name.replace(" - 副本", "").replace("_副本", "").replace("(副本)", "")
            output_file_name = clean_name + '_optimized' + output_ext
            output_path = os.path.join(file_dir, output_file_name)
            # 确保路径分隔符一致
            output_path = os.path.normpath(output_path)
            
            # 保存压缩后的图片
            if output_format == 'JPEG':
                img.save(output_path, output_format, quality=self.compression_quality[quality])
            elif output_format == 'PNG':
                img.save(output_path, output_format, optimize=True)
            else:  # WebP
                img.save(output_path, output_format, quality=self.compression_quality[quality])
            
            # 获取优化后的文件大小
            optimized_size = os.path.getsize(output_path)
            
            # 如果优化没有减小文件大小，则删除优化后的文件并返回失败结果
            if optimized_size >= original_size:
                print(f"Optimization did not reduce file size for {image_path}")
                os.remove(output_path)
                return {
                    'original_path': image_path,
                    'optimized_path': None,
                    'original_size': original_size,
                    'optimized_size': optimized_size,
                    'saved_space': 0,
                    'format': output_format,
                    'success': False,
                    'reason': 'No size reduction'
                }
            
            return {
                'original_path': image_path,
                'optimized_path': output_path,
                'original_size': original_size,
                'optimized_size': optimized_size,
                'saved_space': original_size - optimized_size,
                'format': output_format,
                'success': True
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