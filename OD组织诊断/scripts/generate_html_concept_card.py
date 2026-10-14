#!/usr/bin/env python3
"""
HTML转PDF概念卡生成器
使用 HTML 格式生成概念卡，支持完美中文字符显示
可通过浏览器打印为 PDF
"""

import json
import sys
from pathlib import Path
from jinja2 import Template


def get_embedded_js():
    """读取并内嵌JS库，确保HTML完全离线可用"""
    script_dir = Path(__file__).parent
    assets_dir = script_dir.parent / "assets"
    
    js_embed = ""
    
    # 读取html2pdf库
    html2pdf_path = assets_dir / "html2pdf.bundle.min.js"
    if html2pdf_path.exists():
        with open(html2pdf_path, 'r', encoding='utf-8') as f:
            js_embed += f.read() + "\n"
    
    return js_embed


def parse_input(input_str):
    """
    解析输入的JSON字符串

    输入格式:
    {
        "company_name": "XX公司",
        "title": "OD 组织发展入门概念卡",
        "content": {
            "definition": "OD（Organization Development）组织发展...",
            "difference": "传统HR关注个体绩效...",
            "key_models": ["麦肯锡7S模型", "BLM业务领先模型", "杨三角"]
        },
        "output_path": "./od_concept_card.html"
    }

    验证规则:
    - company_name 和 title 不能为空
    - content 必须包含 definition 和 difference
    - output_path 必须以 .html 结尾
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 检查必需字段
    if 'company_name' not in data or not data['company_name']:
        raise ValueError("缺少必需字段: company_name 或company_name为空")

    if 'title' not in data or not data['title']:
        data['title'] = "OD 组织发展入门概念卡"

    if 'content' not in data:
        raise ValueError("缺少必需字段: content")

    content = data['content']
    if 'definition' not in content:
        raise ValueError("content 必须包含 definition 字段")
    if 'difference' not in content:
        raise ValueError("content 必须包含 difference 字段")

    if 'key_models' not in content:
        data['content']['key_models'] = ["麦肯锡7S模型", "BLM业务领先模型", "杨三角"]

    # 设置默认output_path
    if 'output_path' not in data:
        data['output_path'] = "./od_concept_card.html"
    else:
        if not data['output_path'].endswith('.html'):
            data['output_path'] = "./od_concept_card.html"

    return data


def generate_html_card(data):
    """
    生成 HTML 概念卡（支持完美中文显示）

    参数:
        data: 包含公司信息和内容的字典

    返回:
        str: 生成的 HTML 文件路径
    """
    company_name = data['company_name']
    title = data['title']
    content = data['content']
    output_path = Path(data['output_path'])

    # 获取内嵌的JS库，确保HTML完全离线可用
    embedded_js = get_embedded_js()

    # 生成模型列表
    models_html = ""
    for model in content['key_models']:
        models_html += f"<li><strong>{model}</strong> - 组织诊断/变革设计</li>"

    # HTML模板
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script>
    // 内嵌JS库，确保完全离线可用
    {embedded_js}
    </script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        @page {{
            size: A5;
            margin: 0;
        }}

        @media screen {{
            body {{
                background: #e2e8f0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
            }}
        }}

        @media print {{
            body {{
                background: white;
            }}
            .action-btn {{
                display: none !important;
            }}
        }}

        .card {{
            background: white;
            width: 210mm;
            min-height: 148mm;
            padding: 20mm;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            border-radius: 8px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #3b82f6;
        }}

        .header h1 {{
            font-size: 28px;
            color: #1e293b;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header .subtitle {{
            font-size: 14px;
            color: #64748b;
            font-style: italic;
        }}

        .section {{
            margin-bottom: 25px;
        }}

        .section-title {{
            font-size: 16px;
            color: #3b82f6;
            font-weight: 600;
            margin-bottom: 12px;
            padding-left: 12px;
            border-left: 4px solid #3b82f6;
        }}

        .section-content {{
            font-size: 12px;
            color: #475569;
            line-height: 1.8;
            text-align: justify;
        }}

        .models-list {{
            list-style: none;
            margin-top: 10px;
        }}

        .models-list li {{
            padding: 8px 12px;
            margin-bottom: 8px;
            background: #f1f5f9;
            border-radius: 6px;
            font-size: 12px;
            color: #334155;
        }}

        .models-list strong {{
            color: #3b82f6;
        }}

        .highlight-box {{
            background: #eff6ff;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
            margin-top: 20px;
        }}

        .highlight-box p {{
            font-size: 13px;
            color: #1e40af;
            font-weight: 500;
            line-height: 1.6;
        }}

        .footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 10px;
            color: #94a3b8;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
        }}

        .disclaimer {{
            margin-top: 20px;
            padding: 12px;
            background: #f0f9ff;
            border-left: 4px solid #3b82f6;
            border-radius: 6px;
            font-size: 10px;
            color: #475569;
            line-height: 1.8;
        }}

        .action-bar {{
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 20px;
            padding: 16px;
            background: #f8fafc;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }}

        .action-btn {{
            background: #3b82f6;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .action-btn:hover {{
            background: #2563eb;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h1>{title}</h1>
            <div class="subtitle">{company_name}</div>
        </div>

        <div class="section">
            <div class="section-title">什么是 OD？</div>
            <div class="section-content">
                {content['definition']}
            </div>
        </div>

        <div class="section">
            <div class="section-title">OD vs 传统 HR</div>
            <div class="section-content">
                {content['difference']}
            </div>
        </div>

        <div class="section">
            <div class="section-title">关键 OD 模型</div>
            <ul class="models-list">
                {models_html}
            </ul>
        </div>

        <div class="highlight-box">
            <p>🎯 <strong>核心本质：</strong>OD 不是做培训、不是搞团建，而是以战略为导向的系统性组织能力建设。</p>
        </div>

        <div class="disclaimer">
            <strong>免责申明：</strong> 本工具由AI基于专业理论、行业实践、公开政府文件、权威机构白皮书及行业报告生成。所有生成报告、分析及建议均基于您提供的数据得出，仅供参考，不构成正式管理咨询、法律意见或商业决策依据，任何决策及后果由您自行承担。
        </div>

        <div class="footer">
            本概念卡由 OD 组织发展助手 生成
        </div>

        <div class="action-bar">
            <button class="action-btn" onclick="downloadHTML()">🌐 下载 HTML</button>
            <button class="action-btn" onclick="downloadPDF()">📄 下载 PDF</button>
        </div>
    </div>

    <script>
        // 获取当前日期（自动填充真实系统时间）
        function getCurrentDate() {{
            var now = new Date();
            var year = now.getFullYear();
            var month = String(now.getMonth() + 1).padStart(2, '0');
            var day = String(now.getDate()).padStart(2, '0');
            return year + '年' + month + '月' + day + '日';
        }}

        function downloadHTML() {{
            var htmlContent = document.documentElement.outerHTML;
            var blob = new Blob([htmlContent], {{ type: 'text/html;charset=utf-8' }});
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = '{title}.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}

        // 下载PDF功能
        function downloadPDF() {{
            var element = document.querySelector('.card');
            var opt = {{
                margin: 10,
                filename: '{title}.pdf',
                image: {{ type: 'jpeg', quality: 0.98 }},
                html2canvas: {{ scale: 2, useCORS: true }},
                jsPDF: {{ unit: 'mm', format: 'a4', orientation: 'portrait' }}
            }};

            var btn = document.querySelector('button[onclick="downloadPDF()"]');
            var originalText = btn.textContent;
            btn.textContent = '正在生成PDF...';
            btn.disabled = true;

            html2pdf().set(opt).from(element).save().then(function() {{
                btn.textContent = originalText;
                btn.disabled = false;
            }}).catch(function(err) {{
                console.error('PDF生成失败:', err);
                alert('PDF生成失败，请尝试使用浏览器打印功能');
                btn.textContent = originalText;
                btn.disabled = false;
            }});
        }}
    </script>
</body>
</html>"""

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)

    return str(output_path)


def main():
    """
    主函数
    """
    if len(sys.argv) < 2:
        print("用法: python generate_html_concept_card.py '<JSON数据>'")
        print("示例: python generate_html_concept_card.py '{\"company_name\":\"XX公司\",\"content\":{\"definition\":\"OD是...\",\"difference\":\"OD vs HR...\"}}'")
        print("\n提示：生成的HTML文件可在浏览器中打开，然后点击'打印/保存为PDF'按钮导出为PDF")
        return 1

    input_str = sys.argv[1]

    try:
        # 解析输入
        data = parse_input(input_str)

        # 生成 HTML
        result_path = generate_html_card(data)

        print(f"HTML概念卡已生成: {result_path}")
        print("提示：在浏览器中打开文件，点击右上角'打印/保存为PDF'按钮可导出为PDF格式")
        return 0

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
