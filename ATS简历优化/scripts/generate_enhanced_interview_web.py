#!/usr/bin/env python3
"""
增强版交互式面试模拟页面生成脚本 v2

核心改进：
1. 卡片渲染改用直接DOM写入，避免翻转动画导致的内容空白
2. 答案区默认折叠，点击按钮展开，交互更直观
3. 新增自评评分功能 + 复习模式（一键展开全部答案）
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


def generate_enhanced_interview_html(questions_list, job_name="目标岗位", company_name="目标公司"):
    """
    生成增强版交互式面试模拟页面
    
    Args:
        questions_list: 面试题目列表
        job_name: 岗位名称
        company_name: 公司名称
    
    Returns:
        HTML字符串
    """
    
    if not questions_list:
        questions_list = []
    
    # 将题目列表转换为JSON
    questions_json = json.dumps(questions_list, ensure_ascii=False, indent=2)
    
    # 获取当前时间
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%H:%M:%S')
    current_datetime = now.strftime('%Y年%m月%d日 %H:%M')
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{job_name} - 交互式面试模拟 v2</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: "Microsoft YaHei", "微软雅黑", "SimSun", "宋体", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .header .info {{
            margin-top: 15px;
            font-size: 14px;
            opacity: 0.8;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        /* 控制按钮区 */
        .control-panel {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
        }}
        
        .control-btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .control-btn.primary {{
            background: #667eea;
            color: white;
        }}
        
        .control-btn.primary:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}
        
        .control-btn.secondary {{
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }}
        
        .control-btn.secondary:hover {{
            background: #667eea;
            color: white;
        }}
        
        .control-btn.success {{
            background: #28a745;
            color: white;
        }}
        
        .control-btn.success:hover {{
            background: #218838;
        }}
        
        /* 统计面板 */
        .stats-panel {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
        .stat-card {{
            flex: 1;
            min-width: 150px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }}
        
        .stat-card .stat-value {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-card .stat-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        /* 题目卡片 */
        .question-card {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }}
        
        .question-card:hover {{
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }}
        
        .question-card.completed {{
            border-color: #28a745;
            background: #f0fff4;
        }}
        
        .question-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        
        .question-type {{
            display: inline-block;
            padding: 4px 12px;
            background: #667eea;
            color: white;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
        }}
        
        .question-number {{
            color: #999;
            font-size: 14px;
        }}
        
        .question-title {{
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
            line-height: 1.5;
        }}
        
        .question-source {{
            font-size: 13px;
            color: #667eea;
            margin-bottom: 15px;
            padding: 8px 12px;
            background: #e8f0fe;
            border-radius: 6px;
        }}
        
        /* 答案区 */
        .answer-section {{
            margin-top: 20px;
            display: none;
        }}
        
        .answer-section.show {{
            display: block;
        }}
        
        .answer-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }}
        
        .answer-item h4 {{
            color: #667eea;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        
        .answer-item p {{
            color: #555;
            font-size: 14px;
            line-height: 1.6;
        }}
        
        /* 自评评分 */
        .rating-section {{
            margin-top: 20px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            display: none;
        }}
        
        .rating-section.show {{
            display: block;
        }}
        
        .rating-title {{
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .rating-stars {{
            display: flex;
            gap: 8px;
        }}
        
        .star-btn {{
            width: 36px;
            height: 36px;
            border: none;
            background: #e0e0e0;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            transition: all 0.2s ease;
        }}
        
        .star-btn.active {{
            background: #ffc107;
            color: white;
        }}
        
        .star-btn:hover {{
            transform: scale(1.1);
        }}
        
        /* 按钮组 */
        .btn-group {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .btn-primary {{
            background: #667eea;
            color: white;
        }}
        
        .btn-primary:hover {{
            background: #5568d3;
        }}
        
        .btn-secondary {{
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }}
        
        .btn-secondary:hover {{
            background: #667eea;
            color: white;
        }}
        
        .btn-success {{
            background: #28a745;
            color: white;
        }}
        
        .btn-success:hover {{
            background: #218838;
        }}
        
        /* 进度条 */
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 20px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }}
        
        /* 响应式 */
        @media (max-width: 768px) {{
            .content {{
                padding: 20px;
            }}
            
            .control-panel {{
                flex-direction: column;
            }}
            
            .stats-panel {{
                flex-direction: column;
            }}
            
            .question-header {{
                flex-direction: column;
                gap: 10px;
            }}
        }}
        
        /* 打印样式 */
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
            
            .control-panel, .btn-group {{
                display: none;
            }}
            
            .answer-section {{
                display: block !important;
            }}
            
            .rating-section {{
                display: none !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>交互式面试模拟 v2</h1>
            <p>{job_name} - {company_name}</p>
            <div class="info">生成时间：{current_datetime} | 共 {len(questions_list)} 道面试题</div>
        </div>
        
        <div class="content">
            <!-- 控制按钮区 -->
            <div class="control-panel">
                <button class="control-btn primary" onclick="expandAllAnswers()">
                    <span>📖</span> 复习模式（展开全部答案）
                </button>
                <button class="control-btn secondary" onclick="collapseAllAnswers()">
                    <span>📕</span> 折叠全部答案
                </button>
                <button class="control-btn success" onclick="exportProgress()">
                    <span>💾</span> 导出练习进度
                </button>
            </div>
            
            <!-- 统计面板 -->
            <div class="stats-panel">
                <div class="stat-card">
                    <div class="stat-value" id="totalQuestions">{len(questions_list)}</div>
                    <div class="stat-label">总题数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="completedCount">0</div>
                    <div class="stat-label">已完成</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="avgRating">0.0</div>
                    <div class="stat-label">平均评分</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="progressPercent">0%</div>
                    <div class="stat-label">完成进度</div>
                </div>
            </div>
            
            <!-- 进度条 -->
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill" style="width: 0%;"></div>
            </div>
            
            <!-- 题目容器 -->
            <div id="questionsContainer"></div>
        </div>
    </div>
    
    <script>
        // 题目数据
        const questionsData = {questions_json};
        
        // 练习状态
        let practiceState = {{
            completed: [],
            ratings: {{}},
            expanded: {{}}
        }};
        
        // 初始化
        function init() {{
            renderQuestions();
            updateStats();
            loadState();
        }}
        
        // 渲染题目卡片
        function renderQuestions() {{
            const container = document.getElementById('questionsContainer');
            container.innerHTML = '';
            
            questionsData.forEach((q, index) => {{
                const card = document.createElement('div');
                card.className = 'question-card';
                card.id = `question-${{index}}`;
                
                // 直接写入DOM内容，避免翻转动画导致的内容空白
                card.innerHTML = `
                    <div class="question-header">
                        <span class="question-type">${{q.type || '其他'}}</span>
                        <span class="question-number">第 ${{index + 1}} 题</span>
                    </div>
                    <div class="question-title">${{q.question || ''}}</div>
                    <div class="question-source">📌 来源：${{q.source || '综合'}}</div>
                    
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="toggleAnswer(${{index}})">
                            <span id="btn-text-${{index}}">💡 查看答案</span>
                        </button>
                        <button class="btn btn-secondary" onclick="toggleRating(${{index}})">
                            ⭐ 自评评分
                        </button>
                        <button class="btn btn-success" onclick="markCompleted(${{index}})">
                            ✓ 标记完成
                        </button>
                    </div>
                    
                    <div class="answer-section" id="answer-${{index}}">
                        <div class="answer-item">
                            <h4>答题思路</h4>
                            <p>${{q['思路'] || q.thought || '暂无'}}</p>
                        </div>
                        <div class="answer-item">
                            <h4>参考答案要点</h4>
                            <p>${{q['要点'] || q.key_points || '暂无'}}</p>
                        </div>
                    </div>
                    
                    <div class="rating-section" id="rating-${{index}}">
                        <div class="rating-title">请根据您的回答质量进行自评（1-5星）：</div>
                        <div class="rating-stars">
                            ${{[1,2,3,4,5].map(star => `
                                <button class="star-btn" onclick="setRating(${{index}}, ${{star}})" id="star-${{index}}-${{star}}">
                                    ${{star}}
                                </button>
                            `).join('')}}
                        </div>
                    </div>
                `;
                
                container.appendChild(card);
            }});
        }}
        
        // 切换答案显示
        function toggleAnswer(index) {{
            const answerSection = document.getElementById(`answer-${{index}}`);
            const btnText = document.getElementById(`btn-text-${{index}}`);
            
            if (answerSection.classList.contains('show')) {{
                answerSection.classList.remove('show');
                btnText.textContent = '💡 查看答案';
                practiceState.expanded[index] = false;
            }} else {{
                answerSection.classList.add('show');
                btnText.textContent = '🙈 隐藏答案';
                practiceState.expanded[index] = true;
            }}
            
            saveState();
        }}
        
        // 切换评分区显示
        function toggleRating(index) {{
            const ratingSection = document.getElementById(`rating-${{index}}`);
            ratingSection.classList.toggle('show');
        }}
        
        // 设置评分
        function setRating(index, rating) {{
            practiceState.ratings[index] = rating;
            
            // 更新星星样式
            for (let i = 1; i <= 5; i++) {{
                const star = document.getElementById(`star-${{index}}-${{i}}`);
                if (i <= rating) {{
                    star.classList.add('active');
                }} else {{
                    star.classList.remove('active');
                }}
            }}
            
            updateStats();
            saveState();
        }}
        
        // 标记完成
        function markCompleted(index) {{
            if (!practiceState.completed.includes(index)) {{
                practiceState.completed.push(index);
            }}
            
            const card = document.getElementById(`question-${{index}}`);
            card.classList.add('completed');
            
            updateStats();
            saveState();
        }}
        
        // 展开全部答案（复习模式）
        function expandAllAnswers() {{
            questionsData.forEach((q, index) => {{
                const answerSection = document.getElementById(`answer-${{index}}`);
                const btnText = document.getElementById(`btn-text-${{index}}`);
                answerSection.classList.add('show');
                btnText.textContent = '🙈 隐藏答案';
                practiceState.expanded[index] = true;
            }});
            saveState();
        }}
        
        // 折叠全部答案
        function collapseAllAnswers() {{
            questionsData.forEach((q, index) => {{
                const answerSection = document.getElementById(`answer-${{index}}`);
                const btnText = document.getElementById(`btn-text-${{index}}`);
                answerSection.classList.remove('show');
                btnText.textContent = '💡 查看答案';
                practiceState.expanded[index] = false;
            }});
            saveState();
        }}
        
        // 更新统计信息
        function updateStats() {{
            const total = questionsData.length;
            const completed = practiceState.completed.length;
            const ratings = Object.values(practiceState.ratings);
            const avgRating = ratings.length > 0 
                ? (ratings.reduce((a, b) => a + b, 0) / ratings.length).toFixed(1)
                : '0.0';
            const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
            
            document.getElementById('totalQuestions').textContent = total;
            document.getElementById('completedCount').textContent = completed;
            document.getElementById('avgRating').textContent = avgRating;
            document.getElementById('progressPercent').textContent = progress + '%';
            document.getElementById('progressFill').style.width = progress + '%';
        }}
        
        // 导出练习进度
        function exportProgress() {{
            const report = {{
                exportTime: new Date().toLocaleString('zh-CN'),
                totalQuestions: questionsData.length,
                completedCount: practiceState.completed.length,
                progress: Math.round((practiceState.completed.length / questionsData.length) * 100) + '%',
                ratings: practiceState.ratings,
                averageRating: Object.values(practiceState.ratings).length > 0
                    ? (Object.values(practiceState.ratings).reduce((a, b) => a + b, 0) / Object.values(practiceState.ratings).length).toFixed(1)
                    : 'N/A',
                details: questionsData.map((q, index) => ({{
                    question: q.question,
                    type: q.type,
                    completed: practiceState.completed.includes(index),
                    rating: practiceState.ratings[index] || '未评分'
                }}))
            }};
            
            const blob = new Blob([JSON.stringify(report, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `面试练习进度_${{new Date().toISOString().slice(0,10)}}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }}
        
        // 保存状态到localStorage
        function saveState() {{
            localStorage.setItem('interviewPracticeState', JSON.stringify(practiceState));
        }}
        
        // 从localStorage加载状态
        function loadState() {{
            const saved = localStorage.getItem('interviewPracticeState');
            if (saved) {{
                try {{
                    practiceState = JSON.parse(saved);
                    
                    // 恢复完成状态
                    practiceState.completed.forEach(index => {{
                        const card = document.getElementById(`question-${{index}}`);
                        if (card) card.classList.add('completed');
                    }});
                    
                    // 恢复评分状态
                    Object.entries(practiceState.ratings).forEach(([index, rating]) => {{
                        for (let i = 1; i <= rating; i++) {{
                            const star = document.getElementById(`star-${{index}}-${{i}}`);
                            if (star) star.classList.add('active');
                        }}
                    }});
                    
                    updateStats();
                }} catch (e) {{
                    console.error('Failed to load state:', e);
                }}
            }}
        }}
        
        // 页面加载完成后初始化
        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>'''
    
    return html_content


def main():
    parser = argparse.ArgumentParser(description='生成增强版交互式面试模拟页面 v2')
    parser.add_argument('--questions-file', required=True, help='面试题目JSON文件路径')
    parser.add_argument('--job-name', default='目标岗位', help='岗位名称')
    parser.add_argument('--company-name', default='目标公司', help='公司名称')
    parser.add_argument('--output', required=True, help='输出HTML文件路径')
    
    args = parser.parse_args()
    
    # 读取题目数据
    with open(args.questions_file, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    # 生成HTML
    html_content = generate_enhanced_interview_html(
        questions_data,
        args.job_name,
        args.company_name
    )
    
    # 写入文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8-sig') as f:
        f.write(html_content)
    
    print(f'✅ 增强版交互式面试模拟页面已生成：{output_path}')
    print(f'📊 题目总数：{len(questions_data)}')
    print(f'🎯 核心改进：')
    print(f'   - 卡片渲染改用直接DOM写入，避免翻转动画导致的内容空白')
    print(f'   - 答案区默认折叠，点击按钮展开，交互更直观')
    print(f'   - 新增自评评分功能 + 复习模式（一键展开全部答案）')


if __name__ == '__main__':
    main()
