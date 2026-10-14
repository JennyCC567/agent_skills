#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成交互式模拟面试网页
"""

import os
from datetime import datetime

os.makedirs('./简历优化', exist_ok=True)
current_date = datetime.now().strftime('%Y年%m月%d日')

def create_mock_interview_html(direction, theme_color):
    """创建交互式模拟面试HTML页面"""
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>贾小小 - {direction}模拟面试</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f5f7fa; color: #333; }}
        
        .header {{
            background: linear-gradient(135deg, {theme_color[0]} 0%, {theme_color[1]} 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 0 0 30px 30px;
        }}
        
        .header h1 {{ font-size: 24px; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; font-size: 14px; }}
        
        .container {{ max-width: 900px; margin: 30px auto; padding: 0 20px; }}
        
        .card {{
            background: white;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        
        .question-card {{
            background: white;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-left: 5px solid {theme_color[0]};
        }}
        
        .question-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .question-type {{
            background: {theme_color[0]}20;
            color: {theme_color[0]};
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .question-num {{
            color: #999;
            font-size: 12px;
        }}
        
        .question-text {{
            font-size: 16px;
            line-height: 1.8;
            margin-bottom: 15px;
        }}
        
        .source-tag {{
            color: #666;
            font-size: 12px;
            background: #f5f5f5;
            padding: 3px 8px;
            border-radius: 4px;
        }}
        
        .answer-section {{
            margin-top: 15px;
        }}
        
        .answer-textarea {{
            width: 100%;
            min-height: 120px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            font-size: 14px;
            resize: vertical;
            font-family: inherit;
        }}
        
        .answer-textarea:focus {{
            outline: none;
            border-color: {theme_color[0]};
        }}
        
        .btn-group {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }}
        
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .btn-primary {{
            background: {theme_color[0]};
            color: white;
        }}
        
        .btn-primary:hover {{
            opacity: 0.9;
            transform: translateY(-2px);
        }}
        
        .btn-secondary {{
            background: #f0f0f0;
            color: #666;
        }}
        
        .progress-bar {{
            background: #e0e0e0;
            border-radius: 10px;
            height: 8px;
            margin-bottom: 20px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, {theme_color[0]}, {theme_color[1]});
            border-radius: 10px;
            transition: width 0.3s;
        }}
        
        .progress-text {{
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        
        .tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .tab {{
            padding: 10px 20px;
            border: none;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .tab.active {{
            background: {theme_color[0]};
            color: white;
        }}
        
        .chart-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .chart-card {{
            background: #f9f9f9;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        
        .chart-title {{
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
        }}
        
        .score-display {{
            font-size: 48px;
            font-weight: bold;
            color: {theme_color[0]};
        }}
        
        .score-label {{
            font-size: 12px;
            color: #999;
            margin-top: 5px;
        }}
        
        .tips-card {{
            background: linear-gradient(135deg, {theme_color[0]}10, {theme_color[1]}10);
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid {theme_color[0]};
        }}
        
        .tips-card h4 {{
            color: {theme_color[0]};
            margin-bottom: 10px;
        }}
        
        .tips-card ul {{
            padding-left: 20px;
            color: #666;
        }}
        
        .tips-card li {{
            margin-bottom: 5px;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 12px;
        }}
        
        @media print {{
            .no-print {{ display: none; }}
            .card {{ box-shadow: none; border: 1px solid #ddd; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 模拟面试练习</h1>
        <p>贾小小 - {direction} | 报告生成日期：{current_date}</p>
    </div>
    
    <div class="container">
        <div class="progress-text">面试进度：<span id="progress-text">0/8 题</span></div>
        <div class="progress-bar">
            <div class="progress-fill" id="progress-fill" style="width: 0%"></div>
        </div>
        
        <div class="tabs no-print">
            <button class="tab active" onclick="showTab('questions')">面试题目</button>
            <button class="tab" onclick="showTab('tips')">面试技巧</button>
        </div>
        
        <div id="questions-tab">
            <!-- Question 1 -->
            <div class="question-card" id="q1">
                <div class="question-header">
                    <span class="question-type">自我介绍</span>
                    <span class="question-num">第 1/8 题</span>
                </div>
                <div class="question-text">
                    <strong>请简单介绍一下你自己。</strong>
                </div>
                <span class="source-tag">[来源：简历-个人信息]</span>
                <div class="answer-section">
                    <textarea class="answer-textarea" placeholder="请在此输入你的回答..."></textarea>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="markComplete('q1')">标记已完成</button>
                    </div>
                </div>
            </div>
            
            <!-- Question 2 -->
            <div class="question-card" id="q2">
                <div class="question-header">
                    <span class="question-type">简历深挖</span>
                    <span class="question-num">第 2/8 题</span>
                </div>
                <div class="question-text">
                    <strong>在广州奇迹科技期间，你主导的HRSSC数字化体系具体是如何搭建的？实现了哪些成果？</strong>
                </div>
                <span class="source-tag">[来源：简历-工作经历2]</span>
                <div class="answer-section">
                    <textarea class="answer-textarea" placeholder="请在此输入你的回答..."></textarea>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="markComplete('q2')">标记已完成</button>
                    </div>
                </div>
            </div>
            
            <!-- Question 3 -->
            <div class="question-card" id="q3">
                <div class="question-header">
                    <span class="question-type">简历深挖</span>
                    <span class="question-num">第 3/8 题</span>
                </div>
                <div class="question-text">
                    <strong>你提到招聘周期缩短30%，请问具体是怎么做到的？</strong>
                </div>
                <span class="source-tag">[来源：简历-工作经历1]</span>
                <div class="answer-section">
                    <textarea class="answer-textarea" placeholder="请在此输入你的回答..."></textarea>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="markComplete('q3')">标记已完成</button>
                    </div>
                </div>
            </div>
            
            <!-- Question 4 -->
            <div class="question-card" id="q4">
                <div class="question-header">
                    <span class="question-type">专业问题</span>
                    <span class="question-num">第 4/8 题</span>
                </div>
                <div class="question-text">
                    <strong>{"你如何理解HR数字化转型的核心要义？" if "数字化HR" in direction else "你如何设计一套有效的薪酬绩效体系？"}</strong>
                </div>
                <span class="source-tag">[来源：简历-专业能力]</span>
                <div class="answer-section">
                    <textarea class="answer-textarea" placeholder="请在此输入你的回答..."></textarea>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="markComplete('q4')">标记已完成</button>
                    </div>
                </div>
            </div>
            
            <!-- Question 5 -->
            <div class="question-card" id="q5">
                <div class="question-header">
                    <span class="question-type">专业问题</span>
                    <span class="question-num">第 5/8 题</span>
                </div>
                <div class="question-text">
                    <strong>{"如果让你主导一家中型企业的HR数字化转型，你会如何规划？" if "数字化HR" in direction else "你是如何平衡业务扩张与人力成本控制的？"}</strong>
                </div>
                <span class="source-tag">[来源：简历-工作经历]</span>
                <div class="answer-section">
                    <textarea class="answer-textarea" placeholder="请在此输入你的回答..."></textarea>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="markComplete('q5')">标记已完成</button>
                    </div>
                </div>
            </div>
            
            <!-- Question 6 -->
            <div class="question-card" id="q6">
                <div class="question-header">
                    <span class="question-type">行为面试</span>
                    <span class="question-num">第 6/8 题</span>
                </div>
                <div class="question-text">
                    <strong>请举例说明你如何处理与业务部门的冲突。</strong>
                </div>
                <span class="source-tag">[来源：简历-工作经历]</span>
                <div class="answer-section">
                    <textarea class="answer-textarea" placeholder="请在此输入你的回答..."></textarea>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="markComplete('q6')">标记已完成</button>
                    </div>
                </div>
            </div>
            
            <!-- Question 7 -->
            <div class="question-card" id="q7">
                <div class="question-header">
                    <span class="question-type">行为面试</span>
                    <span class="question-num">第 7/8 题</span>
                </div>
                <div class="question-text">
                    <strong>描述一次你主动承担额外责任并取得成果的经历。</strong>
                </div>
                <span class="source-tag">[来源：简历-工作经历]</span>
                <div class="answer-section">
                    <textarea class="answer-textarea" placeholder="请在此输入你的回答..."></textarea>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="markComplete('q7')">标记已完成</button>
                    </div>
                </div>
            </div>
            
            <!-- Question 8 -->
            <div class="question-card" id="q8">
                <div class="question-header">
                    <span class="question-type">反向提问</span>
                    <span class="question-num">第 8/8 题</span>
                </div>
                <div class="question-text">
                    <strong>你有什么问题想要问我的吗？</strong>
                </div>
                <span class="source-tag">[面试常规问题]</span>
                <div class="answer-section">
                    <textarea class="answer-textarea" placeholder="请在此输入你的回答..."></textarea>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="markComplete('q8')">标记已完成</button>
                    </div>
                </div>
            </div>
        </div>
        
        <div id="tips-tab" style="display:none;">
            <div class="card">
                <h3 style="color:{theme_color[0]};margin-bottom:20px;">📋 面试准备技巧</h3>
                
                <div class="tips-card" style="margin-bottom:20px;">
                    <h4>🎯 回答技巧（STAR法则）</h4>
                    <ul>
                        <li><strong>Situation（情境）：</strong>描述背景和具体情况</li>
                        <li><strong>Task（任务）：</strong>说明你需要完成的任务</li>
                        <li><strong>Action（行动）：</strong>详细描述你采取的具体行动</li>
                        <li><strong>Result（结果）：</strong>量化你的成果和影响</li>
                    </ul>
                </div>
                
                <div class="tips-card" style="margin-bottom:20px;">
                    <h4>💡 注意事项</h4>
                    <ul>
                        <li>回答时引用简历中的具体数据和案例</li>
                        <li>突出你在项目中的具体贡献和角色</li>
                        <li>用量化数据增强说服力</li>
                        <li>保持回答结构清晰、逻辑性强</li>
                    </ul>
                </div>
                
                <div class="tips-card">
                    <h4>⚠️ 常见错误避免</h4>
                    <ul>
                        <li>避免回答过于笼统或抽象</li>
                        <li>不要虚构或夸大经历</li>
                        <li>不要将团队成果完全归于自己</li>
                        <li>避免负面评价前雇主或同事</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="card no-print" style="margin-top:30px;">
            <h3 style="color:{theme_color[0]};margin-bottom:20px;">📊 面试自评</h3>
            <div class="chart-container">
                <div class="chart-card">
                    <div class="chart-title">回答相关性</div>
                    <div class="score-display">--</div>
                    <div class="score-label">是否切中问题核心</div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">内容完整性</div>
                    <div class="score-display">--</div>
                    <div class="score-label">是否有STAR结构</div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">逻辑清晰度</div>
                    <div class="score-display">--</div>
                    <div class="score-label">表达是否条理清晰</div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">具体性</div>
                    <div class="score-display">--</div>
                    <div class="score-label">是否有具体案例</div>
                </div>
            </div>
            <p style="text-align:center;color:#999;margin-top:20px;font-size:12px;">
                完成所有问题后，可自行对照评分标准进行评估
            </p>
        </div>
    </div>
    
    <div class="footer">
        <p>贾小小 - {direction}面试准备 | 生成日期：{current_date}</p>
        <p style="margin-top:10px;">
            <button onclick="window.print()" class="btn btn-secondary" style="margin-right:10px;">打印/导出PDF</button>
        </p>
    </div>
    
    <script>
        let completedQuestions = 0;
        const totalQuestions = 8;
        
        function markComplete(questionId) {{
            const card = document.getElementById(questionId);
            if (!card.classList.contains('completed')) {{
                card.classList.add('completed');
                card.style.opacity = '0.7';
                card.style.borderLeftColor = '#10b981';
                completedQuestions++;
                updateProgress();
            }}
        }}
        
        function updateProgress() {{
            const percentage = (completedQuestions / totalQuestions) * 100;
            document.getElementById('progress-fill').style.width = percentage + '%';
            document.getElementById('progress-text').textContent = completedQuestions + '/' + totalQuestions + ' 题';
        }}
        
        function showTab(tabName) {{
            document.getElementById('questions-tab').style.display = tabName === 'questions' ? 'block' : 'none';
            document.getElementById('tips-tab').style.display = tabName === 'tips' ? 'block' : 'none';
            
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>'''
    
    return html_content

# 生成数字化HR模拟面试页面
digital_hr_html = create_mock_interview_html('数字化HR', ('#667eea', '#764ba2'))
with open('./简历优化/贾小小_数字化HR_模拟面试.html', 'w', encoding='utf-8') as f:
    f.write(digital_hr_html)
print('数字化HR模拟面试页面已保存')

# 生成全盘HR模拟面试页面
full_hr_html = create_mock_interview_html('全盘HR', ('#f5576c', '#f093fb'))
with open('./简历优化/贾小小_全盘HR_模拟面试.html', 'w', encoding='utf-8') as f:
    f.write(full_hr_html)
print('全盘HR模拟面试页面已保存')

print('所有交互式模拟面试页面生成完成！')
