#!/usr/bin/env python3
"""
完整诊断问卷生成器
动态生成 HTML 格式的 7S 模型和杨三角诊断问卷
支持在线填写、自动评分、生成诊断报告和雷达图
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
    
    # 读取ECharts库
    echarts_path = assets_dir / "echarts.min.js"
    if echarts_path.exists():
        with open(echarts_path, 'r', encoding='utf-8') as f:
            js_embed += f.read() + "\n"
    
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
        "questionnaire_type": "7s",  # 或 "yang_triangle"
        "company_name": "XX公司",
        "title": "组织健康度诊断问卷",
        "questions": [
            {
                "dimension": "战略",
                "question": "公司是否有清晰的战略规划？",
                "options": ["完全不符合", "不符合", "一般", "符合", "完全符合"]
            }
        ],
        "dimensions": ["战略", "结构", "制度", "风格", "人员", "技能", "共享价值观"],
        "output_path": "./diagnostic_questionnaire.html"
    }

    验证规则:
    - questionnaire_type 必须是 "7s" 或 "yang_triangle"
    - company_name 不能为空
    - questions 必须至少包含 1 题
    - output_path 必须以 .html 结尾
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 检查必需字段
    if 'questionnaire_type' not in data:
        data['questionnaire_type'] = "7s"

    q_type = data['questionnaire_type'].lower()
    if q_type not in ['7s', 'yang_triangle']:
        raise ValueError("questionnaire_type 必须是 '7s' 或 'yang_triangle'")

    if 'company_name' not in data or not data['company_name']:
        raise ValueError("缺少必需字段: company_name 或company_name为空")

    if 'title' not in data:
        data['title'] = "组织健康度诊断问卷"

    if 'questions' not in data or not isinstance(data['questions'], list):
        raise ValueError("缺少必需字段: questions 或questions格式错误")

    if len(data['questions']) == 0:
        raise ValueError("questions 必须至少包含 1 题")

    # 设置默认维度（7S模型）
    if 'dimensions' not in data:
        data['dimensions'] = ["战略", "结构", "制度", "风格", "人员", "技能", "共享价值观"]

    # 设置默认output_path
    if 'output_path' not in data:
        data['output_path'] = "./diagnostic_questionnaire.html"
    else:
        if not data['output_path'].endswith('.html'):
            raise ValueError("output_path 必须以 .html 结尾")

    return data


def generate_questionnaire(data):
    """
    生成诊断问卷 HTML（支持在线填写和报告生成）

    参数:
        data: 包含问卷类型、题目等信息的字典

    返回:
        str: 生成的 HTML 文件路径
    """
    q_type = data['questionnaire_type']
    company_name = data['company_name']
    title = data['title']
    questions = data['questions']
    dimensions = data['dimensions']
    output_path = Path(data['output_path'])

    # 获取内嵌的JS库，确保HTML完全离线可用
    embedded_js = get_embedded_js()

    # 生成题目HTML（添加data-dimension属性）
    questions_html = ""
    for idx, q in enumerate(questions):
        dimension = q.get('dimension', '')
        question_text = q.get('question', '')
        options = q.get('options', ['完全不符合', '不符合', '一般', '符合', '完全符合'])

        questions_html += f"""
        <div class="question-item" data-dimension="{dimension}">
            <div class="question-header">
                <span class="question-number">Q{idx + 1}</span>
                <span class="question-dimension">{dimension}</span>
            </div>
            <div class="question-text">{question_text}</div>
            <div class="question-options">
        """

        for opt_idx, option in enumerate(options):
            questions_html += f"""
                <label class="option-item">
                    <input type="radio" name="q{idx}" value="{opt_idx + 1}" required data-question="{idx}" data-dimension="{dimension}">
                    <span class="option-text">{option}</span>
                </label>
            """

        questions_html += """
            </div>
        </div>
        """

    # HTML模板（包含完整的提交、评分和报告生成逻辑）
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
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        .header .subtitle {{
            font-size: 14px;
            opacity: 0.8;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .question-item {{
            margin-bottom: 35px;
            padding-bottom: 25px;
            border-bottom: 2px solid #f1f5f9;
        }}
        .question-item:last-child {{
            border-bottom: none;
        }}
        .question-header {{
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }}
        .question-number {{
            background: #3b82f6;
            color: white;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            margin-right: 12px;
        }}
        .question-dimension {{
            background: #e0e7ff;
            color: #4f46e5;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }}
        .question-text {{
            font-size: 16px;
            color: #1e293b;
            line-height: 1.6;
            margin-bottom: 16px;
            font-weight: 500;
        }}
        .question-options {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .option-item {{
            display: flex;
            align-items: center;
            padding: 12px 16px;
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .option-item:hover {{
            background: #e0e7ff;
            border-color: #3b82f6;
        }}
        .option-item input[type="radio"] {{
            width: 20px;
            height: 20px;
            margin-right: 12px;
            accent-color: #3b82f6;
        }}
        .option-text {{
            font-size: 14px;
            color: #475569;
        }}
        .submit-btn {{
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .submit-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
        }}
        .submit-btn:disabled {{
            background: #94a3b8;
            cursor: not-allowed;
            transform: none;
        }}
        .footer {{
            background: #f8fafc;
            padding: 20px;
            text-align: center;
            color: #64748b;
            font-size: 13px;
        }}

        /* 报告页面样式 */
        .report-container {{
            display: none;
        }}
        .report-container.active {{
            display: block;
        }}
        .questionnaire-container {{
            display: block;
        }}
        .questionnaire-container.hidden {{
            display: none;
        }}
        .score-summary {{
            background: #f0f9ff;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 24px;
            border-left: 4px solid #3b82f6;
        }}
        .score-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }}
        .score-item {{
            text-align: center;
            padding: 16px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .score-dimension {{
            font-size: 14px;
            color: #64748b;
            margin-bottom: 8px;
        }}
        .score-value {{
            font-size: 28px;
            font-weight: 700;
            color: #3b82f6;
        }}
        .radar-chart-container {{
            width: 100%;
            min-height: 400px;
            background: #ffffff;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            margin: 24px 0;
        }}
        #radarChart {{
            width: 100%;
            height: 400px;
            min-height: 400px;
        }}
        .analysis-section {{
            margin-top: 24px;
            padding: 20px;
            background: #f8fafc;
            border-radius: 12px;
        }}
        .analysis-item {{
            padding: 16px;
            margin-bottom: 12px;
            border-radius: 8px;
            border-left: 4px solid;
        }}
        .analysis-item.high {{
            background: #f0fdf4;
            border-color: #22c55e;
        }}
        .analysis-item.medium {{
            background: #fef9c3;
            border-color: #eab308;
        }}
        .analysis-item.low {{
            background: #fef2f2;
            border-color: #ef4444;
        }}
        .back-btn {{
            padding: 12px 24px;
            background: #64748b;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 20px;
            font-size: 14px;
            font-weight: 600;
        }}
        .back-btn:hover {{
            background: #475569;
        }}
        .action-bar {{
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 24px;
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
        #radarChart {{
            width: 100%;
            height: 400px;
            margin: 24px 0;
        }}
        @media print {{
            body {{ background: white; }}
            .submit-btn, .back-btn, .action-btn {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 问卷表单 -->
        <div id="questionnaireContainer" class="questionnaire-container">
            <div class="header">
                <h1>{title}</h1>
                <div class="subtitle">{company_name} | {q_type.upper()} 模型诊断</div>
            </div>

            <div class="content">
                <form id="questionnaireForm">
                    {questions_html}

                    <button type="submit" class="submit-btn" id="submitBtn">提交问卷并生成诊断报告</button>
                </form>
            </div>

            <div class="footer">
                本问卷由 OD 组织发展助手 生成 | 填写后将自动生成诊断报告
            </div>
        </div>

        <!-- 诊断报告 -->
        <div id="reportContainer" class="report-container">
            <div class="header">
                <h1>诊断报告</h1>
                <div class="subtitle">{company_name} | {q_type.upper()} 模型诊断结果</div>
            </div>

            <div class="content">
                <button class="back-btn" onclick="showQuestionnaire()">← 返回问卷</button>

                <div class="score-summary">
                    <h3>📊 各维度得分汇总</h3>
                    <div class="score-grid" id="scoreGrid"></div>
                </div>

                <div class="radar-chart-container">
                    <h3>📈 能力雷达图</h3>
                    <div id="radarChart"></div>
                </div>

                <div class="analysis-section">
                    <h3>🔍 诊断分析</h3>
                    <div id="analysisContent"></div>
                </div>

                <div class="analysis-section">
                    <h3>💡 改进建议</h3>
                    <div id="recommendations"></div>
                </div>

                <div style="margin-top: 32px; padding: 20px; background: #f0f9ff; border-left: 4px solid #3b82f6; border-radius: 8px;">
                    <h4 style="color: #3b82f6; margin-bottom: 12px;">免责申明</h4>
                    <p style="color: #475569; font-size: 14px; line-height: 1.8;">
                        本工具由AI基于专业理论、行业实践、公开政府文件、权威机构白皮书及行业报告生成。所有生成报告、分析及建议均基于您提供的数据得出，仅供参考，不构成正式管理咨询、法律意见或商业决策依据，任何决策及后果由您自行承担。
                    </p>
                </div>
            </div>

            <div class="footer">
                本报告由 OD 组织发展助手 生成
            </div>

            <div class="action-bar" style="display: none;" id="actionBar">
                <button class="action-btn" onclick="downloadHTML()">🌐 下载 HTML</button>
                <button class="action-btn" onclick="downloadPDF()">📄 下载 PDF</button>
            </div>
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

        // 维度定义
        const dimensions = {json.dumps(dimensions)};

        // 提交表单并生成报告
        document.getElementById('questionnaireForm').addEventListener('submit', function(e) {{
            e.preventDefault();

            // 禁用提交按钮
            const submitBtn = document.getElementById('submitBtn');
            submitBtn.disabled = true;
            submitBtn.textContent = '正在分析...';

            // 收集答案
            const answers = {{}};
            const dimensionScores = {{}};

            dimensions.forEach(dim => {{
                dimensionScores[dim] = {{ scores: [], count: 0 }};
            }});

            // 遍历所有题目
            const form = this;
            const inputs = form.querySelectorAll('input[type="radio"]:checked');

            if (inputs.length === 0) {{
                alert('请回答所有问题后再提交！');
                submitBtn.disabled = false;
                submitBtn.textContent = '提交问卷并生成诊断报告';
                return;
            }}

            inputs.forEach(input => {{
                const questionIndex = input.getAttribute('data-question');
                const dimension = input.getAttribute('data-dimension');
                const value = parseInt(input.value);

                answers[questionIndex] = {{
                    dimension: dimension,
                    value: value
                }};

                if (dimensionScores[dimension]) {{
                    dimensionScores[dimension].scores.push(value);
                    dimensionScores[dimension].count++;
                }}
            }});

            // 计算各维度平均分
            const finalScores = {{}};
            dimensions.forEach(dim => {{
                const scores = dimensionScores[dim].scores;
                if (scores.length > 0) {{
                    const sum = scores.reduce((a, b) => a + b, 0);
                    finalScores[dim] = (sum / scores.length * 2).toFixed(1); // 转换为10分制
                }} else {{
                    finalScores[dim] = 0;
                }}
            }});

            // 延迟以显示加载效果
            setTimeout(() => {{
                generateReport(finalScores);
                showReport();
                submitBtn.disabled = false;
                submitBtn.textContent = '提交问卷并生成诊断报告';
            }}, 1000);
        }});

        // 生成报告
        function generateReport(scores) {{
            // 生成得分汇总
            const scoreGrid = document.getElementById('scoreGrid');
            scoreGrid.innerHTML = '';

            dimensions.forEach(dim => {{
                const score = scores[dim];
                const scoreItem = document.createElement('div');
                scoreItem.className = 'score-item';
                scoreItem.innerHTML = `
                    <div class="score-dimension">${{dim}}</div>
                    <div class="score-value">${{score}}</div>
                `;
                scoreGrid.appendChild(scoreItem);
            }});

            // 生成雷达图
            generateRadarChart(scores);

            // 生成分析内容
            generateAnalysis(scores);

            // 生成改进建议
            generateRecommendations(scores);
        }}

        // 生成雷达图
        function generateRadarChart(scores) {{
            const chartDom = document.getElementById('radarChart');
            
            // 获取容器实际大小
            const containerWidth = chartDom.parentElement.clientWidth - 40; // 减去padding
            const containerHeight = 400;
            
            // 设置div的固定尺寸
            chartDom.style.width = containerWidth + 'px';
            chartDom.style.height = containerHeight + 'px';
            
            const myChart = echarts.init(chartDom);

            const scoreValues = dimensions.map(dim => parseFloat(scores[dim]));

            const option = {{
                backgroundColor: 'transparent',
                radar: {{
                    indicator: dimensions.map(dim => ({{ name: dim, max: 10 }})),
                    shape: 'circle',
                    center: ['50%', '50%'],
                    radius: '75%',
                    axisName: {{
                        color: '#475569',
                        fontSize: 14,
                        fontWeight: 'bold',
                        padding: [3, 5]
                    }},
                    splitArea: {{
                        show: true,
                        areaStyle: {{
                            color: ['rgba(59, 130, 246, 0.05)', 'rgba(59, 130, 246, 0.1)']
                        }}
                    }},
                    axisLine: {{
                        lineStyle: {{
                            color: '#e2e8f0',
                            width: 1
                        }}
                    }},
                    splitLine: {{
                        lineStyle: {{
                            color: '#e2e8f0',
                            width: 1
                        }}
                    }}
                }},
                series: [{{
                    type: 'radar',
                    data: [{{
                        value: scoreValues,
                        name: '当前状态',
                        areaStyle: {{
                            color: 'rgba(59, 130, 246, 0.4)'
                        }},
                        lineStyle: {{
                            color: '#3b82f6',
                            width: 3
                        }},
                        itemStyle: {{
                            color: '#1e3a8a',
                            borderWidth: 2,
                            borderColor: '#fff',
                            shadowBlur: 4,
                            shadowColor: 'rgba(0, 0, 0, 0.2)'
                        }}
                    }}]
                }}],
                legend: {{
                    bottom: 0,
                    left: 'center',
                    textStyle: {{
                        color: '#475569',
                        fontSize: 13
                    }}
                }},
                tooltip: {{
                    trigger: 'item',
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    borderColor: '#3b82f6',
                    borderWidth: 1,
                    textStyle: {{
                        color: '#f1f5f9',
                        fontSize: 13
                    }},
                    formatter: function(params) {{
                        return params.name + '<br/>' + 
                               dimensions.map((dim, i) => 
                                   dim + ': ' + params.data.value[i] + '分'
                               ).join('<br/>');
                    }}
                }}
            }};

            myChart.setOption(option);

            // 响应式处理 - 立即resize一次
            setTimeout(() => {{
                myChart.resize();
            }}, 100);

            // 窗口大小改变时resize
            window.addEventListener('resize', function() {{
                setTimeout(() => {{
                    const newWidth = chartDom.parentElement.clientWidth - 40;
                    chartDom.style.width = newWidth + 'px';
                    myChart.resize();
                }}, 100);
            }});
        }}

        // 生成分析内容
        function generateAnalysis(scores) {{
            const analysisContent = document.getElementById('analysisContent');
            analysisContent.innerHTML = '';

            dimensions.forEach(dim => {{
                const score = parseFloat(scores[dim]);
                let level, text, className;

                if (score >= 8) {{
                    level = '优秀';
                    text = `${{dim}}维度表现优秀，是组织的优势领域，建议继续保持并进一步强化。`;
                    className = 'high';
                }} else if (score >= 6) {{
                    level = '良好';
                    text = `${{dim}}维度表现良好，仍有提升空间，建议进行优化完善。`;
                    className = 'medium';
                }} else if (score >= 4) {{
                    level = '中等';
                    text = `${{dim}}维度表现一般，存在明显短板，需要重点关注和改善。`;
                    className = 'medium';
                }} else {{
                    level = '较差';
                    text = `${{dim}}维度表现较差，严重影响组织效能，急需进行系统性改进。`;
                    className = 'low';
                }}

                const item = document.createElement('div');
                item.className = `analysis-item ${{className}}`;
                item.innerHTML = `
                    <strong>${{dim}} - ${{level}}（${{score}}分）</strong>
                    <p style="margin-top: 8px; color: #475569;">${{text}}</p>
                `;
                analysisContent.appendChild(item);
            }});
        }}

        // 生成改进建议
        function generateRecommendations(scores) {{
            const recommendations = document.getElementById('recommendations');
            recommendations.innerHTML = '';

            // 找出得分最低的维度
            const sortedDimensions = dimensions
                .map(dim => ({{ dimension: dim, score: parseFloat(scores[dim]) }}))
                .sort((a, b) => a.score - b.score);

            // 找出需要改进的维度（得分低于7分）
            const needImprovement = sortedDimensions.filter(item => item.score < 7);

            if (needImprovement.length === 0) {{
                // 所有维度都很好，给出总体建议
                const recList = document.createElement('ul');
                recList.style.listStyle = 'none';
                
                const li = document.createElement('li');
                li.style.padding = '16px';
                li.style.background = '#ecfdf5';
                li.style.borderRadius = '8px';
                li.style.borderLeft = '4px solid #10b981';
                li.innerHTML = `
                    <strong style="color: #059669; font-size: 15px;">✅ 组织健康度优秀</strong>
                    <p style="margin-top: 8px; font-size: 14px; color: #475569; line-height: 1.6;">
                        各维度表现均衡且优秀，建议继续保持现有优势，定期评估和优化，建立持续改进机制，确保组织能力持续提升。
                    </p>
                `;
                recList.appendChild(li);
                recommendations.appendChild(recList);
                return;
            }}

            // 检查各维度的问题是否相似
            const scoresArray = needImprovement.map(item => item.score);
            const minScore = Math.min(...scoresArray);
            const maxScore = Math.max(...scoresArray);
            const scoreRange = maxScore - minScore;

            const recList = document.createElement('ul');
            recList.style.listStyle = 'none';

            // 如果分数差异小于2分，说明问题相似，合并建议
            if (scoreRange < 2 && needImprovement.length > 1) {{
                const li = document.createElement('li');
                li.style.padding = '16px';
                li.style.marginBottom = '12px';
                li.style.background = '#f0f9ff';
                li.style.borderRadius = '8px';
                li.style.borderLeft = '4px solid #3b82f6';
                
                const dimNames = needImprovement.map(item => item.dimension).join('、');
                const avgScore = (scoresArray.reduce((a, b) => a + b, 0) / scoresArray.length).toFixed(1);
                
                li.innerHTML = `
                    <strong style="color: #3b82f6; font-size: 15px;">${{dimNames}} - 综合改善建议</strong>
                    <p style="margin-top: 8px; font-size: 14px; color: #475569; line-height: 1.6;">
                        这些维度表现接近（平均${{avgScore}}分），反映出组织在系统协同方面需要加强。建议从以下方面入手：
                    </p>
                    <ul style="margin-top: 8px; margin-left: 20px; font-size: 13px; color: #64748b; line-height: 1.8;">
                        <li><strong>统一战略与执行：</strong>确保战略目标在各个维度的一致性，避免各自为政</li>
                        <li><strong>强化制度建设：</strong>完善相关制度流程，确保各项工作有章可循</li>
                        <li><strong>提升组织能力：</strong>加强培训和能力建设，提升整体素质</li>
                        <li><strong>优化沟通机制：</strong>建立顺畅的内部沟通渠道，促进信息共享</li>
                        <li><strong>定期评估反馈：</strong>建立定期评估机制，及时发现问题并调整</li>
                    </ul>
                    <p style="margin-top: 8px; font-size: 13px; color: #64748b; padding-top: 8px; border-top: 1px solid #e2e8f0;">
                        📅 建议制定3-6个月的改进计划，每月跟进进展，确保改进措施有效落地。
                    </p>
                `;
                recList.appendChild(li);
            }} else {{
                // 各维度问题不同，提供针对性建议
                const dimensionRecommendations = {{
                    '战略': [
                        '明确战略目标和优先级，确保方向清晰',
                        '加强战略沟通和宣贯，确保全员理解',
                        '建立战略执行监控机制，确保落地到位'
                    ],
                    '结构': [
                        '优化组织结构，明确各部门职责边界',
                        '减少管理层级，提升决策效率',
                        '建立跨部门协作机制，打破部门壁垒'
                    ],
                    '制度': [
                        '完善关键业务流程和制度',
                        '建立绩效考核和激励机制',
                        '优化资源配置和审批流程'
                    ],
                    '风格': [
                        '强化领导力建设，提升管理效能',
                        '营造开放包容的组织文化',
                        '建立及时反馈和沟通机制'
                    ],
                    '人员': [
                        '加强人才引进和培养',
                        '建立人才梯队，做好人才储备',
                        '优化人员配置，提升整体效能'
                    ],
                    '技能': [
                        '识别关键能力缺口，制定培训计划',
                        '建立知识管理体系，促进经验分享',
                        '鼓励学习和创新，持续提升能力'
                    ],
                    '共同价值观': [
                        '提炼和强化核心价值观',
                        '将价值观融入日常管理和考核',
                        '通过文化建设增强凝聚力和认同感'
                    ]
                }};

                needImprovement.forEach(item => {{
                    const li = document.createElement('li');
                    li.style.padding = '16px';
                    li.style.marginBottom = '12px';
                    li.style.background = '#fef2f2';
                    li.style.borderRadius = '8px';
                    li.style.borderLeft = '4px solid #ef4444';
                    
                    const recs = dimensionRecommendations[item.dimension] || ['制定具体的改进计划'];
                    
                    li.innerHTML = `
                        <strong style="color: #dc2626; font-size: 15px;">${{item.dimension}} - 优先改善（${{item.score}}分）</strong>
                        <p style="margin-top: 8px; font-size: 14px; color: #475569;">
                            该维度得分较低，需要优先关注和改善。建议措施：
                        </p>
                        <ul style="margin-top: 6px; margin-left: 20px; font-size: 13px; color: #64748b; line-height: 1.8;">
                            ${{recs.map(rec => `<li>${{rec}}</li>`).join('')}}
                        </ul>
                        <p style="margin-top: 8px; font-size: 13px; color: #64748b; padding-top: 8px; border-top: 1px solid #e2e8f0;">
                            📅 建议制定1-3个月的专项改进计划，重点突破，快速见效。
                        </p>
                    `;
                    recList.appendChild(li);
                }});
            }}

            recommendations.appendChild(recList);
        }}

        // 显示报告
        function showReport() {{
            document.getElementById('questionnaireContainer').classList.add('hidden');
            document.getElementById('reportContainer').classList.add('active');
            document.getElementById('actionBar').style.display = 'flex';
            window.scrollTo(0, 0);
        }}

        // 显示问卷
        function showQuestionnaire() {{
            document.getElementById('reportContainer').classList.remove('active');
            document.getElementById('questionnaireContainer').classList.remove('hidden');
            document.getElementById('actionBar').style.display = 'none';
            window.scrollTo(0, 0);
        }}

        // 下载HTML功能
        function downloadHTML() {{
            var htmlContent = document.documentElement.outerHTML;
            var blob = new Blob([htmlContent], {{ type: 'text/html;charset=utf-8' }});
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = '{title}_诊断报告.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}

        // 下载PDF功能
        function downloadPDF() {{
            var element = document.getElementById('reportContainer');
            var opt = {{
                margin: 10,
                filename: '{title}_诊断报告.pdf',
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
        print("用法: python generate_diagnostic_questionnaire.py '<JSON数据>'")
        print("示例: python generate_diagnostic_questionnaire.py '{\"questionnaire_type\":\"7s\",\"company_name\":\"XX公司\",\"questions\":[{\"dimension\":\"战略\",\"question\":\"...\"}]}'")
        return 1

    input_str = sys.argv[1]

    try:
        # 解析输入
        data = parse_input(input_str)

        # 生成问卷
        result_path = generate_questionnaire(data)

        print(f"诊断问卷已生成: {result_path}")
        return 0

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
