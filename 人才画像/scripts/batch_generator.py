#!/usr/bin/env python3
"""
批量报告生成脚本
功能：根据规则批量生成报告，默认输出HTML和PDF两种格式
"""

import argparse
import json
import os
from typing import Dict, Any
from datetime import datetime
from report_generator import ReportGenerator


def generate_default_formats(report_data: Dict[str, Any], output_prefix: str,
                             template_dir: str = './assets/templates') -> None:
    """
    生成默认格式报告（交互式可视化HTML + PDF）

    Args:
        report_data: 报告数据
        output_prefix: 输出文件前缀
        template_dir: 模板目录
    """
    generator = ReportGenerator(template_dir, os.path.dirname(output_prefix))

    # 生成交互式可视化HTML格式
    interactive_html_output = f"{output_prefix}.html"
    print(f"📊 生成交互式可视化HTML报告: {interactive_html_output}")
    generator.generate_interactive_html(report_data, interactive_html_output)

    # 生成PDF格式
    pdf_output = f"{output_prefix}.pdf"
    print(f"📄 生成PDF报告: {pdf_output}")
    generator.generate_pdf_report(report_data, pdf_output)


def generate_all_formats(report_data: Dict[str, Any], output_prefix: str,
                         template_dir: str = './assets/templates') -> None:
    """
    生成所有格式报告（包括Excel）

    注意：仅在用户明确使用--all-formats时才生成Excel格式，
    默认情况下（不指定格式）不生成Excel文件，也不显示在输出列表中。

    Args:
        report_data: 报告数据
        output_prefix: 输出文件前缀
        template_dir: 模板目录
    """
    generator = ReportGenerator(template_dir, os.path.dirname(output_prefix))

    formats = [
        ('html', 'HTML', '.html'),
        ('pdf', 'PDF', '.pdf'),
        ('word', 'Word', '.docx'),
        ('ppt', 'PPT', '.pptx'),
        ('excel', 'Excel', '.xlsx'),
        ('interactive', '动态可视化', '_interactive.html')
    ]

    for format_key, format_name, extension in formats:
        output = f"{output_prefix}{extension}"
        print(f"📄 生成{format_name}报告: {output}")

        if format_key == 'html':
            generator.generate_html_report(report_data, output)
        elif format_key == 'pdf':
            generator.generate_pdf_report(report_data, output)
        elif format_key == 'word':
            generator.generate_word_report(report_data, output)
        elif format_key == 'ppt':
            generator.generate_ppt_report(report_data, output)
        elif format_key == 'excel':
            generator.generate_excel_report(report_data, output)
        elif format_key == 'interactive':
            generator.generate_interactive_html(report_data, output)


def load_json(file_path: str) -> Dict[str, Any]:
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description='批量报告生成脚本（默认生成交互式可视化HTML和PDF）',
        epilog='使用示例:\n'
               '  # 默认生成交互式可视化HTML和PDF\n'
               '  python scripts/batch_generator.py --data report.json --output report\n\n'
               '  # 生成所有格式\n'
               '  python scripts/batch_generator.py --data report.json --output report --all-formats\n\n'
               '  # 指定格式\n'
               '  python scripts/batch_generator.py --data report.json --output report --formats html word ppt',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--data', required=True, help='报告数据文件路径（JSON格式）')
    parser.add_argument('--output', required=True, help='输出文件前缀（不带扩展名）')
    parser.add_argument('--formats', nargs='+',
                        choices=['html', 'pdf', 'word', 'ppt', 'excel', 'interactive'],
                        help='指定输出格式（不指定则默认生成交互式可视化HTML和PDF）')
    parser.add_argument('--all-formats', action='store_true',
                        help='生成所有支持的格式')
    parser.add_argument('--template-dir', default='./assets/templates',
                        help='模板文件目录（默认：./assets/templates）')

    args = parser.parse_args()

    # 加载数据
    print(f"📂 加载数据: {args.data}")
    report_data = load_json(args.data)

    # 添加默认值（强制更新生成时间）
    report_data['generated_at'] = datetime.now().strftime('%Y-%m-%d')
    report_data.setdefault('version', '1.0')

    # 确定输出格式
    if args.all_formats:
        # 生成所有格式
        print("\n🚀 生成所有格式报告...")
        generate_all_formats(report_data, args.output, args.template_dir)
    elif args.formats:
        # 用户指定格式
        print(f"\n🚀 生成指定格式报告: {', '.join(args.formats)}")
        generator = ReportGenerator(args.template_dir, os.path.dirname(args.output))

        for fmt in args.formats:
            if fmt == 'html':
                output = f"{args.output}.html"
                generator.generate_html_report(report_data, output)
            elif fmt == 'pdf':
                output = f"{args.output}.pdf"
                generator.generate_pdf_report(report_data, output)
            elif fmt == 'word':
                output = f"{args.output}.docx"
                generator.generate_word_report(report_data, output)
            elif fmt == 'ppt':
                output = f"{args.output}.pptx"
                generator.generate_ppt_report(report_data, output)
            elif fmt == 'excel':
                output = f"{args.output}.xlsx"
                generator.generate_excel_report(report_data, output)
            elif fmt == 'interactive':
                output = f"{args.output}_interactive.html"
                generator.generate_interactive_html(report_data, output)
    else:
        # 默认生成交互式可视化HTML和PDF
        print("\n🚀 默认生成交互式可视化HTML和PDF两种格式报告...")
        generate_default_formats(report_data, args.output, args.template_dir)

    print("\n✅ 报告生成完成!")
    print("\n📋 输出文件:")
    if args.all_formats:
        # --all-formats时显示所有格式，包括Excel
        print(f"  - {args.output}.html")
        print(f"  - {args.output}.pdf")
        print(f"  - {args.output}.docx")
        print(f"  - {args.output}.pptx")
        print(f"  - {args.output}.xlsx (包含数据表格)")
        print(f"  - {args.output}_interactive.html")
    elif args.formats:
        # 用户指定格式时显示指定格式
        for fmt in args.formats:
            if fmt == 'interactive':
                print(f"  - {args.output}_interactive.html")
            elif fmt == 'excel':
                print(f"  - {args.output}.xlsx (包含数据表格)")
            else:
                print(f"  - {args.output}.{fmt}")
    else:
        # 默认输出：显示交互式可视化HTML和PDF，不显示原始数据文件
        print(f"  - {args.output}.html (默认 - 交互式可视化动态报告，在线查看+一键下载)")
        print(f"  - {args.output}.pdf (默认 - 可下载)")
        print(f"\n💡 提示：")
        print(f"  - 提供给用户的文档中不包含JSON数据文件")
        print(f"  - 用户端无法下载JSON数据文件")
        print(f"  - 原始数据已脱敏处理，不单独提供给用户，也不显示在输出列表中。")


if __name__ == "__main__":
    main()
