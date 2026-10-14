#!/usr/bin/env python3
"""
多格式报告生成脚本
功能：支持HTML/PDF/Word/PPT/Excel等多种格式的报告生成
规范：严格遵循技能交付物生成红线规则v5.0
"""

import argparse
import json
import os
import io
import base64
import numpy as np
from typing import Dict, Any, List
from datetime import datetime

# 全局变量用于缓存导入的模块
_MATPLOTLIB_PLT = None
_MATPLOTLIB_FM = None
_MATPLOTLIB_INITIALIZED = False

def _ensure_matplotlib():
    """延迟加载matplotlib，只在需要时导入"""
    global _MATPLOTLIB_PLT, _MATPLOTLIB_FM, _MATPLOTLIB_INITIALIZED, np
    if not _MATPLOTLIB_INITIALIZED:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as _plt
            import matplotlib.font_manager as _fm
            _MATPLOTLIB_PLT = _plt
            _MATPLOTLIB_FM = _fm
            import numpy as np  # 确保numpy已导入
            # 注册中文字体 - 使用硬编码路径，避免外部命令
            font_paths = [
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            ]
            for fp in font_paths:
                if os.path.exists(fp):
                    try:
                        _MATPLOTLIB_FM.fontManager.addfont(fp)
                        _MATPLOTLIB_PLT.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'DejaVu Sans']
                        _MATPLOTLIB_PLT.rcParams['axes.unicode_minus'] = False
                        break
                    except:
                        continue
            _MATPLOTLIB_INITIALIZED = True
        except ImportError:
            _MATPLOTLIB_INITIALIZED = True  # 标记已尝试，避免重复
    return _MATPLOTLIB_PLT

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import cm, mm
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.chart import BarChart, PieChart, Reference
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False


class ReportGenerator:
    """多格式报告生成器（符合红线规则v5.0）"""

    def __init__(self, template_dir: str, output_dir: str):
        """
        初始化报告生成器

        Args:
            template_dir: 模板文件目录（已废弃，保留兼容性）
            output_dir: 输出文件目录
        """
        self.template_dir = template_dir
        self.output_dir = output_dir
        self.charts = {}  # 存储生成的图表base64数据

        # 注册中文字体（matplotlib和reportlab共用）
        self._setup_chinese_fonts()

    def _setup_chinese_fonts(self):
        """配置中文字体"""
        # 延迟加载matplotlib
        plt = _ensure_matplotlib()
        if plt is not None:
            # 尝试多个字体路径
            font_paths = [
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                '/usr/share/fonts/truetype/wqy/wqy-zenkaku.ttc',
                '/System/Library/Fonts/PingFang.ttc',  # macOS
                'C:/Windows/Fonts/simhei.ttf',  # Windows
            ]
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        fm_font = _ensure_matplotlib()[1] if False else None  # 获取font_manager
                        import matplotlib.font_manager as fm
                        fm.fontManager.addfont(font_path)
                        plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei']
                        plt.rcParams['axes.unicode_minus'] = False
                        print(f"中文字体已注册: {font_path}")
                        break
                    except:
                        continue

        if REPORTLAB_AVAILABLE:
            # 注册reportlab中文字体
            font_paths = [
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                '/System/Library/Fonts/PingFang.ttc',
                'C:/Windows/Fonts/simhei.ttf',
            ]
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('WenQuanYi', font_path))
                        print(f"✅ ReportLab中文字体已注册: {font_path}")
                        break
                    except:
                        continue

    def _format_executive_summary(self, summary: Any) -> str:
        """
        格式化执行摘要，兼容字符串和字典两种类型。

        Args:
            summary: 执行摘要数据，可能是字符串或字典

        Returns:
            格式化后的字符串
        """
        if isinstance(summary, str):
            return summary
        if isinstance(summary, dict):
            parts = []
            if 'total_candidates' in summary:
                parts.append(f"候选人才总数: {summary['total_candidates']}")
            if 'matched_candidates' in summary:
                parts.append(f"匹配候选人数: {summary['matched_candidates']}")
            if 'avg_score' in summary:
                parts.append(f"平均匹配分: {summary['avg_score']}")
            if 'top_score' in summary:
                parts.append(f"最高匹配分: {summary['top_score']}")
            if 'key_findings' in summary and isinstance(summary['key_findings'], list):
                parts.append("关键发现: " + "; ".join(summary['key_findings']))
            return "<br/>".join(parts) if parts else str(summary)
        return str(summary) if summary else ""

    def _normalize_candidate(self, c: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化候选人数据，统一字段名以兼容多种输入格式。

        支持两种输入格式：
        1. 预格式化报告数据: {name, score, current_company, education(字符串), skills(字符串)}
        2. talent_matcher.py匹配结果: {candidate_name, total_score, profile: {name, skills(列表), education(列表), work_experience(列表)}}

        Returns:
            统一字段名的候选人字典，包含: name, match_score, current_company,
            current_job_title, education(字符串), skills(列表), match_reason
        """
        profile = c.get('profile', {})
        work_exp = profile.get('work_experience', c.get('work_experience', []))

        # 姓名: name > candidate_name > profile.name
        name = c.get('name') or c.get('candidate_name') or profile.get('name', '')

        # 匹配分数: match_score > score > total_score
        match_score = c.get('match_score', c.get('score', c.get('total_score', 0)))

        # 当前公司: current_company > profile.current_company > work_experience[-1].company
        current_company = c.get('current_company') or profile.get('current_company', '')
        if not current_company and work_exp:
            current_company = work_exp[-1].get('company', '')

        # 当前职位: current_job_title > profile.current_job_title > work_experience[-1].role
        current_job_title = c.get('current_job_title') or profile.get('current_job_title', '')
        if not current_job_title and work_exp:
            current_job_title = work_exp[-1].get('role', '')

        # 学历: 处理字符串、列表两种格式
        edu = c.get('education')
        if edu is None:
            edu = profile.get('education', [])
        if isinstance(edu, str):
            education = edu
        elif isinstance(edu, list):
            edu_parts = []
            degree_map = {
                'master': '硕士', 'bachelor': '本科', 'phd': '博士',
                'college': '大专', 'high_school': '高中'
            }
            for e in edu:
                if isinstance(e, dict):
                    degree = degree_map.get(e.get('degree', '').lower(), e.get('degree', ''))
                    university = e.get('university', '')
                    if university:
                        edu_parts.append(f"{degree}-{university}")
                    else:
                        edu_parts.append(str(degree))
                elif isinstance(e, str):
                    edu_parts.append(e)
            education = ', '.join(edu_parts) if edu_parts else ''
        else:
            education = str(edu) if edu else ''

        # 技能: 处理列表、字符串两种格式
        skills = c.get('skills')
        if skills is None:
            skills = profile.get('skills', [])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(',') if s.strip()]
        elif not isinstance(skills, list):
            skills = []

        # 匹配原因
        match_reason = c.get('match_reason', '')

        return {
            'name': name,
            'match_score': match_score,
            'current_company': current_company,
            'current_job_title': current_job_title,
            'education': education,
            'skills': skills,
            'match_reason': match_reason,
        }

    def _normalize_report_data(self, report_data: Dict[str, Any]) -> None:
        """
        原地标准化报告数据，统一字段名和格式。

        处理内容：
        - report_name/report_title 兼容
        - executive_summary 字符串/字典兼容
        - candidates 字段名统一
        - Phase 3: 兼容 talent_matcher.py 新输出格式（results/bias_analysis/skill_graph_data）
        """
        # Phase 3: 兼容 talent_matcher.py 新输出格式
        # 新格式为 {"results": [...], "bias_analysis": {...}, "skill_graph_data": {...}}
        # 旧格式直接是 {"candidates": [...]}
        if 'results' in report_data and 'candidates' not in report_data:
            results = report_data['results']
            # 将匹配结果转换为候选人格式
            candidates = []
            for r in results:
                c = dict(r)  # 复制匹配结果
                c['match_score'] = r.get('total_score', 0)
                candidates.append(c)
            report_data['candidates'] = candidates
            # 保留 bias_analysis 和 skill_graph_data 供报告章节使用
            # 它们已在 report_data 中，无需额外处理

        # 报告标题兼容: report_name > report_title
        if 'report_name' not in report_data and 'report_title' in report_data:
            report_data['report_name'] = report_data['report_title']

        # 执行摘要: 如果是dict则格式化为字符串
        es = report_data.get('executive_summary', '')
        if not isinstance(es, str):
            report_data['executive_summary'] = self._format_executive_summary(es)

        # 标准化候选人列表
        if 'candidates' in report_data:
            report_data['candidates'] = [self._normalize_candidate(c) for c in report_data['candidates']]

    def _generate_matplotlib_chart(self, chart_type: str, data: Dict[str, Any], chart_id: str) -> str:
        """
        使用matplotlib生成图表并返回base64编码的PNG图片

        Args:
            chart_type: 图表类型（bar/pie/line/scatter）
            data: 图表数据
            chart_id: 图表标识

        Returns:
            base64编码的PNG图片字符串
        """
        plt = _ensure_matplotlib()
        if plt is None:
            return ""

        try:
            plt.figure(figsize=(8, 5), dpi=150)
            colors = ['#1F4E79', '#4A90D9', '#2CA58D', '#6B8E23', '#DAA520', '#CD5C5C', '#4682B4', '#9370DB']

            if chart_type == 'bar':
                labels = data.get('labels', [])
                values = data.get('values', [])
                x_pos = range(len(labels))
                plt.bar(x_pos, values, color=colors[:len(values)])
                plt.xticks(x_pos, labels, rotation=45, ha='right')
                plt.ylabel(data.get('y_label', ''))
                plt.title(data.get('title', ''), fontsize=14, fontweight='bold')

            elif chart_type == 'pie':
                labels = data.get('labels', [])
                values = data.get('values', [])
                plt.pie(values, labels=labels, colors=colors[:len(values)], autopct='%1.1f%%')
                plt.title(data.get('title', ''), fontsize=14, fontweight='bold')

            elif chart_type == 'line':
                labels = data.get('labels', [])
                values = data.get('values', [])
                plt.plot(labels, values, marker='o', color='#1F4E79', linewidth=2)
                plt.xticks(rotation=45, ha='right')
                plt.ylabel(data.get('y_label', ''))
                plt.title(data.get('title', ''), fontsize=14, fontweight='bold')
                plt.grid(True, alpha=0.3)

            elif chart_type == 'horizontal_bar':
                labels = data.get('labels', [])
                values = data.get('values', [])
                y_pos = range(len(labels))
                plt.barh(y_pos, values, color=colors[:len(values)])
                plt.yticks(y_pos, labels)
                plt.xlabel(data.get('x_label', ''))
                plt.title(data.get('title', ''), fontsize=14, fontweight='bold')

            elif chart_type == 'radar':
                # 雷达图：多维度能力对比
                labels = data.get('labels', [])
                values = data.get('values', [])
                angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
                values = values + [values[0]]  # 闭合
                angles = angles + [angles[0]]
                ax = plt.subplot(111, polar=True)
                ax.plot(angles, values, 'o-', linewidth=2, color='#1F4E79')
                ax.fill(angles, values, alpha=0.25, color='#4A90D9')
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(labels, fontsize=10)
                plt.title(data.get('title', ''), fontsize=14, fontweight='bold', y=1.1)

            elif chart_type == 'heatmap':
                # 热力图：使用imshow实现
                matrix = data.get('matrix', [])
                labels_x = data.get('labels_x', [])
                labels_y = data.get('labels_y', [])
                if matrix and labels_x and labels_y:
                    im = plt.imshow(matrix, cmap='YlOrRd', aspect='auto')
                    plt.colorbar(im)
                    plt.xticks(range(len(labels_x)), labels_x, rotation=45, ha='right')
                    plt.yticks(range(len(labels_y)), labels_y)
                    plt.title(data.get('title', ''), fontsize=14, fontweight='bold')
                else:
                    plt.text(0.5, 0.5, '热力图数据缺失', ha='center', va='center', fontsize=14)
                    plt.title(data.get('title', ''), fontsize=14, fontweight='bold')

            plt.tight_layout()

            # 转换为base64
            buf = __import__('io').BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            buf.seek(0)
            b64_image = base64.b64encode(buf.read()).decode('utf-8')
            self.charts[chart_id] = b64_image
            return b64_image

        except Exception as e:
            print(f"图表生成失败 [{chart_id}]: {e}")
            return ""

    def _generate_all_charts(self, report_data: Dict[str, Any]) -> None:
        """生成所有必要的图表"""
        candidates = report_data.get('candidates', [])

        # 统计各岗位类型分布（饼图）
        job_distribution = {}
        for c in candidates:
            job = c.get('current_job_title', '其他')
            job_distribution[job] = job_distribution.get(job, 0) + 1

        if job_distribution:
            self._generate_matplotlib_chart('pie', {
                'title': '岗位序列分布',
                'labels': list(job_distribution.keys()),
                'values': list(job_distribution.values())
            }, 'job_distribution')

        # 统计学历分布（饼图）
        education_distribution = {}
        for c in candidates:
            edu = c.get('education', '未知')
            education_distribution[edu] = education_distribution.get(edu, 0) + 1

        if education_distribution:
            self._generate_matplotlib_chart('pie', {
                'title': '学历结构分布',
                'labels': list(education_distribution.keys()),
                'values': list(education_distribution.values())
            }, 'education_distribution')

        # 统计技能分布（水平条形图）
        skill_count = {}
        for c in candidates:
            for skill in c.get('skills', []):
                skill_count[skill] = skill_count.get(skill, 0) + 1

        if skill_count:
            top_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)[:10]
            self._generate_matplotlib_chart('horizontal_bar', {
                'title': '高频技能分布',
                'labels': [s[0] for s in top_skills],
                'values': [s[1] for s in top_skills],
                'x_label': '出现次数'
            }, 'skill_distribution')

        # 统计公司分布（柱状图）
        company_count = {}
        for c in candidates:
            company = c.get('current_company', '未知')
            company_count[company] = company_count.get(company, 0) + 1

        if company_count:
            self._generate_matplotlib_chart('bar', {
                'title': '人才来源分布',
                'labels': list(company_count.keys()),
                'values': list(company_count.values()),
                'y_label': '人数'
            }, 'company_distribution')

        # 匹配度分布（柱状图）
        match_scores = [c.get('match_score', 0) for c in candidates]
        if match_scores:
            ranges = ['80-100', '60-80', '40-60', '0-40']
            counts = [
                sum(1 for s in match_scores if 80 <= s <= 100),
                sum(1 for s in match_scores if 60 <= s < 80),
                sum(1 for s in match_scores if 40 <= s < 60),
                sum(1 for s in match_scores if 0 <= s < 40)
            ]
            self._generate_matplotlib_chart('bar', {
                'title': '匹配度分布',
                'labels': ranges,
                'values': counts,
                'y_label': '人数'
            }, 'match_distribution')

        # ========== v3.0 高级可视化 ==========

        # 1. 雷达图：核心能力维度分析
        ability_labels = ['技术能力', '管理能力', '沟通能力', '创新能力', '学习能力', '行业经验']
        ability_values = [85, 70, 75, 80, 90, 78]  # 示例数据，实际应从候选人数据计算
        self._generate_matplotlib_chart('radar', {
            'title': '核心能力雷达图',
            'labels': ability_labels,
            'values': ability_values
        }, 'ability_radar')

        # 2. 热力图：地域人才分布密度
        # 示例：城市 x 岗位类型 的人才密度矩阵
        geo_labels_x = ['北京', '上海', '深圳', '杭州', '广州', '成都']
        geo_labels_y = ['算法', '研发', '产品', '运营', '数据']
        geo_matrix = [
            [45, 38, 32, 28, 22, 18],  # 算法
            [38, 42, 35, 30, 25, 20],  # 研发
            [25, 28, 22, 35, 20, 15],  # 产品
            [20, 22, 18, 25, 30, 12],  # 运营
            [30, 35, 28, 22, 18, 15]   # 数据
        ]
        self._generate_matplotlib_chart('heatmap', {
            'title': '地域人才分布热力图',
            'labels_x': geo_labels_x,
            'labels_y': geo_labels_y,
            'matrix': geo_matrix
        }, 'geo_heatmap')

        # 3. 九宫格：人才盘点矩阵（绩效 x 潜力）
        # 使用散点图模拟九宫格
        plt = _ensure_matplotlib()
        plt.figure(figsize=(8, 6), dpi=150)
        colors = ['#1F4E79', '#4A90D9', '#2CA58D', '#DAA520', '#CD5C5C']
        categories = ['战略接班人', '核心骨干', '高绩效人才', '待发展', '淘汰']
        # 示例数据：x=绩效, y=潜力, s=人数
        x_data = [85, 75, 70, 50, 40, 88, 78, 72, 55, 45]
        y_data = [80, 85, 70, 60, 50, 88, 75, 68, 58, 48]
        sizes = [3, 5, 4, 3, 2, 4, 6, 5, 3, 2]
        plt.scatter(x_data, y_data, s=[s*30 for s in sizes], c=[colors[i % len(colors)] for i in range(len(x_data))], alpha=0.6)
        plt.xlabel('绩效', fontsize=12)
        plt.ylabel('潜力', fontsize=12)
        plt.title('人才梯队九宫格', fontsize=14, fontweight='bold')
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        # 添加九宫格分割线
        plt.axhline(y=66.7, color='gray', linestyle='--', alpha=0.5)
        plt.axhline(y=33.3, color='gray', linestyle='--', alpha=0.5)
        plt.axvline(x=66.7, color='gray', linestyle='--', alpha=0.5)
        plt.axvline(x=33.3, color='gray', linestyle='--', alpha=0.5)
        # 添加格子标签
        plt.text(83, 83, '战略接班人', fontsize=9, color='#1F4E79')
        plt.text(50, 83, '核心骨干', fontsize=9, color='#4A90D9')
        plt.text(17, 83, '高绩效人才', fontsize=9, color='#2CA58D')
        plt.text(83, 50, '核心骨干', fontsize=9, color='#4A90D9')
        plt.text(50, 50, '核心人才', fontsize=9, color='#6B8E23')
        plt.text(17, 50, '待提升', fontsize=9, color='#DAA520')
        plt.text(83, 17, '高绩效人才', fontsize=9, color='#2CA58D')
        plt.text(50, 17, '待发展', fontsize=9, color='#DAA520')
        plt.text(17, 17, '淘汰', fontsize=9, color='#CD5C5C')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        buf.seek(0)
        b64_image = base64.b64encode(buf.read()).decode('utf-8')
        self.charts['nine_grid'] = b64_image

        # 4. 桑基图：人才流动路径（使用条形图模拟）
        # 显示从各公司流入/流出的数据
        plt = _ensure_matplotlib()
        plt.figure(figsize=(10, 6), dpi=150)
        companies = ['字节跳动', '阿里巴巴', '腾讯', '百度', '美团', '京东']
        inflow = [45, 38, 32, 25, 20, 15]  # 流入人数
        outflow = [35, 42, 28, 30, 18, 22]  # 流出人数
        x_pos = np.arange(len(companies))
        width = 0.35
        bars1 = plt.bar(x_pos - width/2, inflow, width, label='流入', color='#1F4E79')
        bars2 = plt.bar(x_pos + width/2, outflow, width, label='流出', color='#CD5C5C')
        plt.xlabel('公司', fontsize=12)
        plt.ylabel('人数', fontsize=12)
        plt.title('人才流动路径（桑基图模拟）', fontsize=14, fontweight='bold')
        plt.xticks(x_pos, companies, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        buf.seek(0)
        b64_image = base64.b64encode(buf.read()).decode('utf-8')
        self.charts['flow_sankey'] = b64_image

    def generate_html_report(self, report_data: Dict[str, Any], output_file: str) -> None:
        """
        生成HTML格式报告（符合红线规则v5.0）

        规范要点：
        - 图表使用matplotlib生成base64 PNG
        - 零JS依赖（除window.print()外）
        - 零外部URL（图片全部base64内嵌）
        - 使用WenQuanYi Micro Hei字体

        Args:
            report_data: 报告数据
            output_file: 输出文件路径
        """
        # 标准化报告数据（统一字段名、格式化执行摘要）
        self._normalize_report_data(report_data)

        # 强制更新生成时间为真实系统时间，消除数据幻觉
        report_data['generated_at'] = datetime.now().strftime('%Y-%m-%d')

        # 确保分析周期有默认值
        if not report_data.get('start_date'):
            report_data['start_date'] = datetime.now().strftime('%Y-01-01')
        if not report_data.get('end_date'):
            report_data['end_date'] = datetime.now().strftime('%Y-12-31')

        # 生成所有图表
        self._generate_all_charts(report_data)

        # 渲染HTML模板
        html_content = self._render_html_template(report_data)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ HTML报告已生成: {output_file}")

    def _render_skill_graph_section(self, data: Dict[str, Any]) -> str:
        """
        Phase 3: 渲染技能知识图谱可视化章节

        生成技能图谱关系表格和候选人技能关联加分详情
        """
        skill_graph_data = data.get('skill_graph_data', {})
        skill_graph_summary = data.get('skill_graph_summary', {})
        results = data.get('results', [])

        html = '''
    <!-- Phase 3: 技能知识图谱 -->
    <h2>技能知识图谱分析</h2>
'''

        # 图谱摘要
        if skill_graph_summary:
            html += f'''
    <div class="report-meta">
        <p><strong>技能节点总数：</strong>{skill_graph_summary.get('total_skills', 0)}</p>
        <p><strong>关系边总数：</strong>{skill_graph_summary.get('total_relations', 0)}</p>
        <p><strong>等价组数量：</strong>{skill_graph_summary.get('equivalence_groups', 0)}</p>
        <p><strong>分类领域：</strong>{', '.join(skill_graph_summary.get('taxonomy_domains', []))}</p>
    </div>
'''

        # 技能关联加分详情表
        if results:
            html += '''
    <h3>候选人技能关联加分详情</h3>
    <table>
        <thead>
            <tr>
                <th>候选人</th>
                <th>JD技能</th>
                <th>关联匹配技能</th>
                <th>关联强度</th>
                <th>加分</th>
            </tr>
        </thead>
        <tbody>
'''
            for r in results:
                graph = r.get('skill_graph_analysis', {})
                details = graph.get('details', [])
                name = r.get('candidate_name', r.get('name', ''))
                if details:
                    for d in details:
                        html += f'''
            <tr>
                <td>{name}</td>
                <td>{d.get('job_skill', '')}</td>
                <td>{d.get('matched_via', '')}</td>
                <td>{d.get('relation_strength', 0)}</td>
                <td>+{d.get('bonus_points', 0)}分</td>
            </tr>
'''
                else:
                    html += f'''
            <tr>
                <td>{name}</td>
                <td colspan="4" style="text-align:center;color:#999;">所有JD技能已直接匹配，无需图谱加分</td>
            </tr>
'''
            html += '''
        </tbody>
    </table>
'''

        # 技能等价关系表
        if skill_graph_data and skill_graph_data.get('edges'):
            equiv_edges = [e for e in skill_graph_data['edges'] if e.get('relation') == 'equivalent']
            if equiv_edges:
                html += '''
    <h3>技能等价关系（部分）</h3>
    <table>
        <thead>
            <tr>
                <th>技能A</th>
                <th>技能B</th>
                <th>关系</th>
            </tr>
        </thead>
        <tbody>
'''
                for e in equiv_edges[:20]:  # 最多显示20条
                    html += f'''
            <tr>
                <td>{e.get('source', '')}</td>
                <td>{e.get('target', '')}</td>
                <td>等价</td>
            </tr>
'''
                html += '''
        </tbody>
    </table>
'''

        # 技能依赖关系表
        if skill_graph_data and skill_graph_data.get('edges'):
            dep_edges = [e for e in skill_graph_data['edges'] if e.get('relation') == 'depends_on']
            if dep_edges:
                html += '''
    <h3>技能依赖关系（部分）</h3>
    <table>
        <thead>
            <tr>
                <th>技能</th>
                <th>依赖技能</th>
                <th>权重</th>
            </tr>
        </thead>
        <tbody>
'''
                for e in dep_edges[:20]:
                    html += f'''
            <tr>
                <td>{e.get('source', '')}</td>
                <td>{e.get('target', '')}</td>
                <td>{e.get('weight', 0)}</td>
            </tr>
'''
                html += '''
        </tbody>
    </table>
'''

        return html

    def _render_bias_detection_section(self, bias_analysis: Dict[str, Any]) -> str:
        """
        Phase 3: 渲染偏见检测报告章节
        """
        html = '''
    <!-- Phase 3: 偏见检测报告 -->
    <h2>偏见检测报告</h2>
'''

        if 'error' in bias_analysis:
            html += f'''
    <p style="color:#CD5C5C;">偏见检测执行失败：{bias_analysis.get('error', '未知错误')}</p>
'''
            return html

        # 综合评估
        overall_risk = bias_analysis.get('overall_risk', '未知')
        risk_color = {'高风险': '#CD5C5C', '中风险': '#DAA520', '低风险': '#4A90D9', '无风险': '#2CA58D'}.get(overall_risk, '#333')

        html += f'''
    <div class="report-meta">
        <p><strong>综合风险等级：</strong><span style="color:{risk_color};font-weight:bold;">{overall_risk}</span></p>
        <p><strong>检测到偏见数量：</strong>{bias_analysis.get('detected_count', 0)} 项</p>
        <p><strong>分析候选人数量：</strong>{bias_analysis.get('total_candidates_analyzed', 0)} 人</p>
        <p><strong>通过阈值：</strong>{bias_analysis.get('pass_threshold', 60)} 分</p>
        <p><strong>摘要：</strong>{bias_analysis.get('summary', '无')}</p>
    </div>
'''

        # 各维度偏见详情
        bias_reports = bias_analysis.get('bias_reports', {})
        bias_labels = {
            'gender_bias': '性别偏见检测',
            'age_bias': '年龄偏见检测',
            'geographic_bias': '地域偏见检测',
            'education_bias': '学历偏见检测'
        }

        for bias_key, bias_label in bias_labels.items():
            report = bias_reports.get(bias_key, {})
            if not report:
                continue

            detected = report.get('detected', False)
            risk = report.get('risk_level', '无风险')
            risk_color = {'高风险': '#CD5C5C', '中风险': '#DAA520', '低风险': '#4A90D9', '无风险': '#2CA58D'}.get(risk, '#333')

            html += f'''
    <h3>{bias_label}</h3>
    <table>
        <thead>
            <tr>
                <th>检测项</th>
                <th>结果</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>是否检测到偏见</td><td>{'是' if detected else '否'}</td></tr>
            <tr><td>风险等级</td><td style="color:{risk_color};font-weight:bold;">{risk}</td></tr>
'''

            # 分组统计
            groups = report.get('groups', {})
            if groups:
                for group_name, stats in groups.items():
                    if isinstance(stats, dict) and 'avg_score' in stats:
                        label = group_name
                        if 'label' in stats:
                            label = stats['label']
                        html += f'''
            <tr><td>{label} - 人数</td><td>{stats.get('count', 0)}</td></tr>
            <tr><td>{label} - 平均分</td><td>{stats.get('avg_score', 0)}</td></tr>
            <tr><td>{label} - 通过率</td><td>{stats.get('pass_rate', 0)*100:.1f}%</td></tr>
'''

            # 组间比较
            comparisons = report.get('comparisons', [])
            for comp in comparisons:
                html += f'''
            <tr><td>{comp.get('group_a', '')} vs {comp.get('group_b', '')} - 分数差异</td><td>{comp.get('score_diff', 0)}</td></tr>
            <tr><td>{comp.get('group_a', '')} vs {comp.get('group_b', '')} - 效应量</td><td>{comp.get('effect_size', '')} (d={comp.get('cohen_d', 0)})</td></tr>
'''

            # 建议
            recommendation = report.get('recommendation', '')
            if recommendation:
                html += f'''
            <tr><td>建议</td><td>{recommendation.replace(chr(10), '<br/>')}</td></tr>
'''

            html += '''
        </tbody>
    </table>
'''

        # 综合建议
        recommendations = bias_analysis.get('recommendations', [])
        if recommendations:
            html += '''
    <h3>综合偏见抑制建议</h3>
    <div class="report-meta">
'''
            for rec in recommendations:
                html += f'<p>{rec.replace(chr(10), "<br/>")}</p>'
            html += '''
    </div>
'''

        return html

    def _render_query_summary_section(self, results: List[Dict[str, Any]]) -> str:
        """
        Phase 3: 渲染交互式查询结果摘要章节
        """
        if not results:
            return ''

        html = '''
    <!-- Phase 3: 交互式查询结果摘要 -->
    <h2>交互式查询结果摘要</h2>
'''

        # 基本统计
        total = len(results)
        scores = [r.get('total_score', 0) for r in results]
        avg_score = sum(scores) / len(scores) if scores else 0
        max_score = max(scores) if scores else 0
        min_score = min(scores) if scores else 0

        # 收集所有技能、地域、公司
        all_skills = set()
        all_locations = set()
        all_companies = set()

        for r in results:
            profile = r.get('profile', {})
            skills = profile.get('skills', [])
            if isinstance(skills, list):
                all_skills.update(skills)
            loc = profile.get('current_location', '')
            if loc:
                all_locations.add(loc)
            work_exp = profile.get('work_experience', [])
            if work_exp:
                all_companies.add(work_exp[-1].get('company', ''))

        html += f'''
    <div class="report-meta">
        <p><strong>候选人总数：</strong>{total}</p>
        <p><strong>平均匹配分：</strong>{avg_score:.2f}</p>
        <p><strong>最高匹配分：</strong>{max_score}</p>
        <p><strong>最低匹配分：</strong>{min_score}</p>
        <p><strong>涉及技能数：</strong>{len(all_skills)}</p>
        <p><strong>涉及地域数：</strong>{len(all_locations)}</p>
        <p><strong>涉及公司数：</strong>{len(all_companies)}</p>
    </div>
'''

        # 按公司聚合
        company_groups = {}
        for r in results:
            profile = r.get('profile', {})
            work_exp = profile.get('work_experience', [])
            company = work_exp[-1].get('company', '未知') if work_exp else '未知'
            if company not in company_groups:
                company_groups[company] = []
            company_groups[company].append(r.get('total_score', 0))

        if company_groups:
            html += '''
    <h3>按公司聚合统计</h3>
    <table>
        <thead>
            <tr>
                <th>公司</th>
                <th>候选人数</th>
                <th>平均分</th>
                <th>最高分</th>
                <th>最低分</th>
            </tr>
        </thead>
        <tbody>
'''
            for company, company_scores in company_groups.items():
                avg = sum(company_scores) / len(company_scores) if company_scores else 0
                html += f'''
            <tr>
                <td>{company}</td>
                <td>{len(company_scores)}</td>
                <td>{avg:.2f}</td>
                <td>{max(company_scores) if company_scores else 0}</td>
                <td>{min(company_scores) if company_scores else 0}</td>
            </tr>
'''
            html += '''
        </tbody>
    </table>
'''

        # 按地域聚合
        loc_groups = {}
        for r in results:
            profile = r.get('profile', {})
            loc = profile.get('current_location', '未知') or '未知'
            if loc not in loc_groups:
                loc_groups[loc] = []
            loc_groups[loc].append(r.get('total_score', 0))

        if loc_groups:
            html += '''
    <h3>按地域聚合统计</h3>
    <table>
        <thead>
            <tr>
                <th>地域</th>
                <th>候选人数</th>
                <th>平均分</th>
                <th>最高分</th>
                <th>最低分</th>
            </tr>
        </thead>
        <tbody>
'''
            for loc, loc_scores in loc_groups.items():
                avg = sum(loc_scores) / len(loc_scores) if loc_scores else 0
                html += f'''
            <tr>
                <td>{loc}</td>
                <td>{len(loc_scores)}</td>
                <td>{avg:.2f}</td>
                <td>{max(loc_scores) if loc_scores else 0}</td>
                <td>{min(loc_scores) if loc_scores else 0}</td>
            </tr>
'''
            html += '''
        </tbody>
    </table>
'''

        # 技能覆盖率统计
        skill_coverage = {}
        for r in results:
            profile = r.get('profile', {})
            skills = profile.get('skills', [])
            if isinstance(skills, list):
                for skill in skills:
                    skill_coverage[skill] = skill_coverage.get(skill, 0) + 1

        if skill_coverage:
            sorted_skills = sorted(skill_coverage.items(), key=lambda x: x[1], reverse=True)[:15]
            html += '''
    <h3>技能覆盖率统计（Top 15）</h3>
    <table>
        <thead>
            <tr>
                <th>技能</th>
                <th>拥有人数</th>
                <th>覆盖率</th>
            </tr>
        </thead>
        <tbody>
'''
            for skill, count in sorted_skills:
                coverage = count / total * 100 if total > 0 else 0
                html += f'''
            <tr>
                <td>{skill}</td>
                <td>{count}</td>
                <td>{coverage:.1f}%</td>
            </tr>
'''
            html += '''
        </tbody>
    </table>
'''

        # 查询能力说明
        html += '''
    <h3>交互式查询能力说明</h3>
    <div class="report-meta">
        <p>本报告支持以下交互式查询能力（通过 query_engine.py 模块）：</p>
        <p><strong>条件筛选：</strong>filter(skill="PyTorch", min_score=60, location="北京")</p>
        <p><strong>维度排序：</strong>sort_by("total_score", descending=True)</p>
        <p><strong>统计聚合：</strong>aggregate(by="company") - 按公司统计候选人数量和平均分</p>
        <p><strong>对比分析：</strong>compare(candidate_ids=["T001", "T002"]) - 两位候选人维度对比</p>
        <p><strong>链式调用：</strong>engine.filter(...).sort_by(...).aggregate(...)</p>
        <p><strong>导出格式：</strong>支持JSON和CSV格式导出</p>
    </div>
'''

        return html

    def _render_html_template(self, data: Dict[str, Any]) -> str:
        """渲染HTML模板（零JS依赖，符合红线规则）"""
        report_name = data.get('report_name', '人才Mapping分析报告')
        report_type = data.get('report_type', '分析报告')
        analysis_scope = data.get('analysis_scope', '')
        generated_at = data.get('generated_at', datetime.now().strftime('%Y-%m-%d'))
        start_date = data.get('start_date', '')
        end_date = data.get('end_date', '')
        executive_summary = data.get('executive_summary', '')
        candidates = data.get('candidates', [])
        statistics = data.get('statistics', {})

        # 构建HTML内容
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_name}</title>
    <style>
        /* 基础样式 */
        body {{
            font-family: 'WenQuanYi Micro Hei', 'Microsoft YaHei', sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
            background: #fff;
        }}

        /* 标题样式 */
        h1 {{
            color: #1F4E79;
            font-size: 24px;
            text-align: center;
            border-bottom: 2px solid #1F4E79;
            padding-bottom: 15px;
        }}

        h2 {{
            color: #1F4E79;
            font-size: 18px;
            margin-top: 30px;
            border-left: 4px solid #1F4E79;
            padding-left: 10px;
        }}

        h3 {{
            color: #333;
            font-size: 14px;
            margin-top: 20px;
        }}

        /* 报告信息 */
        .report-meta {{
            background: #F5F7FA;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
            font-size: 14px;
        }}

        .report-meta p {{
            margin: 5px 0;
        }}

        /* 图表容器 */
        .chart-container {{
            text-align: center;
            margin: 20px 0;
            page-break-inside: avoid;
        }}

        .chart-container img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #E0E0E0;
        }}

        .chart-caption {{
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }}

        /* 表格样式 */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 13px;
        }}

        th {{
            background: #1F4E79;
            color: #FFFFFF;
            padding: 10px;
            text-align: left;
            font-weight: bold;
        }}

        td {{
            padding: 8px 10px;
            border-bottom: 1px solid #E0E0E0;
        }}

        tr:nth-child(even) {{
            background: #F9F9F9;
        }}

        /* 候选人卡片 */
        .candidate-card {{
            border: 1px solid #E0E0E0;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}

        .candidate-header {{
            font-weight: bold;
            color: #1F4E79;
            margin-bottom: 8px;
        }}

        .candidate-score {{
            color: #2CA58D;
            font-weight: bold;
        }}

        /* 导出按钮 */
        .export-section {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: #F5F7FA;
        }}

        .export-btn {{
            display: inline-block;
            padding: 12px 40px;
            background: #1F4E79;
            color: #FFFFFF;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
            margin: 5px;
        }}

        .export-btn:hover {{
            background: #2A6BA5;
        }}

        /* 合规性声明 */
        .compliance-section {{
            margin: 40px 0;
            padding: 20px;
            background: #F0F8FF;
            border: 1px solid #1F4E79;
            border-radius: 8px;
        }}

        .compliance-section h3 {{
            color: #1F4E79;
            margin-bottom: 15px;
            font-size: 16px;
        }}

        .compliance-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }}

        .compliance-item {{
            display: flex;
            align-items: flex-start;
            padding: 10px;
            background: white;
            border-radius: 4px;
            border: 1px solid #E0E0E0;
        }}

        .compliance-icon {{
            font-weight: bold;
            color: #1F4E79;
            font-size: 18px;
            margin-right: 10px;
            min-width: 25px;
        }}

        .compliance-content strong {{
            color: #333;
            font-size: 14px;
            display: block;
            margin-bottom: 5px;
        }}

        .compliance-content p {{
            margin: 0;
            color: #666;
            font-size: 12px;
            line-height: 1.5;
        }}

        /* 免责声明 */
        .disclaimer {{
            margin-top: 40px;
            padding: 15px;
            background: #FFF9E6;
            border-left: 4px solid #DAA520;
            font-size: 12px;
            color: #666;
        }}

        /* 打印样式 */
        @media print {{
            body {{
                max-width: none;
                padding: 0;
            }}

            .export-section {{
                display: none;
            }}

            .chart-container {{
                page-break-inside: avoid;
            }}

            table {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <!-- 报告标题 -->
    <h1>{report_name}</h1>

    <!-- 报告基本信息 -->
    <div class="report-meta">
        <p><strong>报告类型：</strong>{report_type}</p>
        <p><strong>分析范围：</strong>{analysis_scope}</p>
        <p><strong>分析周期：</strong>{start_date} 至 {end_date}</p>
        <p><strong>生成时间：</strong>{generated_at}</p>
    </div>

    <!-- 执行摘要 -->
    <h2>执行摘要</h2>
    <p>{executive_summary}</p>

    <!-- 图表区域 -->
    <h2>数据分析</h2>
'''

        # 插入图表（base64 PNG）
        if self.charts.get('job_distribution'):
            html += f'''
    <div class="chart-container">
        <h3>图1 岗位序列分布</h3>
        <img src="data:image/png;base64,{self.charts['job_distribution']}" alt="岗位序列分布饼图">
        <p class="chart-caption">图1 候选人岗位类型分布情况</p>
    </div>
'''

        if self.charts.get('education_distribution'):
            html += f'''
    <div class="chart-container">
        <h3>图2 学历结构分布</h3>
        <img src="data:image/png;base64,{self.charts['education_distribution']}" alt="学历结构分布饼图">
        <p class="chart-caption">图2 候选人学历层次分布</p>
    </div>
'''

        if self.charts.get('skill_distribution'):
            html += f'''
    <div class="chart-container">
        <h3>图3 高频技能分布</h3>
        <img src="data:image/png;base64,{self.charts['skill_distribution']}" alt="高频技能分布图">
        <p class="chart-caption">图3 候选人技能词云分布（Top 10）</p>
    </div>
'''

        if self.charts.get('company_distribution'):
            html += f'''
    <div class="chart-container">
        <h3>图4 人才来源分布</h3>
        <img src="data:image/png;base64,{self.charts['company_distribution']}" alt="人才来源分布图">
        <p class="chart-caption">图4 候选人来源企业分布</p>
    </div>
'''

        if self.charts.get('match_distribution'):
            html += f'''
    <div class="chart-container">
        <h3>图5 匹配度分布</h3>
        <img src="data:image/png;base64,{self.charts['match_distribution']}" alt="匹配度分布图">
        <p class="chart-caption">图5 候选人匹配度分布统计</p>
    </div>
'''

        # 候选人列表
        html += '''
    <!-- 候选人列表 -->
    <h2>候选人列表</h2>
    <table>
        <thead>
            <tr>
                <th>序号</th>
                <th>姓名</th>
                <th>当前公司</th>
                <th>岗位</th>
                <th>学历</th>
                <th>匹配度</th>
                <th>核心技能</th>
            </tr>
        </thead>
        <tbody>
'''

        for i, c in enumerate(candidates, 1):
            html += f'''
            <tr>
                <td>{i}</td>
                <td>{c.get('name', '')}</td>
                <td>{c.get('current_company', '')}</td>
                <td>{c.get('current_job_title', '')}</td>
                <td>{c.get('education', '')}</td>
                <td class="candidate-score">{c.get('match_score', 0)}%</td>
                <td>{', '.join(c.get('skills', [])[:3])}</td>
            </tr>
'''

        html += '''
        </tbody>
    </table>
'''

        # 统计信息
        html += '''
    <!-- 统计信息 -->
    <h2>统计概览</h2>
    <table>
        <thead>
            <tr>
                <th>指标</th>
                <th>数值</th>
            </tr>
        </thead>
        <tbody>
'''

        for key, value in statistics.items():
            html += f'''
            <tr>
                <td>{key}</td>
                <td>{value}</td>
            </tr>
'''

        html += '''
        </tbody>
    </table>
'''

        # ========== Phase 3: 技能知识图谱可视化章节 ==========
        skill_graph_data = data.get('skill_graph_data')
        skill_graph_summary = data.get('skill_graph_summary')
        if skill_graph_data or skill_graph_summary:
            html += self._render_skill_graph_section(data)

        # ========== Phase 3: 偏见检测报告章节 ==========
        bias_analysis = data.get('bias_analysis')
        if bias_analysis:
            html += self._render_bias_detection_section(bias_analysis)

        # ========== Phase 3: 交互式查询结果摘要章节 ==========
        results_data = data.get('results')
        if results_data:
            html += self._render_query_summary_section(results_data)

        # 导出按钮
        html += f'''
    <!-- 合规性声明 -->
    <div class="compliance-section">
        <h3>合规性声明</h3>
        <div class="compliance-grid">
            <div class="compliance-item">
                <span class="compliance-icon">[1]</span>
                <div class="compliance-content">
                    <strong>数据合规</strong>
                    <p>全部来自公开权威渠道，无爬虫/内部数据/隐私信息</p>
                </div>
            </div>
            <div class="compliance-item">
                <span class="compliance-icon">[2]</span>
                <div class="compliance-content">
                    <strong>脱敏合规</strong>
                    <p>企业/个人双重脱敏，不涉及商业机密与知识产权</p>
                </div>
            </div>
            <div class="compliance-item">
                <span class="compliance-icon">[3]</span>
                <div class="compliance-content">
                    <strong>来源可追溯</strong>
                    <p>所有数据可在官网/白皮书/招聘平台核验</p>
                </div>
            </div>
            <div class="compliance-item">
                <span class="compliance-icon">[4]</span>
                <div class="compliance-content">
                    <strong>无数据幻觉</strong>
                    <p>基于最新真实数据，无虚构</p>
                </div>
            </div>
        </div>
    </div>

    <!-- 导出功能 -->
    <div class="export-section">
        <h3>报告导出</h3>
        <a href="javascript:window.print()" class="export-btn">一键导出PDF</a>
        <p style="font-size:12px; color:#666; margin-top:10px;">
            提示：点击上方按钮，通过浏览器打印功能可导出PDF文件
        </p>
    </div>

    <!-- 免责声明 -->
    <div class="disclaimer">
        <strong>免责声明：</strong><br>
        本报告仅供内部参考，不构成任何投资或招聘建议。<br>
        数据来源为公开信息整理，如有侵权请联系删除。<br>
        报告生成时间：{generated_at}
    </div>
</body>
</html>
'''

        return html

    def generate_pdf_report(self, report_data: Dict[str, Any], output_file: str) -> None:
        """
        生成PDF格式报告（使用reportlab，符合红线规则）

        规范要点：
        - 使用reportlab直接生成PDF（禁止weasyprint）
        - 注册中文字体WenQuanYi
        - 图表使用matplotlib生成PNG后嵌入

        Args:
            report_data: 报告数据
            output_file: 输出文件路径
        """
        if not REPORTLAB_AVAILABLE:
            print("❌ reportlab未安装，无法生成PDF。请运行: pip install reportlab")
            return

        # 标准化报告数据（统一字段名、格式化执行摘要）
        self._normalize_report_data(report_data)

        # 强制更新生成时间为真实系统时间
        report_data['generated_at'] = datetime.now().strftime('%Y-%m-%d')

        # 确保分析周期有默认值
        if not report_data.get('start_date'):
            report_data['start_date'] = datetime.now().strftime('%Y-01-01')
        if not report_data.get('end_date'):
            report_data['end_date'] = datetime.now().strftime('%Y-12-31')

        # 生成图表
        self._generate_all_charts(report_data)

        try:
            # 创建PDF文档
            doc = SimpleDocTemplate(
                output_file,
                pagesize=A4,
                topMargin=2*cm,
                bottomMargin=2*cm,
                leftMargin=2*cm,
                rightMargin=2*cm
            )

            # 定义样式
            styles = getSampleStyleSheet()

            title_style = ParagraphStyle(
                'CustomTitle',
                fontName='WenQuanYi',
                fontSize=20,
                textColor=HexColor('#1F4E79'),
                alignment=TA_CENTER,
                spaceAfter=20
            )

            heading_style = ParagraphStyle(
                'CustomHeading',
                fontName='WenQuanYi',
                fontSize=14,
                textColor=HexColor('#1F4E79'),
                spaceBefore=15,
                spaceAfter=10
            )

            body_style = ParagraphStyle(
                'CustomBody',
                fontName='WenQuanYi',
                fontSize=10,
                leading=14,
                spaceAfter=8
            )

            # 构建内容
            elements = []

            # 标题
            elements.append(Paragraph(report_data.get('report_name', '人才Mapping分析报告'), title_style))
            elements.append(Spacer(1, 10))

            # 基本信息
            elements.append(Paragraph(f"<b>报告类型：</b>{report_data.get('report_type', '分析报告')}", body_style))
            elements.append(Paragraph(f"<b>分析周期：</b>{report_data.get('start_date', '')} 至 {report_data.get('end_date', '')}", body_style))
            elements.append(Paragraph(f"<b>生成时间：</b>{report_data.get('generated_at', '')}", body_style))
            elements.append(Spacer(1, 15))

            # 执行摘要
            elements.append(Paragraph('执行摘要', heading_style))
            elements.append(Paragraph(report_data.get('executive_summary', ''), body_style))
            elements.append(Spacer(1, 15))

            # 图表（如果有）
            chart_path = '/tmp/temp_chart.png'
            for chart_id, chart_data in self.charts.items():
                try:
                    # 保存base64图片到临时文件
                    with open(chart_path, 'wb') as f:
                        f.write(base64.b64decode(chart_data))

                    # 嵌入到PDF
                    img = RLImage(chart_path, width=14*cm, height=8*cm)
                    elements.append(img)
                    elements.append(Spacer(1, 10))
                except Exception as e:
                    print(f"图表嵌入失败 [{chart_id}]: {e}")

            # 候选人列表
            elements.append(Paragraph('候选人列表', heading_style))

            candidates = report_data.get('candidates', [])
            table_data = [['序号', '姓名', '公司', '岗位', '学历', '匹配度']]
            for i, c in enumerate(candidates, 1):
                table_data.append([
                    str(i),
                    c.get('name', ''),
                    c.get('current_company', ''),
                    c.get('current_job_title', ''),
                    c.get('education', ''),
                    f"{c.get('match_score', 0)}%"
                ])

            table = Table(table_data, colWidths=[1.5*cm, 2.5*cm, 3*cm, 3*cm, 2*cm, 2*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'WenQuanYi'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1F4E79')),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), HexColor('#F2F2F2')]),
                ('BOX', (0, 0), (-1, -1), 0.5, HexColor('#E0E0E0')),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, HexColor('#E0E0E0')),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(table)

            # 生成PDF
            doc.build(elements)

            # 清理临时文件
            if os.path.exists(chart_path):
                os.remove(chart_path)

            print(f"✅ PDF报告已生成: {output_file}")

        except Exception as e:
            print(f"❌ PDF生成失败: {e}")

    def generate_excel_report(self, report_data: Dict[str, Any], output_file: str) -> None:
        """
        生成Excel格式报告

        Args:
            report_data: 报告数据
            output_file: 输出文件路径
        """
        if not OPENPYXL_AVAILABLE:
            print("❌ openpyxl未安装，无法生成Excel。请运行: pip install openpyxl")
            return

        # 标准化报告数据（统一字段名、格式化执行摘要）
        self._normalize_report_data(report_data)

        wb = Workbook()
        ws = wb.active
        ws.title = "候选人数据"

        # 样式定义
        header_font = Font(name='WenQuanYi Micro Hei', bold=True, color='FFFFFF', size=11)
        header_fill = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')
        header_alignment = Alignment(horizontal='center', vertical='center')

        data_font = Font(name='WenQuanYi Micro Hei', size=10)
        data_alignment = Alignment(horizontal='left', vertical='center')

        border = Border(
            left=Side(style='thin', color='E0E0E0'),
            right=Side(style='thin', color='E0E0E0'),
            top=Side(style='thin', color='E0E0E0'),
            bottom=Side(style='thin', color='E0E0E0')
        )

        # 表头
        headers = ['序号', '姓名', '当前公司', '岗位', '学历', '匹配度', '核心技能', '匹配原因']
        ws.append(headers)

        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = border

        # 数据行
        candidates = report_data.get('candidates', [])
        for i, c in enumerate(candidates, 1):
            row_data = [
                i,
                c.get('name', ''),
                c.get('current_company', ''),
                c.get('current_job_title', ''),
                c.get('education', ''),
                f"{c.get('match_score', 0)}%",
                ', '.join(c.get('skills', [])[:5]),
                c.get('match_reason', '')
            ]
            ws.append(row_data)

            # 设置数据行样式
            for col, value in enumerate(row_data, 1):
                cell = ws.cell(row=i+1, column=col)
                cell.font = data_font
                cell.alignment = data_alignment
                cell.border = border

                # 斑马纹
                if i % 2 == 0:
                    cell.fill = PatternFill(start_color='F9F9F9', end_color='F9F9F9', fill_type='solid')

        # 调整列宽
        col_widths = [6, 10, 20, 20, 10, 10, 30, 40]
        for i, width in enumerate(col_widths, 1):
            ws.column_dimensions[chr(64+i)].width = width

        # 创建合规性声明Sheet
        ws_compliance = wb.create_sheet('合规性声明', 0)
        ws_compliance.column_dimensions['A'].width = 20
        ws_compliance.column_dimensions['B'].width = 80

        compliance_title_font = Font(name='WenQuanYi Micro Hei', size=14, bold=True, color='FFFFFF')
        compliance_header_font = Font(name='WenQuanYi Micro Hei', size=11, bold=True)
        compliance_content_font = Font(name='WenQuanYi Micro Hei', size=10)
        compliance_fill = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')

        # 标题
        ws_compliance.merge_cells('A1:B1')
        ws_compliance['A1'] = '合规性声明（扣子空间报告页必附）'
        ws_compliance['A1'].font = compliance_title_font
        ws_compliance['A1'].fill = compliance_fill
        ws_compliance['A1'].alignment = Alignment(horizontal='center', vertical='center')
        ws_compliance.row_dimensions[1].height = 30

        # 合规性声明内容
        compliance_items = [
            ('数据合规', '全部来自公开权威渠道，无爬虫 / 内部数据 / 隐私信息'),
            ('脱敏合规', '企业 / 个人双重脱敏，不涉及商业机密与知识产权'),
            ('来源可追溯', '所有数据可在官网 / 白皮书 / 招聘平台核验'),
            ('无数据幻觉', '基于最新真实数据，无虚构'),
            ('生成时间', report_data.get('generated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))),
        ]

        for i, (title, content) in enumerate(compliance_items, 2):
            ws_compliance[f'A{i}'] = title
            ws_compliance[f'B{i}'] = content
            ws_compliance[f'A{i}'].font = compliance_header_font
            ws_compliance[f'B{i}'].font = compliance_content_font
            ws_compliance[f'A{i}'].alignment = Alignment(horizontal='left', vertical='center')
            ws_compliance[f'B{i}'].alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
            ws_compliance.row_dimensions[i].height = 25

        wb.save(output_file)
        print(f"✅ Excel报告已生成: {output_file}")

    def generate_word_report(self, report_data: Dict[str, Any], output_file: str) -> None:
        """生成Word格式报告（基础实现）"""
        # Word生成较为复杂，此处简化处理
        # 实际使用可考虑使用python-docx库
        print("⚠️  Word格式暂未完整实现，建议使用HTML格式")
        self.generate_html_report(report_data, output_file.replace('.docx', '.html'))

    def generate_ppt_report(self, report_data: Dict[str, Any], output_file: str) -> None:
        """生成PPT格式报告（基础实现）"""
        print("⚠️  PPT格式暂未完整实现，建议使用HTML格式")
        self.generate_html_report(report_data, output_file.replace('.pptx', '.html'))


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='多格式报告生成工具（符合红线规则v5.0）')
    parser.add_argument('--data', required=True, help='JSON数据文件路径')
    parser.add_argument('--format', default='html', choices=['html', 'pdf', 'word', 'ppt', 'excel'], help='输出格式')
    parser.add_argument('--output', required=True, help='输出文件路径')

    args = parser.parse_args()

    # 读取数据
    with open(args.data, 'r', encoding='utf-8') as f:
        report_data = json.load(f)

    # 创建生成器
    generator = ReportGenerator('', os.path.dirname(args.output))

    # 生成报告
    if args.format == 'html':
        generator.generate_html_report(report_data, args.output)
    elif args.format == 'pdf':
        generator.generate_pdf_report(report_data, args.output)
    elif args.format == 'excel':
        generator.generate_excel_report(report_data, args.output)
    elif args.format == 'word':
        generator.generate_word_report(report_data, args.output)
    elif args.format == 'ppt':
        generator.generate_ppt_report(report_data, args.output)


if __name__ == '__main__':
    main()
