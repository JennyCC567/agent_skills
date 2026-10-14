# 行业解决方案 v3.0

> **版本**：v3.0
> **更新日期**：2026-06-08
> **适用范围**：定制化分析模型、行业基准数据库

---

## 目录

1. [行业解决方案概览](#1-行业解决方案概览)
2. [金融行业](#2-金融行业)
3. [科技行业](#3-科技行业)
4. [制造业](#4-制造业)
5. [医疗健康](#5-医疗健康)

---

## 1. 行业解决方案概览

### 1.1 行业分类

```python
# 行业分类配置
industry_config = {
    "industries": {
        "finance": {
            "name": "金融行业",
            "sub_industries": [
                "银行", "证券", "保险", "基金", "信托", "期货", "互联网金融"
            ],
            "key_positions": [
                "投资经理", "风控专员", "量化分析师", "合规经理",
                "客户经理", "产品经理", "IT开发"
            ],
            "key_skills": [
                "金融建模", "风险评估", "财务分析", "投资分析",
                "Python", "SQL", "数据分析"
            ],
            "certifications": [
                "CFA", "CPA", "FRM", "ACCA"
            ]
        },
        "tech": {
            "name": "科技行业",
            "sub_industries": [
                "互联网", "软件", "硬件", "半导体", "人工智能", "云计算"
            ],
            "key_positions": [
                "算法工程师", "后端开发", "前端开发", "产品经理",
                "测试工程师", "运维工程师", "数据分析师"
            ],
            "key_skills": [
                "Python", "Java", "Go", "机器学习", "深度学习",
                "分布式系统", "云原生"
            ],
            "certifications": [
                "AWS认证", "Azure认证", "PMP"
            ]
        },
        "manufacturing": {
            "name": "制造业",
            "sub_industries": [
                "汽车", "电子", "机械", "化工", "新能源", "航空航天"
            ],
            "key_positions": [
                "工艺工程师", "质量工程师", "供应链经理", "项目经理",
                "研发工程师", "生产主管"
            ],
            "key_skills": [
                "精益生产", "Six Sigma", "供应链管理", "质量管控",
                "CAD", "PLC编程"
            ],
            "certifications": [
                "PMP", "六西格玛绿带/黑带", "ISO内审员"
            ]
        },
        "healthcare": {
            "name": "医疗健康",
            "sub_industries": [
                "制药", "医疗器械", "医疗服务", "生物技术", "互联网医疗"
            ],
            "key_positions": [
                "医学经理", "临床运营", "注册专员", "销售代表",
                "市场专员", "BD经理"
            ],
            "key_skills": [
                "医学知识", "临床试验", "GCP", "市场准入",
                "销售技巧", "客户管理"
            ],
            "certifications": [
                "GCP证书", "执业药师", "医师资格证"
            ]
        }
    }
}
```

---

## 2. 金融行业

### 2.1 金融行业分析模型

```python
# 金融行业分析模型
class FinanceTalentAnalysisModel:
    """金融行业人才分析模型"""
    
    def __init__(self):
        self.industry = "finance"
        self.certification_weights = {
            "CFA": 0.15,
            "CPA": 0.12,
            "FRM": 0.10,
            "ACCA": 0.08
        }
        self.position_levels = {
            "analyst": 1,
            "associate": 2,
            "vice_president": 3,
            "director": 4,
            "managing_director": 5
        }
    
    def calculate_competitiveness_score(self, candidate: Dict) -> float:
        """计算人才竞争力评分"""
        score = 0
        
        # 教育背景（权重30%）
        education_score = self._evaluate_education(candidate.get("education", {}))
        score += education_score * 0.30
        
        # 证书资质（权重25%）
        cert_score = self._evaluate_certifications(candidate.get("certifications", []))
        score += cert_score * 0.25
        
        # 机构背景（权重25%）
        company_score = self._evaluate_company_background(candidate.get("work_experience", []))
        score += company_score * 0.25
        
        # 技能匹配（权重20%）
        skill_score = self._evaluate_skills(candidate.get("skills", []))
        score += skill_score * 0.20
        
        return round(score * 100, 2)
    
    def _evaluate_education(self, education: Dict) -> float:
        """评估教育背景"""
        education_scores = {
            "博士": 1.0,
            "硕士": 0.85,
            "本科": 0.70,
            "大专": 0.50
        }
        
        highest = education.get("highest_education", "未知")
        return education_scores.get(highest, 0.3)
    
    def _evaluate_certifications(self, certifications: List[str]) -> float:
        """评估证书资质"""
        score = 0
        for cert in certifications:
            cert_upper = cert.upper()
            if "CFA" in cert_upper:
                score += self.certification_weights["CFA"]
            elif "CPA" in cert_upper:
                score += self.certification_weights["CPA"]
            elif "FRM" in cert_upper:
                score += self.certification_weights["FRM"]
            elif "ACCA" in cert_upper:
                score += self.certification_weights["ACCA"]
        
        return min(score, 1.0)  # 最高1分
    
    def _evaluate_company_background(self, work_experience: List[Dict]) -> float:
        """评估机构背景"""
        tier1_companies = [
            "中金公司", "中信证券", "华泰证券", "高盛", "摩根士丹利",
            "摩根大通", "花旗", "汇丰"
        ]
        tier2_companies = [
            "招商证券", "国泰君安", "海通证券", "广发证券",
            "建设银行", "工商银行", "中国银行"
        ]
        
        score = 0
        for exp in work_experience:
            company = exp.get("company", "")
            if any(t1 in company for t1 in tier1_companies):
                score = max(score, 1.0)
            elif any(t2 in company for t2 in tier2_companies):
                score = max(score, 0.7)
        
        return score
    
    def _evaluate_skills(self, skills: List[str]) -> float:
        """评估技能匹配"""
        required_skills = [
            "金融建模", "风险评估", "财务分析", "Python", "SQL"
        ]
        
        matched = sum(1 for skill in skills if any(req in skill for req in required_skills))
        return matched / len(required_skills)
    
    def generate_finance_insight(self, talent_data: Dict) -> str:
        """生成金融行业洞察"""
        insights = []
        
        # CFA持有者分析
        cfa_count = sum(1 for c in talent_data if "CFA" in str(c.get("certifications", [])))
        insights.append(f"CFA持证人：{cfa_count}人，占比{cfa_count/len(talent_data)*100:.1f}%")
        
        # 机构背景分布
        tier1_count = self._count_tier1_companies(talent_data)
        insights.append(f"头部机构背景候选人：{tier1_count}人")
        
        # 薪酬预期分析
        avg_salary = self._calculate_avg_expected_salary(talent_data)
        insights.append(f"平均期望薪资：{avg_salary:.0f}K/月")
        
        return "\n".join(insights)
```

### 2.2 金融行业基准数据库

```python
# 金融行业薪资基准
finance_salary_benchmark = {
    "investment_management": {
        "job_title": "投资经理",
        "salary_range": {
            "entry": {"min": 25000, "max": 40000, "median": 32000},
            "mid": {"min": 40000, "max": 80000, "median": 60000},
            "senior": {"min": 80000, "max": 150000, "median": 100000}
        },
        "factors": {
            "certificate_bonus": {"CFA": 0.15, "CPA": 0.10},
            "company_tier_bonus": {"tier1": 0.30, "tier2": 0.15}
        }
    },
    "risk_management": {
        "job_title": "风控专员",
        "salary_range": {
            "entry": {"min": 18000, "max": 30000, "median": 24000},
            "mid": {"min": 30000, "max": 60000, "median": 45000},
            "senior": {"min": 60000, "max": 100000, "median": 80000}
        },
        "factors": {
            "certificate_bonus": {"FRM": 0.15, "CPA": 0.10},
            "industry_exp_bonus": 0.05  # 每3年经验加5%
        }
    },
    "quantitative_analysis": {
        "job_title": "量化分析师",
        "salary_range": {
            "entry": {"min": 30000, "max": 50000, "median": 40000},
            "mid": {"min": 50000, "max": 100000, "median": 75000},
            "senior": {"min": 100000, "max": 200000, "median": 150000}
        },
        "factors": {
            "tech_skills_bonus": {"Python": 0.20, "C++": 0.15, "Machine Learning": 0.25}
        }
    }
}
```

---

## 3. 科技行业

### 3.1 科技行业分析模型

```python
# 科技行业人才分析模型
class TechTalentAnalysisModel:
    """科技行业人才分析模型"""
    
    def __init__(self):
        self.industry = "tech"
        self.tech_stack_weights = {
            "programming_languages": {
                "Python": 0.08,
                "Java": 0.07,
                "Go": 0.08,
                "C++": 0.06,
                "JavaScript": 0.05
            },
            "frameworks": {
                "React": 0.06,
                "Vue": 0.05,
                "Spring": 0.06,
                "Django": 0.05
            },
            "infrastructure": {
                "Kubernetes": 0.07,
                "Docker": 0.05,
                "AWS": 0.06,
                "Azure": 0.05
            },
            "data": {
                "Machine Learning": 0.10,
                "Deep Learning": 0.12,
                "SQL": 0.05,
                "Spark": 0.06
            }
        }
    
    def calculate_technical_score(self, candidate: Dict) -> float:
        """计算技术能力评分"""
        score = 0
        skills = [s.lower() for s in candidate.get("skills", [])]
        
        # 编程语言
        for lang, weight in self.tech_stack_weights["programming_languages"].items():
            if lang.lower() in skills:
                score += weight
        
        # 框架
        for framework, weight in self.tech_stack_weights["frameworks"].items():
            if framework.lower() in skills:
                score += weight
        
        # 基础设施
        for infra, weight in self.tech_stack_weights["infrastructure"].items():
            if infra.lower() in skills:
                score += weight
        
        # 数据技能
        for data_skill, weight in self.tech_stack_weights["data"].items():
            if data_skill.lower() in skills:
                score += weight
        
        return min(score, 1.0) * 100
    
    def calculate_growth_potential(self, candidate: Dict) -> float:
        """计算成长潜力"""
        score = 0
        
        # 技术栈广度
        score += min(len(candidate.get("skills", [])) / 10, 1) * 0.3
        
        # 学习速度指标（用项目复杂度变化衡量）
        score += self._evaluate_learning_velocity(candidate.get("work_experience", [])) * 0.4
        
        # 开源贡献
        if candidate.get("github_contributions", 0) > 100:
            score += 0.15
        
        # 论文/专利
        papers = candidate.get("papers", [])
        patents = candidate.get("patents", [])
        score += min((len(papers) * 0.05 + len(patents) * 0.08), 0.15)
        
        return score * 100
    
    def _evaluate_learning_velocity(self, work_experience: List[Dict]) -> float:
        """评估学习速度"""
        if len(work_experience) < 2:
            return 0.5
        
        # 计算项目复杂度变化
        complexity_scores = [exp.get("project_complexity", 5) for exp in work_experience]
        
        # 线性回归斜率
        import numpy as np
        x = np.arange(len(complexity_scores))
        y = np.array(complexity_scores)
        
        if len(x) > 1:
            slope = np.polyfit(x, y, 1)[0]
            return max(0, min(slope / 10, 1))  # 归一化到0-1
        
        return 0.5
    
    def generate_tech_insight(self, talent_data: List[Dict]) -> str:
        """生成科技行业洞察"""
        insights = []
        
        # 技术栈分布
        tech_stack_dist = self._analyze_tech_stack_distribution(talent_data)
        top_tech = sorted(tech_stack_dist.items(), key=lambda x: x[1], reverse=True)[:5]
        insights.append(f"热门技术栈：{', '.join([f'{t[0]}({t[1]}人)' for t in top_tech])}")
        
        # 薪资期望分析
        avg_exp_salary = self._calculate_tech_salary_expectation(talent_data)
        insights.append(f"平均期望薪资：{avg_exp_salary:.0f}K/月")
        
        # 人才流动分析
        mobility_rate = self._calculate_mobility_rate(talent_data)
        insights.append(f"平均跳槽频率：{mobility_rate:.1f}次/年")
        
        return "\n".join(insights)
```

### 3.2 科技行业基准数据库

```python
# 科技行业薪资基准
tech_salary_benchmark = {
    "software_engineer": {
        "job_title": "软件开发工程师",
        "salary_range": {
            "entry_1_3y": {"min": 15000, "max": 30000, "median": 22000},
            "mid_3_5y": {"min": 30000, "max": 50000, "median": 40000},
            "senior_5_8y": {"min": 50000, "max": 80000, "median": 65000},
            "expert_8y+": {"min": 80000, "max": 120000, "median": 100000}
        },
        "hot_skills": ["Python", "Java", "Go", "Kubernetes"]
    },
    "algorithm_engineer": {
        "job_title": "算法工程师",
        "salary_range": {
            "entry_1_3y": {"min": 25000, "max": 45000, "median": 35000},
            "mid_3_5y": {"min": 45000, "max": 80000, "median": 60000},
            "senior_5_8y": {"min": 80000, "max": 150000, "median": 100000},
            "expert_8y+": {"min": 150000, "max": 250000, "median": 200000}
        },
        "hot_skills": ["Deep Learning", "NLP", "Computer Vision", "Recommendation"]
    },
    "product_manager": {
        "job_title": "产品经理",
        "salary_range": {
            "entry_1_3y": {"min": 18000, "max": 35000, "median": 26000},
            "mid_3_5y": {"min": 35000, "max": 60000, "median": 45000},
            "senior_5_8y": {"min": 60000, "max": 100000, "median": 80000},
            "expert_8y+": {"min": 100000, "max": 150000, "median": 120000}
        },
        "hot_skills": ["数据分析", "用户研究", "PRD", "项目管理"]
    }
}
```

---

## 4. 制造业

### 4.1 制造业分析模型

```python
# 制造业人才分析模型
class ManufacturingTalentAnalysisModel:
    """制造业人才分析模型"""
    
    def __init__(self):
        self.industry = "manufacturing"
        self.quality_certifications = [
            "六西格玛绿带", "六西格玛黑带", "PMP", "ISO内审员"
        ]
        self.technical_skills = [
            "CAD", "SolidWorks", "PLC编程", "精益生产", "SAP"
        ]
    
    def calculate_operation_efficiency(self, candidate: Dict) -> float:
        """计算运营效率评分"""
        score = 0
        
        # 精益生产经验
        if any("精益" in exp.get("description", "") for exp in candidate.get("work_experience", [])):
            score += 0.25
        
        # 质量管理证书
        certs = candidate.get("certifications", [])
        for cert in certs:
            if "六西格玛" in cert:
                score += 0.20
            elif "PMP" in cert:
                score += 0.15
        
        # 技术技能
        skills = [s.lower() for s in candidate.get("skills", [])]
        for skill in self.technical_skills:
            if skill.lower() in skills:
                score += 0.10
        
        return min(score, 1.0) * 100
    
    def evaluate_supply_chain_competency(self, candidate: Dict) -> float:
        """评估供应链能力"""
        score = 0
        
        # 供应链管理经验年限
        exp_years = self._calculate_supply_chain_exp(candidate.get("work_experience", []))
        score += min(exp_years / 10, 1) * 0.40
        
        # 供应商管理能力
        if candidate.get("supplier_management_exp", 0) > 0:
            score += 0.30
        
        # ERP系统使用经验
        if "SAP" in str(candidate.get("skills", [])):
            score += 0.20
        
        # 成本控制经验
        if candidate.get("cost_control_exp", False):
            score += 0.10
        
        return score * 100
```

---

## 5. 医疗健康

### 5.1 医疗健康分析模型

```python
# 医疗健康人才分析模型
class HealthcareTalentAnalysisModel:
    """医疗健康人才分析模型"""
    
    def __init__(self):
        self.industry = "healthcare"
        self.required_certifications = [
            "GCP证书", "执业药师", "医师资格证", "护士资格证"
        ]
    
    def evaluate_compliance_capability(self, candidate: Dict) -> float:
        """评估合规能力"""
        score = 0
        
        # GCP证书（临床试验必备）
        certs = candidate.get("certifications", [])
        if any("GCP" in cert for cert in certs):
            score += 0.35
        
        # 法规知识
        regulatory_knowledge = candidate.get("regulatory_knowledge", [])
        if "NMPA" in regulatory_knowledge:
            score += 0.20
        if "FDA" in regulatory_knowledge:
            score += 0.25
        
        # 审计经验
        if candidate.get("audit_experience", 0) > 0:
            score += 0.20
        
        return score * 100
    
    def calculate_market_access_ability(self, candidate: Dict) -> float:
        """评估市场准入能力"""
        score = 0
        
        # 市场准入项目经验
        ma_projects = candidate.get("market_access_projects", 0)
        score += min(ma_projects / 5, 1) * 0.40
        
        # 医保目录经验
        if candidate.get("nra_list_experience", False):
            score += 0.25
        
        # 招标经验
        bidding_exp = candidate.get("bidding_experience", 0)
        score += min(bidding_exp / 10, 1) * 0.20
        
        # KOL关系
        kols = candidate.get("kol_relationships", 0)
        score += min(kols / 20, 1) * 0.15
        
        return score * 100
```

### 5.2 行业基准数据库查询

```python
# 行业基准数据库查询接口
class IndustryBenchmarkDatabase:
    """行业基准数据库"""
    
    def __init__(self):
        self.benchmarks = {
            "finance": finance_salary_benchmark,
            "tech": tech_salary_benchmark,
            "manufacturing": self._load_manufacturing_benchmark(),
            "healthcare": self._load_healthcare_benchmark()
        }
    
    def query_salary_benchmark(
        self, 
        industry: str, 
        position: str, 
        experience_years: int,
        location: str = None
    ) -> Dict:
        """查询薪资基准"""
        
        benchmark = self.benchmarks.get(industry, {})
        position_data = benchmark.get(position, {})
        
        # 根据经验年限确定级别
        if experience_years <= 3:
            level = "entry"
        elif experience_years <= 5:
            level = "mid"
        elif experience_years <= 8:
            level = "senior"
        else:
            level = "expert"
        
        salary_range = position_data.get("salary_range", {}).get(level, {})
        
        # 地区系数
        location_multiplier = self._get_location_multiplier(location)
        
        return {
            "industry": industry,
            "position": position,
            "experience_years": experience_years,
            "location": location,
            "salary_range": {
                "min": int(salary_range.get("min", 0) * location_multiplier),
                "max": int(salary_range.get("max", 0) * location_multiplier),
                "median": int(salary_range.get("median", 0) * location_multiplier)
            },
            "hot_skills": position_data.get("hot_skills", []),
            "updated_at": datetime.now().isoformat()
        }
    
    def _get_location_multiplier(self, location: str) -> float:
        """获取地区系数"""
        multipliers = {
            "北京": 1.3,
            "上海": 1.25,
            "深圳": 1.2,
            "杭州": 1.15,
            "广州": 1.1,
            "新一线城市": 1.0,
            "二线城市": 0.9,
            "其他": 0.8
        }
        
        for city, mult in multipliers.items():
            if city in location:
                return mult
        
        return 1.0
```
