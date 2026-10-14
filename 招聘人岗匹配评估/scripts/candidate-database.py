#!/usr/bin/env python3
"""
候选人库导入脚本
功能：支持导入历史简历构建本地人才库
版本：v1.0
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='候选人库导入工具 - 支持批量导入历史简历构建本地人才库'
    )
    parser.add_argument(
        '--input-dir',
        required=True,
        help='输入目录：包含待导入简历文件的目录路径'
    )
    parser.add_argument(
        '--output-file',
        required=True,
        help='输出文件：人才库数据库文件路径（JSON格式）'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'csv', 'xlsx'],
        default='json',
        help='输出格式：json/csv/xlsx（默认：json）'
    )
    parser.add_argument(
        '--dedup',
        action='store_true',
        help='启用去重：根据姓名+手机号+邮箱去重'
    )
    parser.add_argument(
        '--category',
        default='uncategorized',
        help='候选人分类：如：技术/销售/管理（默认：uncategorized）'
    )
    parser.add_argument(
        '--source',
        default='unknown',
        help='简历来源：如：招聘网站/企业内部/猎头推荐（默认：unknown）'
    )
    return parser.parse_args()

def scan_resume_files(input_dir):
    """扫描目录中的简历文件"""
    supported_formats = ['.docx', '.pdf', '.txt', '.html', '.doc']
    resume_files = []
    
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"错误：输入目录不存在 - {input_dir}")
        sys.exit(1)
    
    for file_path in input_path.rglob('*'):
        if file_path.suffix.lower() in supported_formats:
            resume_files.append(str(file_path))
    
    return resume_files

def import_resumes(resume_files, category, source):
    """导入简历到人才库"""
    candidates = []
    
    for idx, file_path in enumerate(resume_files, 1):
        filename = os.path.basename(file_path)
        print(f"[{idx}/{len(resume_files)}] 正在导入：{filename}")
        
        candidate = {
            'id': f'C{ datetime.now().strftime("%Y%m%d") }{idx:04d}',
            'import_date': datetime.now().strftime('%Y-%m-%d'),
            'category': category,
            'source': source,
            'original_filename': filename,
            'file_path': file_path,
            'status': 'pending',
            'resume_parsed': False
        }
        candidates.append(candidate)
    
    return candidates

def deduplicate_candidates(candidates):
    """去重：根据姓名+手机号+邮箱去重"""
    seen = set()
    unique_candidates = []
    
    for candidate in candidates:
        key = (
            candidate.get('name', ''),
            candidate.get('phone', ''),
            candidate.get('email', '')
        )
        
        if key not in seen:
            seen.add(key)
            unique_candidates.append(candidate)
        else:
            print(f"[去重] 移除重复候选人：{key[0]}")
    
    return unique_candidates

def save_candidates(candidates, output_file, format_type):
    """保存候选人数据"""
    output_path = Path(output_file)
    
    if format_type == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'created_at': datetime.now().isoformat(),
                'total_count': len(candidates),
                'candidates': candidates
            }, f, ensure_ascii=False, indent=2)
    elif format_type == 'csv':
        import csv
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if candidates:
                fieldnames = ['id', 'import_date', 'category', 'source', 
                             'name', 'phone', 'email', 'status']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(candidates)
    else:
        print(f"错误：不支持的格式 - {format_type}")
        sys.exit(1)
    
    print(f"[完成] 已保存 {len(candidates)} 条候选人记录到：{output_file}")

def main():
    """主函数"""
    args = parse_arguments()
    
    print("=" * 50)
    print("候选人库导入工具 v1.0")
    print("=" * 50)
    print(f"输入目录：{args.input_dir}")
    print(f"输出文件：{args.output_file}")
    print(f"输出格式：{args.format}")
    print(f"启用去重：{args.dedup}")
    print(f"候选人分类：{args.category}")
    print(f"简历来源：{args.source}")
    print("=" * 50)
    
    # 扫描简历文件
    print("\n[1/4] 扫描简历文件...")
    resume_files = scan_resume_files(args.input_dir)
    print(f"找到 {len(resume_files)} 个简历文件")
    
    if not resume_files:
        print("错误：未找到任何简历文件")
        sys.exit(1)
    
    # 导入简历
    print("\n[2/4] 导入简历数据...")
    candidates = import_resumes(resume_files, args.category, args.source)
    
    # 去重
    print("\n[3/4] 处理去重...")
    if args.dedup:
        candidates = deduplicate_candidates(candidates)
        print(f"去重后剩余 {len(candidates)} 条记录")
    else:
        print("跳过去重步骤")
    
    # 保存结果
    print("\n[4/4] 保存数据...")
    save_candidates(candidates, args.output_file, args.format)
    
    print("\n" + "=" * 50)
    print("导入完成！")
    print("=" * 50)
    
    # 输出结果JSON供智能体使用
    result = {
        'status': 'success',
        'total_count': len(candidates),
        'category': args.category,
        'source': args.source,
        'output_file': args.output_file
    }
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
