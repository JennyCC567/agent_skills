#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OD速诊模式 - 10题快诊+即时雷达图
"""

import json
import argparse

def generate_quick_diagnostic_html(company_name="贵公司"):
    from datetime import datetime
    date = datetime.now().strftime('%Y年%m月%d日')
    
    questions = [
        {"id": "q1", "dimension": "Strategy", "text": "公司有清晰的3-5年发展战略规划", "options": [("强烈不同意", 1), ("不同意", 2), ("中立", 3), ("同意", 4), ("强烈同意", 5)]},
        {"id": "q2", "dimension": "Structure", "text": "组织架构能有效支撑战略执行", "options": [("强烈不同意", 1), ("不同意", 2), ("中立", 3), ("同意", 4), ("强烈同意", 5)]},
        {"id": "q3", "dimension": "Systems", "text": "核心管理制度和流程清晰高效", "options": [("强烈不同意", 1), ("不同意", 2), ("中立", 3), ("同意", 4), ("强烈同意", 5)]},
        {"id": "q4", "dimension": "SharedValues", "text": "公司核心价值观得到员工广泛认同", "options": [("强烈不同意", 1), ("不同意", 2), ("中立", 3), ("同意", 4), ("强烈同意", 5)]},
        {"id": "q5", "dimension": "Skills", "text": "员工能力满足岗位和战略发展需求", "options": [("强烈不同意", 1), ("不同意", 2), ("中立", 3), ("同意", 4), ("强烈同意", 5)]},
        {"id": "q6", "dimension": "Style", "text": "领导团队管理风格适应公司发展", "options": [("强烈不同意", 1), ("不同意", 2), ("中立", 3), ("同意", 4), ("强烈同意", 5)]},
        {"id": "q7", "dimension": "Staff", "text": "关键岗位人才储备充足", "options": [("强烈不同意", 1), ("不同意", 2), ("中立", 3), ("同意", 4), ("强烈同意", 5)]},
        {"id": "q8", "dimension": "Culture", "text": "组织文化支持创新和协作", "options": [("强烈不同意", 1), ("不同意", 2), ("中立", 3), ("同意", 4), ("强烈同意", 5)]},
        {"id": "q9", "dimension": "Innovation", "text": "公司创新能力和学习速度行业领先", "options": [("强烈不同意", 1), ("不同意", 2), ("中立", 3), ("同意", 4), ("强烈同意", 5)]},
        {"id": "q10", "dimension": "Change", "text": "组织具备应对变革的能力和准备", "options": [("强烈不同意", 1), ("不同意", 2), ("中立", 3), ("同意", 4), ("强烈同意", 5)]}
    ]
    
    questions_html = ""
    for q in questions:
        options_html = ""
        for opt_text, opt_val in q["options"]:
            options_html += '<label class="option-label"><input type="radio" name="answer_' + q["id"] + '" value="' + str(opt_val) + '" class="option-radio" required>' + opt_text + '</label>'
        questions_html += '<div class="question-card"><div class="question-text"><span class="q-number">' + q["id"].replace("q", "#") + '</span> ' + q["text"] + '</div><div class="options-grid">' + options_html + '</div></div>'
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OD速诊问卷 - ''' + company_name + '''</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .header { background: white; border-radius: 16px; padding: 40px; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        .header h1 { font-size: 32px; color: #333; margin-bottom: 10px; }
        .header p { color: #666; font-size: 14px; }
        .progress-bar { background: #e8e8e8; height: 8px; border-radius: 4px; margin-top: 20px; overflow: hidden; }
        .progress-fill { background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; width: 0%; transition: width 0.3s; }
        .question-card { background: white; border-radius: 16px; padding: 30px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        .question-text { font-size: 18px; color: #333; margin-bottom: 20px; font-weight: 500; }
        .q-number { display: inline-block; width: 36px; height: 36px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 50%; text-align: center; line-height: 36px; margin-right: 12px; font-size: 14px; }
        .options-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
        .option-label { display: flex; flex-direction: column; align-items: center; padding: 15px 10px; background: #f8f9fa; border-radius: 12px; cursor: pointer; transition: all 0.2s; border: 2px solid transparent; }
        .option-label:hover { background: #e8e8f0; transform: translateY(-2px); }
        .option-label input { margin-bottom: 8px; width: 20px; height: 20px; accent-color: #667eea; }
        .option-label span { font-size: 12px; color: #666; text-align: center; }
        .submit-btn { display: block; width: 100%; padding: 18px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; border-radius: 12px; font-size: 18px; font-weight: 600; cursor: pointer; transition: transform 0.2s; }
        .submit-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4); }
        #resultPage { display: none; }
        .result-header { background: white; border-radius: 16px; padding: 40px; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        .radar-container { background: white; border-radius: 16px; padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        #radarChart { width: 100%; height: 400px; }
        .action-bar { background: white; border-radius: 16px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="container">
        <div id="questionPage">
            <div class="header">
                <h1>OD组织健康度速诊</h1>
                <p>基于7S模型的10题快速诊断，3分钟完成组织现状评估</p>
                <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
            </div>
            <form id="diagnosticForm">
                ''' + questions_html + '''
                <button type="submit" class="submit-btn">提交诊断 →</button>
            </form>
        </div>
        
        <div id="resultPage">
            <div class="result-header">
                <h1>诊断完成</h1>
                <p id="companyName"></p>
                <p id="diagnosisDate"></p>
            </div>
            <div class="radar-container">
                <h2 style="text-align:center;margin-bottom:20px;">组织健康度雷达图</h2>
                <div id="radarChart"></div>
            </div>
            <div class="action-bar">
                <button onclick="downloadHTML()" class="submit-btn">下载HTML报告</button>
            </div>
        </div>
    </div>
    
    <script>
        const dimensionNames = {"Strategy": "战略", "Structure": "结构", "Systems": "制度", "SharedValues": "价值观", "Skills": "技能", "Style": "领导力", "Staff": "人才", "Culture": "文化", "Innovation": "创新", "Change": "变革"};
        
        document.querySelectorAll('input[type=radio]').forEach(input => {
            input.addEventListener('change', updateProgress);
        });
        
        function updateProgress() {
            const total = document.querySelectorAll('.question-card').length;
            const answered = document.querySelectorAll('input[type=radio]:checked').length;
            document.getElementById('progressFill').style.width = (answered / total * 100) + '%';
        }
        
        document.getElementById('diagnosticForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const scores = {};
            let dimensionScores = {};
            
            formData.forEach((value, key) => {
                const qId = key.replace('answer_', '');
                if (!dimensionScores[qId]) dimensionScores[qId] = [];
                dimensionScores[qId].push(parseInt(value));
            });
            
            for (let qId in dimensionScores) {
                const avg = dimensionScores[qId].reduce((a, b) => a + b, 0) / dimensionScores[qId].length;
                scores[qId] = avg;
            }
            
            const avg = Object.values(scores).reduce((a, b) => a + b, 0) / Object.values(scores).length;
            document.getElementById('companyName').textContent = '受诊组织: ''' + company_name + '''';
            document.getElementById('diagnosisDate').textContent = '诊断时间: ' + new Date().toLocaleDateString('zh-CN');
            
            document.getElementById('questionPage').style.display = 'none';
            document.getElementById('resultPage').style.display = 'block';
            
            drawRadarChart(scores);
        });
        
        function drawRadarChart(scores) {
            const chartDom = document.getElementById('radarChart');
            const container = chartDom.parentElement;
            chartDom.style.width = container.clientWidth - 60 + 'px';
            chartDom.style.height = '400px';
            
            const dimensions = Object.keys(scores);
            const values = Object.values(scores);
            const names = dimensions.map(d => dimensionNames[d] || d);
            
            const chart = echarts.init(chartDom);
            const option = {
                radar: {
                    indicator: names.map((name, i) => ({ name: name, max: 5 })),
                    shape: 'polygon',
                    splitNumber: 5,
                    axisName: { color: '#333', fontSize: 14 },
                    splitLine: { lineStyle: { color: '#e8e8e8' } },
                    splitArea: { show: true, areaStyle: { color: ['#f8f9fa', '#fff'] } },
                    axisLine: { lineStyle: { color: '#ccc' } }
                },
                series: [{
                    type: 'radar',
                    data: [{ value: values, name: '健康度评分', areaStyle: { color: 'rgba(102, 126, 234, 0.3)' }, lineStyle: { color: '#667eea', width: 2 }, itemStyle: { color: '#667eea' } }]
                }]
            };
            chart.setOption(option);
            setTimeout(() => chart.resize(), 100);
        }
        
        function downloadHTML() {
            const html = document.documentElement.outerHTML;
            const blob = new Blob([html], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'OD速诊报告_' + new Date().toISOString().slice(0,10) + '.html';
            a.click();
            URL.revokeObjectURL(url);
        }
    </script>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
</body>
</html>'''
    return html

def main():
    parser = argparse.ArgumentParser(description='OD速诊模式 - 10题快诊+即时雷达图')
    parser.add_argument('--company', '-c', default='贵公司', help='公司名称')
    parser.add_argument('--output', '-o', default='./quick_diagnostic.html', help='输出文件路径')
    args = parser.parse_args()
    
    html = generate_quick_diagnostic_html(args.company)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(json.dumps({"status": "success", "output_path": args.output}, ensure_ascii=False))

if __name__ == "__main__":
    main()
