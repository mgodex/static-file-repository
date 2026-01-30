#!/usr/bin/env python3
import os
import json
import random
import re
from pathlib import Path

class EmojiOrganizer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.json_file = self.base_dir / "mengling.json"
        self.used_ids = set()
        
    def load_existing_ids(self):
        """加载已存在的6位数ID"""
        self.used_ids.clear()
        for folder in self.base_dir.iterdir():
            if folder.is_dir():
                for file_path in folder.iterdir():
                    if file_path.is_file() and re.match(r'^\d{6}', file_path.stem):
                        self.used_ids.add(file_path.stem)
    
    def generate_unique_id(self):
        """生成唯一的6位数ID"""
        while True:
            new_id = f"{random.randint(100000, 999999)}"
            if new_id not in self.used_ids:
                self.used_ids.add(new_id)
                return new_id
    
    def is_valid_filename(self, filename):
        """检查文件名是否符合6位数ID规范"""
        stem = Path(filename).stem
        return re.match(r'^\d{6}$', stem)
    
    def rename_files(self):
        """重命名不规范的文件"""
        print("开始重命名不规范的文件...")
        self.load_existing_ids()
        
        renamed_count = 0
        for folder in self.base_dir.iterdir():
            if folder.is_dir():
                for file_path in folder.iterdir():
                    if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                        if not self.is_valid_filename(file_path.name):
                            new_id = self.generate_unique_id()
                            new_name = f"{new_id}{file_path.suffix}"
                            new_path = file_path.parent / new_name
                            
                            print(f"重命名: {folder.name}/{file_path.name} -> {folder.name}/{new_name}")
                            file_path.rename(new_path)
                            renamed_count += 1
        
        print(f"重命名完成，共重命名 {renamed_count} 个文件")
        return renamed_count
    
    def scan_emoji_files(self):
        """扫描所有emoji文件并生成数据"""
        print("开始扫描emoji文件...")
        
        emoji_data = []
        base_url = "https://cdn.jsdmirror.com/gh/mengDot/static-file-repository@main/emoji"
        
        for folder in self.base_dir.iterdir():
            if folder.is_dir():
                category = folder.name  # 文件夹名作为分类
                
                for file_path in folder.iterdir():
                    if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                        file_url = f"{base_url}/{category}/{file_path.name}"
                        
                        emoji_item = {
                            "name": file_path.stem,
                            "category": category,
                            "url": file_url
                        }
                        emoji_data.append(emoji_item)
        
        return emoji_data
    
    def get_category_from_folder(self, folder):
        """从文件夹路径推断分类名称"""
        # 直接使用文件夹名作为分类
        return folder.name
    
    def generate_json(self):
        """生成mengling.json文件"""
        emoji_data = self.scan_emoji_files()
        
        json_content = {
            "code": 200,
            "msg": "萌灵表情包分享地址(mengling.meng.me)",
            "data": emoji_data
        }
        
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, ensure_ascii=False, indent=4)
        
        print(f"生成JSON文件完成，共包含 {len(emoji_data)} 个表情包")
        return len(emoji_data)
    
    def organize_all(self):
        """执行完整的整理流程"""
        print("=== Emoji整理工具 ===")
        
        # 1. 重命名文件
        renamed = self.rename_files()
        
        # 2. 生成JSON文件
        emoji_count = self.generate_json()
        
        print(f"\n整理完成!")
        print(f"- 重命名文件: {renamed} 个")
        print(f"- 生成表情包数据: {emoji_count} 个")

def main():
    # 获取脚本所在目录作为基础目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    organizer = EmojiOrganizer(base_dir)
    
    print("选择操作:")
    print("1. 仅重命名文件")
    print("2. 仅生成JSON文件")
    print("3. 执行完整整理流程")
    
    choice = input("请输入选择 (1-3): ").strip()
    
    if choice == "1":
        organizer.rename_files()
    elif choice == "2":
        organizer.generate_json()
    elif choice == "3":
        organizer.organize_all()
    else:
        print("无效选择")

if __name__ == "__main__":
    main()
