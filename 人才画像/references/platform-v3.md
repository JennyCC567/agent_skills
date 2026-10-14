# 平台化建设 v3.0

> **版本**：v3.0
> **更新日期**：2026-06-08
> **适用范围**：人才知识图谱、多租户、开放API

---

## 目录

1. [人才知识图谱](#1-人才知识图谱)
2. [多租户架构](#2-多租户架构)
3. [开放API](#3-开放api)

---

## 1. 人才知识图谱

### 1.1 实体关系模型

```python
# 人才知识图谱实体关系模型
talent_knowledge_graph_schema = {
    "entities": {
        "Candidate": {
            "description": "候选人实体",
            "properties": {
                "candidate_id": {"type": "string", "unique": True},
                "name": {"type": "string"},
                "gender": {"type": "enum", "values": ["男", "女", "未知"]},
                "age": {"type": "integer"},
                "phone": {"type": "string"},
                "email": {"type": "string"},
                "highest_education": {"type": "enum", "values": ["博士", "硕士", "本科", "大专", "中专", "高中", "未知"]},
                "current_location": {"type": "string"},
                "expected_salary": {"type": "integer"},
                "current_status": {"type": "enum", "values": ["求职", "在职", "考虑机会", "不活跃"]}
            },
            "indexes": ["candidate_id", "email", "phone"]
        },
        "Company": {
            "description": "企业实体",
            "properties": {
                "company_id": {"type": "string", "unique": True},
                "name": {"type": "string"},
                "industry": {"type": "string"},
                "size": {"type": "enum", "values": ["小型", "中型", "大型", "超大型"]},
                "location": {"type": "string"},
                "founded_year": {"type": "integer"}
            }
        },
        "Position": {
            "description": "职位实体",
            "properties": {
                "position_id": {"type": "string", "unique": True},
                "title": {"type": "string"},
                "category": {"type": "string"},
                "level": {"type": "enum", "values": ["初级", "中级", "高级", "专家", "管理"]},
                "salary_range": {"type": "object", "properties": {"min": "integer", "max": "integer"}}
            }
        },
        "School": {
            "description": "院校实体",
            "properties": {
                "school_id": {"type": "string", "unique": True},
                "name": {"type": "string"},
                "type": {"type": "enum", "values": ["985", "211", "普通一本", "普通二本", "专科", "海外"]},
                "location": {"type": "string"},
                "ranking": {"type": "integer"}
            }
        },
        "Skill": {
            "description": "技能实体",
            "properties": {
                "skill_id": {"type": "string", "unique": True},
                "name": {"type": "string"},
                "category": {"type": "string"},
                "level": {"type": "enum", "values": ["初级", "中级", "高级", "专家"]}
            }
        }
    },
    
    "relationships": {
        "WORKED_AT": {
            "source": "Candidate",
            "target": "Company",
            "properties": {
                "position": {"type": "string"},
                "start_date": {"type": "date"},
                "end_date": {"type": "date"},
                "still_working": {"type": "boolean"}
            }
        },
        "GRADUATED_FROM": {
            "source": "Candidate",
            "target": "School",
            "properties": {
                "degree": {"type": "string"},
                "major": {"type": "string"},
                "graduation_year": {"type": "integer"}
            }
        },
        "HAS_SKILL": {
            "source": "Candidate",
            "target": "Skill",
            "properties": {
                "proficiency": {"type": "enum", "values": ["了解", "熟悉", "掌握", "精通"]},
                "years_of_experience": {"type": "integer"}
            }
        },
        "SIMILAR_TO": {
            "source": "Candidate",
            "target": "Candidate",
            "properties": {
                "similarity_score": {"type": "float", "min": 0, "max": 1},
                "similarity_type": {"type": "enum", "values": ["技能相似", "背景相似", "经历相似"]}
            }
        },
        "COMPETITOR_OF": {
            "source": "Company",
            "target": "Company",
            "properties": {
                "competition_intensity": {"type": "float", "min": 0, "max": 1},
                "shared_talent_rate": {"type": "float", "min": 0, "max": 1}
            }
        },
        "REQUIRES_SKILL": {
            "source": "Position",
            "target": "Skill",
            "properties": {
                "importance": {"type": "enum", "values": ["必要", "加分", "可选"]}
            }
        }
    }
}
```

### 1.2 图数据库操作

```python
# 图数据库操作接口
class TalentKnowledgeGraph:
    """人才知识图谱"""
    
    def __init__(self, config: Dict):
        # 支持Neo4j/JanusGraph/TigerGraph
        self.graph_db = self._connect_graph_db(config)
        self.query_engine = GraphQueryEngine()
    
    def add_candidate(self, candidate_data: Dict) -> str:
        """添加候选人到图谱"""
        cypher = """
        MERGE (c:Candidate {candidate_id: $candidate_id})
        SET c.name = $name,
            c.highest_education = $highest_education,
            c.current_location = $current_location
        RETURN c.candidate_id
        """
        
        params = {
            "candidate_id": candidate_data["candidate_id"],
            "name": candidate_data["name"],
            "highest_education": candidate_data.get("education", {}).get("highest_education", "未知"),
            "current_location": candidate_data.get("location", {}).get("city", "")
        }
        
        result = self.graph_db.run(cypher, params)
        return result[0]["c.candidate_id"]
    
    def link_candidate_skill(self, candidate_id: str, skill_name: str, proficiency: str):
        """关联候选人技能"""
        cypher = """
        MATCH (c:Candidate {candidate_id: $candidate_id})
        MERGE (s:Skill {name: $skill_name})
        MERGE (c)-[r:HAS_SKILL]->(s)
        SET r.proficiency = $proficiency
        """
        
        self.graph_db.run(cypher, {
            "candidate_id": candidate_id,
            "skill_name": skill_name,
            "proficiency": proficiency
        })
    
    def link_candidate_school(self, candidate_id: str, school_name: str, education_data: Dict):
        """关联候选人院校"""
        cypher = """
        MATCH (c:Candidate {candidate_id: $candidate_id})
        MERGE (s:School {name: $school_name})
        MERGE (c)-[r:GRADUATED_FROM]->(s)
        SET r.degree = $degree,
            r.major = $major,
            r.graduation_year = $graduation_year
        """
        
        self.graph_db.run(cypher, {
            "candidate_id": candidate_id,
            "school_name": school_name,
            "degree": education_data.get("highest_education", "未知"),
            "major": education_data.get("major", "不限"),
            "graduation_year": education_data.get("graduation_year", "未知")
        })
    
    def find_similar_candidates(self, candidate_id: str, limit: int = 10) -> List[Dict]:
        """查找相似候选人"""
        cypher = """
        MATCH (c1:Candidate {candidate_id: $candidate_id})
        MATCH (c1)-[:HAS_SKILL]->(s:Skill)<-[:HAS_SKILL]-(c2:Candidate)
        WITH c1, c2, count(s) as common_skills
        MATCH (c1)-[r1:HAS_SKILL]->(s1)<-[r2:HAS_SKILL]-(c2)
        WITH c1, c2, common_skills, collect(s.skill_name) as skills
        RETURN c2.candidate_id as candidate_id,
               c2.name as name,
               common_skills,
               skills,
               1.0 * common_skills / (size((c1)-[:HAS_SKILL]->()) + size((c2)-[:HAS_SKILL]->()) - common_skills) as similarity
        ORDER BY similarity DESC
        LIMIT $limit
        """
        
        results = self.graph_db.run(cypher, {"candidate_id": candidate_id, "limit": limit})
        return [dict(r) for r in results]
    
    def find_talent_flow(self, from_company: str, to_company: str) -> List[Dict]:
        """查找人才流动路径"""
        cypher = """
        MATCH (c1:Company {name: $from_company})<-[:WORKED_AT]-(candidate)-[:WORKED_AT]->(c2:Company {name: $to_company})
        RETURN candidate.name as name,
               c1.name as from_company,
               c2.name as to_company
        """
        
        results = self.graph_db.run(cypher, {
            "from_company": from_company,
            "to_company": to_company
        })
        return [dict(r) for r in results]
```

---

## 2. 多租户架构

### 2.1 多租户数据模型

```python
# 多租户数据模型
multitenancy_config = {
    "isolation_strategy": "database",  # database/schema/row
    
    "tenant_model": {
        "tenant_id": {
            "type": "string",
            "description": "租户唯一标识"
        },
        "tenant_name": {
            "type": "string",
            "description": "租户名称"
        },
        "tenant_type": {
            "type": "enum",
            "values": ["enterprise", "smb", "trial"],
            "description": "租户类型"
        },
        "plan": {
            "type": "enum",
            "values": ["free", "basic", "pro", "enterprise"],
            "description": "订阅套餐"
        },
        "data_quota": {
            "type": "object",
            "description": "数据配额",
            "properties": {
                "max_candidates": {"type": "integer"},
                "max_jobs": {"type": "integer"},
                "max_storage_gb": {"type": "integer"}
            }
        },
        "features": {
            "type": "object",
            "description": "功能开关",
            "properties": {
                "ai_recommendation": {"type": "boolean"},
                "market_benchmark": {"type": "boolean"},
                "api_access": {"type": "boolean"},
                "white_label": {"type": "boolean"}
            }
        }
    },
    
    "data_isolation": {
        "candidates": {
            "index_field": "tenant_id",
            "query_filter": "WHERE tenant_id = :current_tenant"
        },
        "jobs": {
            "index_field": "tenant_id",
            "query_filter": "WHERE tenant_id = :current_tenant"
        },
        "analytics": {
            "index_field": "tenant_id",
            "query_filter": "WHERE tenant_id = :current_tenant"
        }
    }
}
```

### 2.2 租户权限管理

```python
# 租户权限管理
class TenantPermissionManager:
    """租户权限管理器"""
    
    def __init__(self):
        self.role_definitions = self._load_role_definitions()
    
    def check_permission(self, user: Dict, resource: str, action: str) -> bool:
        """检查用户权限"""
        tenant = user.get("tenant_id")
        role = user.get("role")
        
        # 管理员拥有所有权限
        if role == "tenant_admin":
            return True
        
        # 检查资源权限
        resource_perms = self.role_definitions.get(role, {}).get(resource, [])
        return action in resource_perms
    
    def get_accessible_data(self, user: Dict, data_type: str) -> Dict:
        """获取用户可访问的数据范围"""
        tenant = user.get("tenant_id")
        role = user.get("role")
        
        if role == "tenant_admin":
            # 管理员可访问所有数据
            return {"tenant_id": tenant}
        elif role == "department_head":
            # 部门负责人访问本部门数据
            return {
                "tenant_id": tenant,
                "department_id": user.get("department_id")
            }
        elif role == "recruiter":
            # 招聘专员只能访问自己的数据
            return {
                "tenant_id": tenant,
                "created_by": user.get("user_id")
            }
        else:
            # 普通用户只能访问公开数据
            return {
                "tenant_id": tenant,
                "visibility": "public"
            }
    
    def _load_role_definitions(self) -> Dict:
        """加载角色权限定义"""
        return {
            "tenant_admin": {
                "candidates": ["read", "write", "delete", "export"],
                "jobs": ["read", "write", "delete", "publish"],
                "analytics": ["read", "export"],
                "users": ["read", "write", "delete"],
                "settings": ["read", "write"]
            },
            "department_head": {
                "candidates": ["read", "write", "export"],
                "jobs": ["read", "write"],
                "analytics": ["read", "export"],
                "users": ["read"]
            },
            "recruiter": {
                "candidates": ["read", "write"],
                "jobs": ["read"],
                "analytics": ["read"]
            },
            "viewer": {
                "candidates": ["read"],
                "jobs": ["read"],
                "analytics": ["read"]
            }
        }
```

### 2.3 数据配额管理

```python
# 数据配额管理
class DataQuotaManager:
    """数据配额管理器"""
    
    def __init__(self, tenant_config: Dict):
        self.tenant_config = tenant_config
        self.quota_limits = tenant_config.get("data_quota", {})
    
    def check_quota(self, tenant_id: str, data_type: str) -> Dict:
        """检查配额使用情况"""
        limits = self.quota_limits
        usage = self._get_usage(tenant_id, data_type)
        
        if data_type == "candidates":
            limit = limits.get("max_candidates", 1000)
        elif data_type == "jobs":
            limit = limits.get("max_jobs", 100)
        else:
            limit = limits.get("max_storage_gb", 10) * 1024 * 1024  # 转换为KB
        
        return {
            "data_type": data_type,
            "limit": limit,
            "usage": usage,
            "remaining": limit - usage,
            "usage_rate": usage / limit if limit > 0 else 0,
            "is_exceeded": usage >= limit
        }
    
    def enforce_quota(self, tenant_id: str, data_type: str) -> bool:
        """执行配额检查"""
        quota_status = self.check_quota(tenant_id, data_type)
        
        if quota_status["is_exceeded"]:
            # 触发告警
            self._send_quota_alert(tenant_id, quota_status)
            return False
        
        return True
    
    def _get_usage(self, tenant_id: str, data_type: str) -> int:
        """获取当前使用量"""
        if data_type == "candidates":
            return self._count_candidates(tenant_id)
        elif data_type == "jobs":
            return self._count_jobs(tenant_id)
        else:
            return self._calculate_storage_usage(tenant_id)
```

---

## 3. 开放API

### 3.1 API架构设计

```python
# API架构设计
api_architecture = {
    "base_url": "/api/v1",
    
    "endpoints": {
        "candidates": {
            "GET /candidates": {
                "description": "获取候选人列表",
                "parameters": {
                    "page": {"type": "integer", "default": 1},
                    "page_size": {"type": "integer", "default": 20, "max": 100},
                    "skills": {"type": "string", "description": "技能筛选，逗号分隔"},
                    "education": {"type": "string", "description": "学历筛选"},
                    "experience_min": {"type": "integer", "description": "最小工作年限"},
                    "location": {"type": "string", "description": "地点筛选"}
                },
                "response": {
                    "total": "integer",
                    "page": "integer",
                    "page_size": "integer",
                    "data": [{"candidate_id": "string", "..."}]
                }
            },
            "GET /candidates/{id}": {
                "description": "获取候选人详情",
                "response": {"candidate_id": "string", "..."}
            },
            "POST /candidates": {
                "description": "创建候选人",
                "body": {"name": "string", "education": "object", "skills": "array", "..."},
                "response": {"candidate_id": "string"}
            }
        },
        "jobs": {
            "GET /jobs": {"description": "获取职位列表"},
            "GET /jobs/{id}": {"description": "获取职位详情"},
            "POST /jobs": {"description": "创建职位"}
        },
        "matching": {
            "POST /matching/match": {
                "description": "候选人匹配",
                "body": {"candidate_id": "string", "job_id": "string"},
                "response": {
                    "match_score": "float",
                    "skill_match": "float",
                    "experience_match": "float",
                    "education_match": "float",
                    "location_match": "float"
                }
            },
            "POST /matching/batch": {
                "description": "批量匹配",
                "body": {"candidate_ids": "array", "job_id": "string"},
                "response": {"matches": "array"}
            }
        },
        "analytics": {
            "GET /analytics/salary": {
                "description": "薪资分析",
                "parameters": {"position": "string", "location": "string"}
            },
            "GET /analytics/talent_pool": {
                "description": "人才池分析"
            },
            "GET /analytics/market": {
                "description": "市场分析"
            }
        }
    }
}
```

### 3.2 SDK实现

```python
# Python SDK实现
class TalentMappingSDK:
    """人才Mapping SDK"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.talentmapping.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def get_candidates(self, **kwargs) -> List[Dict]:
        """获取候选人列表"""
        response = self.session.get(f"{self.base_url}/api/v1/candidates", params=kwargs)
        response.raise_for_status()
        return response.json()["data"]
    
    def get_candidate(self, candidate_id: str) -> Dict:
        """获取候选人详情"""
        response = self.session.get(f"{self.base_url}/api/v1/candidates/{candidate_id}")
        response.raise_for_status()
        return response.json()
    
    def create_candidate(self, candidate_data: Dict) -> Dict:
        """创建候选人"""
        # 学历必填校验
        if "education" not in candidate_data:
            candidate_data["education"] = {}
        if not candidate_data["education"].get("highest_education"):
            candidate_data["education"]["highest_education"] = "未知"
        
        response = self.session.post(
            f"{self.base_url}/api/v1/candidates",
            json=candidate_data
        )
        response.raise_for_status()
        return response.json()
    
    def match_candidates(self, candidate_id: str, job_id: str) -> Dict:
        """候选人匹配"""
        response = self.session.post(
            f"{self.base_url}/api/v1/matching/match",
            json={"candidate_id": candidate_id, "job_id": job_id}
        )
        response.raise_for_status()
        return response.json()
    
    def batch_match(self, candidate_ids: List[str], job_id: str) -> List[Dict]:
        """批量匹配"""
        response = self.session.post(
            f"{self.base_url}/api/v1/matching/batch",
            json={"candidate_ids": candidate_ids, "job_id": job_id}
        )
        response.raise_for_status()
        return response.json()["matches"]
    
    def get_salary_analytics(self, position: str, location: str = None) -> Dict:
        """获取薪资分析"""
        params = {"position": position}
        if location:
            params["location"] = location
        
        response = self.session.get(
            f"{self.base_url}/api/v1/analytics/salary",
            params=params
        )
        response.raise_for_status()
        return response.json()
```

### 3.3 API网关

```python
# API网关配置
api_gateway_config = {
    "rate_limiting": {
        "enabled": True,
        "strategies": {
            "default": {
                "requests_per_minute": 60,
                "requests_per_hour": 1000,
                "requests_per_day": 10000
            },
            "premium": {
                "requests_per_minute": 300,
                "requests_per_hour": 5000,
                "requests_per_day": 50000
            }
        }
    },
    
    "authentication": {
        "methods": ["api_key", "oauth2", "jwt"],
        "default_method": "api_key"
    },
    
    "caching": {
        "enabled": True,
        "strategies": {
            "candidate_list": {"ttl": 300, "max_size": 1000},
            "candidate_detail": {"ttl": 600, "max_size": 5000},
            "analytics": {"ttl": 3600, "max_size": 100}
        }
    },
    
    "monitoring": {
        "enabled": True,
        "metrics": ["latency", "error_rate", "request_count", "quota_usage"],
        "alert_thresholds": {
            "latency_p99": 1000,
            "error_rate": 0.05
        }
    }
}
```

### 3.4 Webhook通知

```python
# Webhook通知配置
webhook_config = {
    "events": {
        "candidate_added": {
            "description": "新候选人添加",
            "payload": {
                "event": "candidate_added",
                "timestamp": "ISO8601",
                "data": {"candidate_id": "string", "..."}
            }
        },
        "candidate_updated": {
            "description": "候选人信息更新",
            "payload": {"..."}
        },
        "match_completed": {
            "description": "匹配完成",
            "payload": {
                "event": "match_completed",
                "data": {
                    "candidate_id": "string",
                    "job_id": "string",
                    "match_score": "float"
                }
            }
        },
        "alert_triggered": {
            "description": "预警触发",
            "payload": {
                "event": "alert_triggered",
                "data": {
                    "alert_type": "string",
                    "severity": "string",
                    "message": "string"
                }
            }
        }
    },
    
    "delivery": {
        "retry_times": 3,
        "retry_interval": 60,
        "timeout": 30,
        "signature_secret": "your_webhook_secret"
    }
}
```
