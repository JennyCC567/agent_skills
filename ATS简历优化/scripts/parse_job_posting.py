#!/usr/bin/env python3
"""
岗位信息解析脚本（纯本地解析，无外部网络请求）

支持从用户提供的JD文本或本地HTML文件中解析岗位信息，输出结构化JSON数据。
不访问任何外部网络，所有数据均在本地处理。
"""

import sys
import json
import argparse
import os


class JobPostingParser:
    """岗位信息解析器 - 纯本地解析，零外部请求"""

    def __init__(self, source, source_type="text"):
        """
        source: JD文本内容 或 本地HTML文件路径
        source_type: 'text'(纯文本JD) 或 'html_file'(本地HTML文件)
        """
        self.source = source
        self.source_type = source_type

    def parse(self):
        """解析岗位信息"""
        try:
            if self.source_type == "html_file":
                if not os.path.isfile(self.source):
                    print(f"错误：文件不存在 - {self.source}", file=sys.stderr)
                    return None
                with open(self.source, 'r', encoding='utf-8') as f:
                    content = f.read()
                return self._parse_html_content(content)
            else:
                return self._parse_text(self.source)
        except Exception as e:
            print(f"解析失败: {str(e)}", file=sys.stderr)
            return None

    def _parse_text(self, text):
        """解析纯文本JD"""
        job_info = {
            'platform': '本地解析',
            'source': 'text_input'
        }

        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            print("错误：输入的JD内容为空", file=sys.stderr)
            return None

        job_name = ''
        desc_lines = []
        for i, line in enumerate(lines):
            if any(kw in line for kw in ['岗位名称', '职位名称', '招聘岗位', '应聘岗位', '岗位：']):
                job_name = line.split('：')[-1].split(':')[-1].strip()
                desc_lines = lines[i+1:]
                break
        if not job_name and lines:
            job_name = lines[0]
            desc_lines = lines[1:]

        job_info['job_name'] = job_name

        salary = ''
        for line in lines:
            if any(kw in line for kw in ['薪资', '薪酬', '待遇', '月薪', '年薪', '工资']):
                salary = line.split('：')[-1].split(':')[-1].strip()
                break
        job_info['salary'] = salary

        requirements = []
        in_requirements = False
        for line in desc_lines:
            if any(kw in line for kw in ['任职要求', '岗位要求', '职位要求', '录用条件', '要求']):
                in_requirements = True
                continue
            if in_requirements:
                if any(kw in line for kw in ['福利', '待遇', '我们提供']):
                    break
                clean = line.lstrip('•·-►▸▹◂◃').strip()
                if clean:
                    requirements.append(clean)
        job_info['requirements'] = requirements

        responsibilities = []
        in_resp = False
        for line in desc_lines:
            if any(kw in line for kw in ['岗位职责', '工作内容', '工作职责', '职位描述']):
                in_resp = True
                continue
            if in_resp:
                if any(kw in line for kw in ['任职要求', '岗位要求', '职位要求']):
                    break
                clean = line.lstrip('•·-►▸▹◂◃').strip()
                if clean:
                    responsibilities.append(clean)
        job_info['responsibilities'] = responsibilities

        if not responsibilities and desc_lines:
            job_info['description'] = '\n'.join(desc_lines)

        return job_info

    def _parse_html_content(self, html_content):
        """解析本地HTML文件中的岗位信息"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
        except ImportError:
            return self._parse_text(self._html_to_text(html_content))

        job_info = {
            'platform': '本地HTML解析',
            'source': 'local_file'
        }

        for tag in ['h1', 'h2', 'title']:
            title = soup.find(tag)
            if title:
                job_info['job_name'] = title.get_text(strip=True)
                break

        body = soup.find('body')
        if body:
            text = body.get_text('\n', strip=True)
            job_info['description'] = text
        else:
            job_info['description'] = soup.get_text('\n', strip=True)

        return job_info

    def _html_to_text(self, html):
        """简单HTML转文本"""
        import re
        text = re.sub(r'<[^>]+>', '\n', html)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='解析招聘岗位JD信息（纯本地，无网络请求）')
    parser.add_argument('--file', help='本地HTML/TXT文件路径')
    parser.add_argument('--text', help='直接输入JD文本')
    parser.add_argument('--stdin', action='store_true', help='从标准输入读取JD文本')

    args = parser.parse_args()

    if args.file:
        ext = os.path.splitext(args.file)[1].lower()
        source_type = 'html_file' if ext in ('.html', '.htm') else 'text'
        job_parser = JobPostingParser(args.file, source_type)
    elif args.text:
        job_parser = JobPostingParser(args.text, 'text')
    elif args.stdin:
        text = sys.stdin.read()
        job_parser = JobPostingParser(text, 'text')
    else:
        print("错误：请通过 --file、--text 或 --stdin 提供JD内容", file=sys.stderr)
        sys.exit(1)

    job_info = job_parser.parse()

    if job_info:
        print(json.dumps(job_info, ensure_ascii=False, indent=2))
    else:
        print("错误：无法解析岗位信息", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
