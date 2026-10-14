#!/usr/bin/env python3
"""
Unicode清理脚本
功能：
1. 制表符 -> Markdown表格/缩进
2. 装饰符号 -> 文字标记
3. 箭头 -> 文字描述
4. Emoji -> 文字标记
"""

import re
import os
from pathlib import Path

# 替换规则定义
REPLACEMENTS = {
    # 箭头符号
    '->': '->',
    '<-': '<-',
    '<->': '<->',
    '^': '^',
    'v': 'v',
    '=>': '=>',
    '<=': '<=',
    '=>': '=>',
    '<=': '<=',

    # 检查符号
    '[是]': '[是]',
    '[否]': '[否]',
    '[匹配]': '[匹配]',
    '[不匹配]': '[不匹配]',
    '[通过]': '[通过]',
    '[失败]': '[失败]',
    '*': '[提示]',

    # 方向符号
    '|': '|',
    '+': '+',
    '+': '+',
    '+': '+',
    '+': '+',
    '+': '+',
    '+': '+',
    '+': '+',
    '+': '+',
    '+': '+',
    '-': '-',
    '-': '-',
    '=': '=',
    '+': '+',
    '+': '+',
    '+': '+',
    '+': '+',
    '|': '|',

    # 其他装饰符号
    '[必填]': '[必填]',
    '[选填]': '[选填]',
    '-': '-',
    '-': '-',
    '*': '*',
    'o': 'o',
    '*': '*',
    '*': '*',
    'o': 'o',
    '*': '*',
    '*': '*',
    'v': 'v',
    '^': '^',

    # 数学符号
    'x': 'x',
    '/': '/',
    '!=': '!=',
    '<=': '<=',
    '>=': '>=',
    '~': '~',
    '+/-': '+/-',
    'inf': 'inf',

    # 其他Unicode符号
    '...': '...',
    ' - ': ' - ',
    ' - ': ' - ',
    'deg': 'deg',
    '(c)': '(c)',
    '(R)': '(R)',
    '(TM)': '(TM)',
    'Section ': 'Section ',
    'para ': 'para ',

    # 特殊空格
    '\u200b': '',  # 零宽空格
    '\u200c': '',  # 零宽非连接符
    '\u200d': '',  # 零宽连接符
    '\ufeff': '',  # BOM
}

def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 应用所有替换
    for old, new in REPLACEMENTS.items():
        content = content.replace(old, new)

    # 处理制表符（保持对齐，但移除多余的）
    lines = content.split('\n')
    processed_lines = []
    for line in lines:
        # 如果是表格行，保留表格结构
        if '|' in line and line.strip():
            processed_lines.append(line.rstrip())
        else:
            # 非表格行，规范化缩进
            processed_lines.append(line.rstrip())

    content = '\n'.join(processed_lines)

    # 如果有变化，写回文件
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """主函数"""
    # 要处理的目录
    base_dir = Path('/workspace/projects/jd-candidate-matching')

    # 要处理的文件类型
    extensions = ['.md', '.py', '.html']

    # 统计
    total_files = 0
    modified_files = 0

    for ext in extensions:
        for filepath in base_dir.rglob(f'*{ext}'):
            # 跳过node_modules等目录
            if 'node_modules' in str(filepath):
                continue

            total_files += 1
            if process_file(filepath):
                modified_files += 1
                print(f'Modified: {filepath}')

    print(f'\n完成: 处理了 {total_files} 个文件，修改了 {modified_files} 个文件')

if __name__ == '__main__':
    main()
