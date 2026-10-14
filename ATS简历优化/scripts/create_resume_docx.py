#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Word格式简历和修改说明文档
"""

import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE

# 创建输出目录
os.makedirs('./简历优化', exist_ok=True)

def create_digital_hr_resume():
    """创建数字化HR方向简历"""
    doc = Document()
    
    # 设置默认字体
    style = doc.styles['Normal']
    style.font.name = '微软雅黑'
    style.font.size = Pt(10.5)
    style._element.rPr.rFonts.set('{http://schemas.openxmlformats.org/officeDocument/2006/main}eastAsia', '微软雅黑')
    
    # ===== 个人信息 =====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('贾小小')
    run.bold = True
    run.font.size = Pt(16)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('185****1510  |  jia****@foxmail.com')
    run.font.size = Pt(10)
    
    # ===== 求职意向 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('求职意向')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(102, 126, 234)
    
    p = doc.add_paragraph('数字化人力资源管理  |  HR数字化转型  |  HRIS / HR数据分析')
    p.paragraph_format.left_indent = Inches(0.2)
    
    # ===== 教育背景 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('教育背景')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(102, 126, 234)
    
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2018.03 - 2021.01  ')
    run.bold = True
    p.add_run('华南理工大学').bold = False
    p.add_run('  人力资源管理专业  ')
    run2 = p.add_run('本科')
    run2.italic = True
    
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2006.09 - 2009.06  ')
    run.bold = True
    p.add_run('广东培正学院').bold = False
    p.add_run('  人力资源管理专业  ')
    run2 = p.add_run('专科')
    run2.italic = True
    
    # ===== 专业证书 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('专业证书')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(102, 126, 234)
    
    certs = [
        ('2023年', '中级经济师（人力资源管理师）'),
        ('2020年', '高级人力资源数据分析证书'),
        ('2016年', '企业培训师三级'),
        ('2008年', '大学英语CET-4'),
    ]
    for year, cert in certs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        run = p.add_run(f'{year}  ')
        run.bold = True
        p.add_run(cert)
    
    # ===== 工作经历 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('工作经历')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(102, 126, 234)
    
    # 公司1
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2023.09 - 至今  ')
    run.bold = True
    run.font.size = Pt(11)
    p.add_run('广州智能信息科技有限公司').bold = False
    run2 = p.add_run('  人力资源经理')
    run2.bold = True
    
    items = [
        '制定与公司业务战略对齐的人力资源数字化战略规划，主导人力资源体系从0到1搭建，覆盖招聘系统、薪酬管理、绩效评估等全模块数字化解决方案',
        '协同管理层推进组织架构数字化转型，明确岗位职责，梳理HR业务流程，实施人才评估数字化工具，支撑业务高效运转',
        '搭建智能招聘管理系统，优化招聘流程，招聘周期缩短30%，支撑业务扩张期人才快速供应',
        '统筹薪酬福利体系数字化设计与落地，建立人力成本数据看板，实现成本动态分析与预警',
        '推进HR运营流程自动化，优化入职转正、岗位调动、离职交接等流程，降低用工风险，提升组织运营效率',
        '主导HR数据分析体系建设，开展人力资本分析，为管理层决策提供数据支撑',
    ]
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.4)
        p.add_run(item)
    
    # 公司2
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2016.06 - 2022.03  ')
    run.bold = True
    run.font.size = Pt(11)
    p.add_run('广州奇迹科技有限公司').bold = False
    run2 = p.add_run('  人力资源经理')
    run2.bold = True
    
    items = [
        '主导集团人力资源数字化转型战略规划，推动组织发展与HR系统架构优化，建立权限管理体系',
        '搭建人力资源共享服务中心数字化体系（HRSSC），实现入转调离、薪资核算等90%事务自动化处理，人力服务响应效率提升40%',
        '推进招聘流程数字化改造，通过精细化管理支撑集团业务高速扩张，人员规模年均增长27%，关键岗位招聘满足率95%',
        '设计数字化薪酬绩效管理平台，建立人才激励与保留机制，员工满意度提升至80%',
        '统筹集团全链路人力成本数字化管控，建立成本分析模型，实现年度人力成本精准预算与控制',
        '构建劳动合规数字化预警系统，任职期间实现人事争议零仲裁，合规率100%',
    ]
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.4)
        p.add_run(item)
    
    # 公司3
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2015.07 - 2016.02  ')
    run.bold = True
    run.font.size = Pt(11)
    p.add_run('广州贾教育科技有限公司').bold = False
    run2 = p.add_run('  人力资源经理')
    run2.bold = True
    
    items = [
        '主导人力行政系统数字化搭建，支撑项目团队年度交付率100%',
        '制定人才招聘数字化方案，建立候选人管理系统，新员工转正率提升至90%',
        '搭建在线培训与人才发展体系，优化员工绩效数字化评估，员工工作效率提升20%',
    ]
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.4)
        p.add_run(item)
    
    # 公司4
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2011.08 - 2015.07  ')
    run.bold = True
    run.font.size = Pt(11)
    p.add_run('盛佳集团').bold = False
    run2 = p.add_run('  集团人力主管')
    run2.bold = True
    
    items = [
        '制定集团招聘数字化策略，搭建多元招聘渠道数字化管理，完成14家子公司全业务板块招聘目标，人才引进效率提升30%',
        '建立HR合规数字化风控体系，优化员工异动数字化流程，任职期间实现人事争议零仲裁',
        '搭建人力资源数据分析平台，生成人员结构、流失率等季度分析报告，为集团战略决策提供数据支撑',
    ]
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.4)
        p.add_run(item)
    
    # 公司5
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2009.05 - 2011.06  ')
    run.bold = True
    run.font.size = Pt(11)
    p.add_run('新嘉教育集团（华南地区/上市公司）').bold = False
    run2 = p.add_run('  区域人力资源专员')
    run2.bold = True
    
    items = [
        '独立负责华南区招聘数字化管理，完成业务板块招聘目标',
        '建立薪资核算数字化系统，准确核算千余名员工薪资，个税、劳务税汇缴合规率100%',
        '配合集团完成ERP系统上线及上市筹备HR相关工作',
    ]
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.4)
        p.add_run(item)
    
    # ===== 专业技能 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('专业技能')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(102, 126, 234)
    
    skills = [
        'HR数字化工具：熟悉HRIS/HR SaaS/e-HR系统设计与实施、OKR/KPI绩效系统、招聘管理系统（ATS）、员工自助平台',
        '数据分析能力：熟练使用Excel高级分析、Power BI数据可视化、人力资本分析（HCA）、组织诊断分析',
        'AI应用能力：AI+人力资源建模、智能招聘应用、流程自动化（IPA）、人才画像构建',
        '专业资质：中级经济师（人力资源管理）、高级人力资源数据分析、企业培训师三级',
    ]
    for skill in skills:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.2)
        p.add_run(skill)
    
    # ===== 持续学习 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('持续学习')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(102, 126, 234)
    
    learning = [
        'AI在人力资源九大场景的应用技能（AI Agent/Skill）开发进阶培训',
        '蜜蜂学堂/三茅在线培训（管理/项目/TD/OD等课程）',
    ]
    for item in learning:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.2)
        p.add_run(item)
    
    # 保存文档
    doc.save('./简历优化/贾小小_数字化HR_优化简历.docx')
    print('数字化HR简历已保存')

def create_full_hr_resume():
    """创建全盘HR方向简历"""
    doc = Document()
    
    # 设置默认字体
    style = doc.styles['Normal']
    style.font.name = '微软雅黑'
    style.font.size = Pt(10.5)
    style._element.rPr.rFonts.set('{http://schemas.openxmlformats.org/officeDocument/2006/main}eastAsia', '微软雅黑')
    
    # ===== 个人信息 =====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('贾小小')
    run.bold = True
    run.font.size = Pt(16)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('185****1510  |  jia****@foxmail.com')
    run.font.size = Pt(10)
    
    # ===== 求职意向 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('求职意向')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(245, 87, 108)
    
    p = doc.add_paragraph('人力资源总监  |  全盘HR管理负责人  |  HRM / HRD')
    p.paragraph_format.left_indent = Inches(0.2)
    
    # ===== 教育背景 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('教育背景')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(245, 87, 108)
    
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2018.03 - 2021.01  ')
    run.bold = True
    p.add_run('华南理工大学').bold = False
    p.add_run('  人力资源管理专业  ')
    run2 = p.add_run('本科')
    run2.italic = True
    
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2006.09 - 2009.06  ')
    run.bold = True
    p.add_run('广东培正学院').bold = False
    p.add_run('  人力资源管理专业  ')
    run2 = p.add_run('专科')
    run2.italic = True
    
    # ===== 专业证书 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('专业证书')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(245, 87, 108)
    
    certs = [
        ('2023年', '中级经济师（人力资源管理师）'),
        ('2020年', '高级人力资源数据分析证书'),
        ('2016年', '企业培训师三级'),
        ('2008年', '大学英语CET-4'),
    ]
    for year, cert in certs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        run = p.add_run(f'{year}  ')
        run.bold = True
        p.add_run(cert)
    
    # ===== 工作经历 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('工作经历')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(245, 87, 108)
    
    # 公司1
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2023.09 - 至今  ')
    run.bold = True
    run.font.size = Pt(11)
    p.add_run('广州智能信息科技有限公司').bold = False
    run2 = p.add_run('  人力资源经理')
    run2.bold = True
    
    items = [
        '全面负责人力资源战略规划与体系搭建，主导从0到1构建招聘、薪酬、绩效、人才发展等全模块管理体系，为公司快速发展提供组织保障',
        '协同管理层优化组织架构，明确岗位职责分工，梳理核心业务流程，实施人才评估与激励机制，支撑业务战略落地',
        '统筹招聘体系全流程管理，搭建关键人才库，招聘周期缩短30%，保障业务扩张期人才供应',
        '设计并落地薪酬福利体系，开展人力成本预算与动态分析，建立成本预警机制，实现人力成本可控',
        '独立统筹人力资源与行政管理全流程，降低用工风险，提升组织运营效率',
        '承担总经理HR战略伙伴角色，推动跨部门协作与业务目标达成',
    ]
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.4)
        p.add_run(item)
    
    # 公司2
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2016.06 - 2022.03  ')
    run.bold = True
    run.font.size = Pt(11)
    p.add_run('广州奇迹科技有限公司').bold = False
    run2 = p.add_run('  人力资源经理（汇报对象：集团董事长）')
    run2.bold = True
    
    items = [
        '全面统筹集团人力资源战略规划与组织发展，主导架构优化与权限体系建设，支撑集团多业务板块快速发展',
        '带领5人HR团队，主导人才盘点与梯队建设，建立关键人才供应链，保障人力资源与业务协同发展',
        '设计创新型薪酬绩效体系，建立人才激励保留机制，员工满意度提升至80%',
        '推进HR共享服务中心建设，实现入转调离、薪资核算等事务90%自动化，人力服务效率提升40%',
        '统筹集团总部及十余家分公司全链路人力成本管控，实现年度成本精准管控',
        '构建劳动合规风控体系，任职期间实现人事争议零仲裁，合规率100%',
        '推动集团HR流程标准化与数据化建设，成功申报政府稳岗及人才补贴，支持集团战略决策',
    ]
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.4)
        p.add_run(item)
    
    # 公司3
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2015.07 - 2016.02  ')
    run.bold = True
    run.font.size = Pt(11)
    p.add_run('广州贾教育科技有限公司').bold = False
    run2 = p.add_run('  人力资源经理（下属1人）')
    run2.bold = True
    
    items = [
        '根据公司战略全面负责人力行政体系搭建与运营，支撑项目团队年度交付率100%',
        '制定人才招聘计划，建立人才选拔体系，新员工转正率提升至90%',
        '建立人才发展与培训体系，优化薪酬绩效机制，员工工作效率提升20%',
    ]
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.4)
        p.add_run(item)
    
    # 公司4
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2011.08 - 2015.07  ')
    run.bold = True
    run.font.size = Pt(11)
    p.add_run('盛佳集团').bold = False
    run2 = p.add_run('  集团人力主管（下辖10人）')
    run2.bold = True
    
    items = [
        '制定集团年度招聘策略，完成14家子公司全业务板块招聘目标，人才引进效率提升30%',
        '搭建集团级合规风控体系，优化员工异动流程，实现人事争议零仲裁',
        '协助集团人力经理统筹全局工作，推动HR标准化规范化建设，团队协作效率提升25%',
        '精细化管理员工档案、社保、公积金等事务，保障员工权益合规',
        '主导人力数据分析与战略报告，为集团决策提供关键支撑',
    ]
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.4)
        p.add_run(item)
    
    # 公司5
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('2009.05 - 2011.06  ')
    run.bold = True
    run.font.size = Pt(11)
    p.add_run('新嘉教育集团（华南地区/上市公司）').bold = False
    run2 = p.add_run('  区域人力资源专员')
    run2.bold = True
    
    items = [
        '独立负责华南区全兼职招聘，完成业务板块招聘目标',
        '准确核算千余名员工薪资，个税、劳务税汇缴合规率100%',
        '配合集团ERP系统上线及上市筹备HR工作',
    ]
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.4)
        p.add_run(item)
    
    # ===== 专业技能 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('专业技能')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(245, 87, 108)
    
    skills = [
        '全模块HR管理：招聘配置、培训发展、绩效管理、薪酬福利、员工关系、组织发展、劳动合规',
        '战略规划能力：人力资源战略规划、组织架构设计、人才梯队建设、变革管理',
        '团队管理能力：HR团队组建与领导、跨部门协作、项目统筹、目标达成',
        '数据决策能力：人力资本分析、HR数据分析可视化、成本预算管控',
        '专业资质：中级经济师（人力资源管理）、高级人力资源数据分析、企业培训师三级',
    ]
    for skill in skills:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.2)
        p.add_run(skill)
    
    # ===== 持续学习 =====
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('持续学习')
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(245, 87, 108)
    
    learning = [
        'AI在人力资源九大场景的应用技能（AI Agent/Skill）开发进阶培训',
        '蜜蜂学堂/三茅在线培训（管理/项目/TD/OD等课程）',
    ]
    for item in learning:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.2)
        p.add_run(item)
    
    # 保存文档
    doc.save('./简历优化/贾小小_全盘HR_优化简历.docx')
    print('全盘HR简历已保存')

# 执行
create_digital_hr_resume()
create_full_hr_resume()
print('Word简历生成完成！')
