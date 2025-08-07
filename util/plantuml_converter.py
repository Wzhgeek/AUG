#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PlantUML 转换工具
将 PlantUML 语法转换为图片文件
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Union
import hashlib
import time


class PlantUMLConverter:
    """PlantUML 转换器类"""
    
    def __init__(self, output_dir: str = "workspace/img"):
        """
        初始化转换器
        
        Args:
            output_dir: 输出图片的目录路径
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查是否安装了 PlantUML
        self._check_plantuml_installation()
    
    def _check_plantuml_installation(self):
        """检查 PlantUML 是否已安装"""
        try:
            result = subprocess.run(['plantuml', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✓ PlantUML 已安装")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        print("⚠ PlantUML 未安装或不在 PATH 中")
        print("请安装 PlantUML:")
        print("  Ubuntu/Debian: sudo apt-get install plantuml")
        print("  macOS: brew install plantuml")
        print("  Windows: 下载并安装 PlantUML.jar")
        return False
    
    def convert_to_image(self, 
                        plantuml_code: str, 
                        output_filename: Optional[str] = None,
                        format: str = "png") -> Optional[str]:
        """
        将 PlantUML 代码转换为图片
        
        Args:
            plantuml_code: PlantUML 语法代码
            output_filename: 输出文件名（不包含扩展名），如果为 None 则自动生成
            format: 输出格式 (png, svg, pdf, etc.)
            
        Returns:
            生成的图片文件路径，如果失败返回 None
        """
        if not plantuml_code.strip():
            print("错误: PlantUML 代码不能为空")
            return None
        
        # 生成输出文件名
        if output_filename is None:
            # 使用代码的哈希值和时间戳生成唯一文件名
            code_hash = hashlib.md5(plantuml_code.encode()).hexdigest()[:8]
            timestamp = int(time.time())
            output_filename = f"plantuml_{code_hash}_{timestamp}"
        
        # 确保文件名不包含扩展名
        output_filename = Path(output_filename).stem
        
        # 创建具有指定名称的临时文件
        temp_puml_path = self.output_dir / f"{output_filename}.puml"
        
        try:
            # 写入PlantUML代码到指定文件
            with open(temp_puml_path, 'w', encoding='utf-8') as f:
                f.write(plantuml_code)
            
            # 构建输出路径
            output_path = self.output_dir / f"{output_filename}.{format}"
            
            # 执行 PlantUML 命令
            cmd = [
                'plantuml',
                '-t', format,
                '-o', str(self.output_dir.absolute()),
                str(temp_puml_path)
            ]
            
            print(f"正在转换 PlantUML 代码为 {format.upper()} 格式...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✓ 转换成功: {output_path}")
                return str(output_path)
            else:
                print(f"✗ 转换失败: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("✗ 转换超时")
            return None
        except Exception as e:
            print(f"✗ 转换过程中发生错误: {e}")
            return None
        finally:
            # 清理临时文件
            try:
                os.unlink(temp_puml_path)
            except:
                pass
    
    def convert_from_file(self, 
                         input_file: Union[str, Path], 
                         output_filename: Optional[str] = None,
                         format: str = "png") -> Optional[str]:
        """
        从文件读取 PlantUML 代码并转换为图片
        
        Args:
            input_file: 包含 PlantUML 代码的文件路径
            output_filename: 输出文件名
            format: 输出格式
            
        Returns:
            生成的图片文件路径
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                plantuml_code = f.read()
            
            if output_filename is None:
                output_filename = Path(input_file).stem
            
            return self.convert_to_image(plantuml_code, output_filename, format)
            
        except FileNotFoundError:
            print(f"✗ 文件未找到: {input_file}")
            return None
        except Exception as e:
            print(f"✗ 读取文件时发生错误: {e}")
            return None


def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PlantUML 转换工具")
    parser.add_argument("input", help="PlantUML 代码或文件路径")
    parser.add_argument("-o", "--output", help="输出文件名（不包含扩展名）")
    parser.add_argument("-f", "--format", default="png", 
                       choices=["png", "svg", "pdf", "eps"], 
                       help="输出格式 (默认: png)")
    parser.add_argument("--output-dir", default="workspace/img", 
                       help="输出目录 (默认: workspace/img)")
    
    args = parser.parse_args()
    
    converter = PlantUMLConverter(args.output_dir)
    
    # 检查输入是文件还是代码
    input_path = Path(args.input)
    if input_path.exists() and input_path.is_file():
        # 输入是文件
        result = converter.convert_from_file(input_path, args.output, args.format)
    else:
        # 输入是代码
        result = converter.convert_to_image(args.input, args.output, args.format)
    
    if result:
        print(f"图片已保存到: {result}")
    else:
        print("转换失败")
        sys.exit(1)


if __name__ == "__main__":
    main() 