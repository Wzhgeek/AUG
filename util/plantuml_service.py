#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PlantUML 服务类
用于在大模型对话中集成 PlantUML 转换功能
"""

import re
import os
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from .plantuml_converter import PlantUMLConverter


class PlantUMLService:
    """PlantUML 服务类"""
    
    def __init__(self, output_dir: str = "workspace/img"):
        """
        初始化 PlantUML 服务
        
        Args:
            output_dir: 输出图片的目录路径
        """
        self.converter = PlantUMLConverter(output_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_plantuml_code(self, text: str) -> Optional[str]:
        """
        从文本中提取 PlantUML 代码
        
        Args:
            text: 包含 PlantUML 代码的文本
            
        Returns:
            提取的 PlantUML 代码，如果没有找到则返回 None
        """
        # 匹配 @startuml 和 @enduml 之间的内容
        pattern = r'@startuml\s*(.*?)\s*@enduml'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        
        if match:
            return f"@startuml\n{match.group(1).strip()}\n@enduml"
        
        return None
    
    def process_llm_response(self, llm_response: str, userid: str = "default") -> Dict[str, Any]:
        """
        处理大模型响应，提取 PlantUML 代码并转换为图片
        
        Args:
            llm_response: 大模型的响应文本
            userid: 用户ID，用于生成唯一文件名
            
        Returns:
            包含处理结果的字典
        """
        result = {
            "original_response": llm_response,
            "plantuml_code": None,
            "image_path": None,
            "image_url": None,
            "success": False,
            "error": None
        }
        
        try:
            # 提取 PlantUML 代码
            plantuml_code = self.extract_plantuml_code(llm_response)
            
            if not plantuml_code:
                result["error"] = "未在响应中找到 PlantUML 代码"
                return result
            
            result["plantuml_code"] = plantuml_code
            
            # 生成唯一的文件名
            import hashlib
            import time
            code_hash = hashlib.md5(plantuml_code.encode()).hexdigest()[:8]
            timestamp = int(time.time())
            filename = f"uml_{userid}_{code_hash}_{timestamp}"
            
            # 转换为图片
            image_path = self.converter.convert_to_image(
                plantuml_code=plantuml_code,
                output_filename=filename,
                format="png"
            )
            
            if image_path:
                result["image_path"] = image_path
                result["image_url"] = f"/api/v1/images/{Path(image_path).name}"
                result["success"] = True
            else:
                result["error"] = "图片转换失败"
                
        except Exception as e:
            result["error"] = f"处理过程中发生错误: {str(e)}"
        
        return result
    
    def get_image_url(self, image_path: str) -> str:
        """
        根据图片路径生成访问URL
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            图片访问URL
        """
        if not image_path:
            return ""
        
        filename = Path(image_path).name
        return f"/api/v1/images/{filename}"
    
    def list_generated_images(self) -> list:
        """
        列出所有生成的图片
        
        Returns:
            图片文件列表
        """
        if not self.output_dir.exists():
            return []
        
        image_files = []
        for file_path in self.output_dir.glob("*.png"):
            image_files.append({
                "filename": file_path.name,
                "path": str(file_path),
                "url": self.get_image_url(str(file_path)),
                "size": file_path.stat().st_size,
                "created_time": file_path.stat().st_ctime
            })
        
        return sorted(image_files, key=lambda x: x["created_time"], reverse=True)


# 全局服务实例
plantuml_service = PlantUMLService() 