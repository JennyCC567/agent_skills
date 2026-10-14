#!/usr/bin/env python3
"""
简历文件解析脚本
支持 Word (.doc, .docx) 和 PDF (.pdf) 格式
"""

import argparse
import sys
from pathlib import Path


def parse_word(file_path):
    """
    解析 Word 文件，提取文本内容
    
    Args:
        file_path: Word 文件路径
        
    Returns:
        str: 提取的文本内容
    """
    try:
        from docx import Document
        
        doc = Document(file_path)
        text_content = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_content.append(paragraph.text)
        
        # 提取表格内容
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_text:
                    text_content.append(" | ".join(row_text))
        
        return "\n".join(text_content)
        
    except ImportError:
        print("错误：缺少 python-docx 库。请运行：pip install python-docx")
        sys.exit(1)
    except Exception as e:
        print(f"解析 Word 文件失败：{str(e)}")
        sys.exit(1)


def parse_pdf(file_path):
    """
    解析 PDF 文件，提取文本内容
    
    Args:
        file_path: PDF 文件路径
        
    Returns:
        str: 提取的文本内容
    """
    try:
        import pdfplumber
        
        text_content = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        
        return "\n".join(text_content)
        
    except ImportError:
        print("错误：缺少 pdfplumber 库。请运行：pip install pdfplumber")
        sys.exit(1)
    except Exception as e:
        print(f"解析 PDF 文件失败：{str(e)}")
        sys.exit(1)


def parse_resume(file_path):
    """
    解析简历文件（自动识别格式）
    
    Args:
        file_path: 简历文件路径
        
    Returns:
        str: 提取的文本内容
    """
    path = Path(file_path)
    
    # 检查文件是否存在
    if not path.exists():
        print(f"错误：文件不存在 - {file_path}")
        sys.exit(1)
    
    # 根据文件扩展名选择解析方法
    file_ext = path.suffix.lower()
    
    if file_ext in ['.doc', '.docx']:
        return parse_word(file_path)
    elif file_ext == '.pdf':
        return parse_pdf(file_path)
    else:
        print(f"错误：不支持的文件格式 - {file_ext}。仅支持 .doc, .docx, .pdf")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='解析简历文件（Word/PDF）')
    parser.add_argument('--file', '-f', required=True, help='简历文件路径')
    
    args = parser.parse_args()
    
    # 解析简历
    text_content = parse_resume(args.file)
    
    # 输出文本内容
    print(text_content)


if __name__ == '__main__':
    main()
