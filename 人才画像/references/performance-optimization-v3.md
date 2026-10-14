# 性能优化 v3.0

> **版本**：v3.0
> **更新日期**：2026-06-08
> **适用范围**：百万级数据检索、实时流处理

---

## 目录

1. [性能优化概览](#1-性能优化概览)
2. [数据存储优化](#2-数据存储优化)
3. [查询优化](#3-查询优化)
4. [实时处理架构](#4-实时处理架构)

---

## 1. 性能优化概览

### 1.1 性能指标

```python
# 性能指标定义
performance_metrics = {
    "latency": {
        "api_response_time": {
            "p50": 50,  # 毫秒
            "p95": 200,
            "p99": 500
        },
        "search_response_time": {
            "p50": 100,
            "p95": 500,
            "p99": 1000
        },
        "report_generation_time": {
            "small": 5000,  # <100条数据，毫秒
            "medium": 15000,  # 100-1000条数据
            "large": 60000   # 1000-10000条数据
        }
    },
    "throughput": {
        "concurrent_users": 1000,
        "requests_per_second": 500,
        "bulk_import_rate": 10000  # 条/分钟
    },
    "scalability": {
        "max_candidates": 10000000,  # 1000万
        "max_jobs": 100000,
        "max_organizations": 1000
    },
    "availability": {
        "uptime_sla": 0.999,
        "backup_frequency": "daily",
        "disaster_recovery_rto": 3600,  # 秒
        "disaster_recovery_rpo": 300   # 秒
    }
}
```

---

## 2. 数据存储优化

### 2.1 分库分表策略

```python
# 分库分表配置
sharding_config = {
    "strategy": "hash",  # hash/range/time
    
    "tables": {
        "candidates": {
            "sharding_key": "candidate_id",
            "sharding_algorithm": "hash_mod",
            "shard_count": 16,  # 16个分片
            "database_per_shard": 1,
            "partition_by": "tenant_id"  # 按租户隔离
        },
        "jobs": {
            "sharding_key": "job_id",
            "sharding_algorithm": "hash_mod",
            "shard_count": 8,
            "database_per_shard": 1
        },
        "applications": {
            "sharding_key": "application_id",
            "sharding_algorithm": "hash_mod",
            "shard_count": 32,
            "partition_by": "job_id"
        }
    },
    
    "index_optimization": {
        "candidate_compound_index": [
            "tenant_id",
            "highest_education",
            "current_location",
            "expected_salary"
        ],
        "candidate_skill_index": {
            "type": "inverted",
            "field": "skills",
            "analyzer": "ik_max_word"
        }
    }
}
```

### 2.2 索引优化策略

```python
# 索引优化
class IndexOptimizer:
    """索引优化器"""
    
    def __init__(self, db_config: Dict):
        self.db = self._connect_db(db_config)
    
    def create_indexes(self):
        """创建优化索引"""
        
        # 复合索引：候选人搜索
        self.db.execute("""
        CREATE INDEX idx_candidate_search 
        ON candidates (
            tenant_id,
            highest_education,
            current_location,
            expected_salary
        )
        """)
        
        # 技能倒排索引
        self.db.execute("""
        CREATE INDEX idx_candidate_skills 
        ON candidates (
            tenant_id,
            skills
        )
        USING GIN (
            to_tsvector('chinese', skills_text)
        )
        """)
        
        # 时间范围索引
        self.db.execute("""
        CREATE INDEX idx_candidate_update_time
        ON candidates (
            tenant_id,
            update_time
        )
        """)
    
    def analyze_query_performance(self, query: str) -> Dict:
        """分析查询性能"""
        explain_result = self.db.execute(f"EXPLAIN ANALYZE {query}")
        
        return {
            "execution_time": explain_result["Execution Time"],
            "rows_scanned": explain_result["Plan"]["Total Cost"],
            "index_used": "idx_candidate_search" in str(explain_result),
            "recommendations": self._generate_recommendations(explain_result)
        }
```

---

## 3. 查询优化

### 3.1 搜索查询优化

```python
# 搜索查询优化
class SearchQueryOptimizer:
    """搜索查询优化器"""
    
    def __init__(self, es_config: Dict):
        self.es_client = Elasticsearch(es_config)
    
    def optimize_search_query(self, query: Dict) -> Dict:
        """优化搜索查询"""
        
        # 1. 布尔查询优化
        optimized_query = {
            "query": {
                "bool": {
                    "filter": query["query"]["bool"]["filter"],
                    "should": query["query"]["bool"]["should"][:5]  # 限制should子句数量
                }
            },
            # 2. 限制返回字段
            "_source": ["candidate_id", "name", "skills", "education", "experience"],
            # 3. 分页优化
            "from": query.get("from", 0),
            "size": min(query.get("size", 20), 100),
            # 4. 性能优化参数
            "track_total_hits": False,  # 不追踪精确总数
            "timeout": "3s"
        }
        
        return optimized_query
    
    def build_caching_key(self, query: Dict) -> str:
        """构建缓存键"""
        import hashlib
        import json
        
        # 规范化查询参数
        normalized = {
            "skills": sorted(query.get("skills", [])),
            "education": query.get("education"),
            "location": query.get("location"),
            "page": query.get("page", 1),
            "page_size": query.get("page_size", 20)
        }
        
        query_str = json.dumps(normalized, sort_keys=True)
        cache_key = hashlib.md5(query_str.encode()).hexdigest()
        
        return f"search:{cache_key}"
    
    def get_cached_results(self, cache_key: str) -> Optional[Dict]:
        """获取缓存结果"""
        return redis_client.get(cache_key)
    
    def cache_results(self, cache_key: str, results: Dict, ttl: int = 300):
        """缓存查询结果"""
        redis_client.setex(cache_key, ttl, json.dumps(results))
```

### 3.2 批量处理优化

```python
# 批量处理优化
class BatchProcessor:
    """批量处理器"""
    
    def __init__(self, config: Dict):
        self.batch_size = config.get("batch_size", 1000)
        self.parallel_workers = config.get("parallel_workers", 4)
    
    def process_batch_matching(
        self, 
        candidate_ids: List[str], 
        job_id: str
    ) -> List[Dict]:
        """
        批量处理匹配
        :param candidate_ids: 候选人ID列表
        :param job_id: 职位ID
        :return: 匹配结果列表
        """
        results = []
        
        # 分批处理
        for i in range(0, len(candidate_ids), self.batch_size):
            batch = candidate_ids[i:i + self.batch_size]
            
            # 并行处理每批数据
            batch_results = self._process_single_batch(batch, job_id)
            results.extend(batch_results)
        
        return results
    
    def _process_single_batch(
        self, 
        batch: List[str], 
        job_id: str
    ) -> List[Dict]:
        """处理单批数据"""
        
        # 获取候选人数据
        candidates = self._get_candidates_by_ids(batch)
        
        # 获取职位数据
        job = self._get_job_by_id(job_id)
        
        # 并行计算匹配度
        with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
            futures = [
                executor.submit(self._calculate_match_score, candidate, job)
                for candidate in candidates
            ]
            results = [f.result() for f in futures]
        
        return results
    
    def _calculate_match_score(self, candidate: Dict, job: Dict) -> Dict:
        """计算单个匹配度"""
        # 简化示例，实际实现更复杂
        skill_match = self._calculate_skill_match(
            candidate.get("skills", []),
            job.get("required_skills", [])
        )
        
        education_match = self._calculate_education_match(
            candidate.get("highest_education"),
            job.get("education_requirement")
        )
        
        return {
            "candidate_id": candidate["candidate_id"],
            "job_id": job["job_id"],
            "match_score": (skill_match * 0.7 + education_match * 0.3) * 100,
            "skill_match": skill_match * 100,
            "education_match": education_match * 100
        }
```

---

## 4. 实时处理架构

### 4.1 流处理架构设计

```python
# 流处理架构
stream_processing_architecture = {
    "kafka_config": {
        "brokers": ["kafka-1:9092", "kafka-2:9092", "kafka-3:9092"],
        "topics": {
            "candidate_events": {
                "partitions": 32,
                "replication_factor": 3,
                "retention_hours": 72
            },
            "job_events": {
                "partitions": 16,
                "replication_factor": 3,
                "retention_hours": 72
            },
            "alert_events": {
                "partitions": 8,
                "replication_factor": 3,
                "retention_hours": 168
            }
        },
        "consumer_groups": {
            "matching_engine": {
                "topics": ["candidate_events", "job_events"],
                "max_poll_records": 500
            },
            "analytics_engine": {
                "topics": ["candidate_events"],
                "max_poll_records": 1000
            },
            "alert_engine": {
                "topics": ["candidate_events", "job_events", "alert_events"],
                "max_poll_records": 100
            }
        }
    },
    
    "flink_config": {
        "checkpoint_interval": 60000,  # 毫秒
        "checkpoint_timeout": 300000,
        "state_backend": "rocksdb",
        "parallelism": {
            "matching_job": 4,
            "analytics_job": 2,
            "alert_job": 2
        }
    }
}
```

### 4.2 实时匹配引擎

```python
# 实时匹配引擎
class RealTimeMatchingEngine:
    """实时匹配引擎"""
    
    def __init__(self, kafka_config: Dict, es_config: Dict):
        self.kafka_consumer = KafkaConsumer(
            'candidate_events',
            'job_events',
            **kafka_config
        )
        self.es_client = Elasticsearch(es_config)
        self.match_cache = RedisClient()
    
    def start(self):
        """启动实时匹配引擎"""
        for message in self.kafka_consumer:
            event = self._parse_event(message)
            
            if event["type"] == "candidate_added":
                self._handle_new_candidate(event)
            elif event["type"] == "job_added":
                self._handle_new_job(event)
            elif event["type"] == "candidate_updated":
                self._handle_candidate_update(event)
    
    def _handle_new_candidate(self, event: Dict):
        """处理新候选人"""
        candidate = event["data"]
        
        # 查询相关职位
        relevant_jobs = self._find_relevant_jobs(candidate)
        
        # 实时计算匹配度
        for job in relevant_jobs:
            match_result = self._calculate_match(candidate, job)
            
            # 更新索引
            self._update_match_index(match_result)
            
            # 发送匹配通知
            if match_result["score"] >= 80:
                self._send_match_notification(candidate, job, match_result)
    
    def _handle_new_job(self, event: Dict):
        """处理新职位"""
        job = event["data"]
        
        # 查询相关候选人
        relevant_candidates = self._find_relevant_candidates(job)
        
        # 批量计算匹配度
        for candidate in relevant_candidates:
            match_result = self._calculate_match(candidate, job)
            
            # 更新索引
            self._update_match_index(match_result)
            
            # 发送匹配通知
            if match_result["score"] >= 80:
                self._send_match_notification(candidate, job, match_result)
    
    def _calculate_match(self, candidate: Dict, job: Dict) -> Dict:
        """计算匹配度"""
        # 简化匹配算法
        skill_match = self._match_skills(
            candidate.get("skills", []),
            job.get("required_skills", [])
        )
        
        education_match = self._match_education(
            candidate.get("highest_education"),
            job.get("education_requirement")
        )
        
        location_match = self._match_location(
            candidate.get("expected_location"),
            job.get("location")
        )
        
        score = (
            skill_match * 0.5 +
            education_match * 0.3 +
            location_match * 0.2
        ) * 100
        
        return {
            "candidate_id": candidate["candidate_id"],
            "job_id": job["job_id"],
            "score": score,
            "skill_match": skill_match * 100,
            "education_match": education_match * 100,
            "location_match": location_match * 100,
            "timestamp": datetime.now().isoformat()
        }
```

### 4.3 实时分析处理

```python
# 实时分析处理
class RealTimeAnalytics:
    """实时分析处理器"""
    
    def __init__(self, kafka_config: Dict):
        self.kafka_consumer = KafkaConsumer(
            'candidate_events',
            **kafka_config
        )
        self.metrics_aggregator = MetricsAggregator()
        self.alert_detector = AlertDetector()
    
    def process_stream(self):
        """处理数据流"""
        for message in self.kafka_consumer:
            event = self._parse_event(message)
            
            # 更新聚合指标
            self.metrics_aggregator.update(event)
            
            # 检测异常
            anomalies = self.alert_detector.detect(
                self.metrics_aggregator.get_current_metrics()
            )
            
            if anomalies:
                self._handle_anomalies(anomalies)
    
    def get_current_metrics(self) -> Dict:
        """获取当前指标"""
        return {
            "total_candidates": self.metrics_aggregator.get_total("candidates"),
            "active_jobs": self.metrics_aggregator.get_total("jobs"),
            "matches_today": self.metrics_aggregator.get_count("matches", "today"),
            "avg_match_score": self.metrics_aggregator.get_average("match_score"),
            "top_skills": self.metrics_aggregator.get_top("skills", 10),
            "top_locations": self.metrics_aggregator.get_top("locations", 5)
        }


class MetricsAggregator:
    """指标聚合器"""
    
    def __init__(self):
        self.counters = defaultdict(int)
        self.gauges = {}
        self.histograms = defaultdict(list)
        self.windows = {
            "1h": deque(maxlen=3600),
            "1d": deque(maxlen=86400)
        }
    
    def update(self, event: Dict):
        """更新指标"""
        event_type = event["type"]
        
        if event_type == "candidate_added":
            self.counters["candidates"] += 1
            self.counters["candidates_today"] += 1
            self._update_skill_metrics(event["data"].get("skills", []))
            self._update_location_metrics(event["data"].get("location"))
        
        elif event_type == "job_added":
            self.counters["jobs"] += 1
        
        elif event_type == "match_completed":
            self.counters["matches"] += 1
            self.histograms["match_scores"].append(event["data"]["score"])
    
    def get_total(self, metric: str) -> int:
        """获取总数"""
        return self.counters.get(metric, 0)
    
    def get_count(self, metric: str, window: str) -> int:
        """获取窗口内数量"""
        if window == "today":
            return self.counters.get(f"{metric}_today", 0)
        return self.counters.get(metric, 0)
    
    def get_average(self, metric: str) -> float:
        """获取平均值"""
        values = self.histograms.get(metric, [])
        return sum(values) / len(values) if values else 0
```

---

## 5. 缓存策略

### 5.1 多级缓存架构

```python
# 多级缓存配置
cache_config = {
    "l1_cache": {  # 本地内存缓存
        "type": "caffeine",  # Java
        "max_size": 10000,
        "ttl_seconds": 60
    },
    "l2_cache": {  # Redis缓存
        "type": "redis",
        "host": "redis-master",
        "port": 6379,
        "db": 0,
        "password": "xxx",
        "max_connections": 100,
        "ttl_seconds": 300
    },
    "l3_cache": {  # 数据库缓存
        "type": "database",
        "fallback": True
    },
    
    "cache_keys": {
        "candidate_detail": {
            "pattern": "candidate:{candidate_id}",
            "ttl": 600,
            "level": "l2"
        },
        "job_detail": {
            "pattern": "job:{job_id}",
            "ttl": 300,
            "level": "l2"
        },
        "search_results": {
            "pattern": "search:{hash}",
            "ttl": 60,
            "level": "l1"
        },
        "match_results": {
            "pattern": "match:{candidate_id}:{job_id}",
            "ttl": 1800,
            "level": "l2"
        },
        "analytics_summary": {
            "pattern": "analytics:{tenant_id}:{type}",
            "ttl": 3600,
            "level": "l2"
        }
    }
}
```

### 5.2 缓存策略实现

```python
# 缓存策略实现
class MultiLevelCache:
    """多级缓存"""
    
    def __init__(self, config: Dict):
        self.l1_cache = self._init_l1_cache(config["l1_cache"])
        self.l2_cache = self._init_l2_cache(config["l2_cache"])
    
    def get(self, key: str, level: str = "l1") -> Optional[Any]:
        """获取缓存"""
        if level == "l1":
            result = self.l1_cache.get(key)
            if result is not None:
                return result
        
        result = self.l2_cache.get(key)
        if result is not None and level == "l1":
            # 写入L1缓存
            self.l1_cache.set(key, result)
        
        return result
    
    def set(self, key: str, value: Any, ttl: int = None):
        """设置缓存"""
        self.l1_cache.set(key, value, ttl)
        self.l2_cache.set(key, value, ttl)
    
    def invalidate(self, key: str):
        """失效缓存"""
        self.l1_cache.delete(key)
        self.l2_cache.delete(key)
    
    def invalidate_pattern(self, pattern: str):
        """按模式失效"""
        # 失效L2中匹配的所有键
        keys = self.l2_cache.keys(pattern)
        for key in keys:
            self.l2_cache.delete(key)
            # 同步失效L1
            self.l1_cache.delete(key)
```

---

## 6. 性能监控

### 6.1 性能监控指标

```python
# 性能监控配置
monitoring_config = {
    "metrics": {
        "application": {
            "request_count": {"type": "counter"},
            "request_duration": {"type": "histogram", "buckets": [5, 10, 25, 50, 100, 250, 500, 1000]},
            "error_rate": {"type": "gauge"}
        },
        "database": {
            "query_count": {"type": "counter"},
            "query_duration": {"type": "histogram"},
            "connection_pool_usage": {"type": "gauge"},
            "slow_query_count": {"type": "counter"}
        },
        "cache": {
            "hit_rate": {"type": "gauge"},
            "miss_count": {"type": "counter"},
            "eviction_count": {"type": "counter"}
        },
        "system": {
            "cpu_usage": {"type": "gauge"},
            "memory_usage": {"type": "gauge"},
            "disk_io": {"type": "gauge"},
            "network_io": {"type": "gauge"}
        }
    },
    
    "alerting": {
        "latency_p99_threshold": 500,
        "error_rate_threshold": 0.01,
        "cpu_usage_threshold": 0.80,
        "memory_usage_threshold": 0.85
    },
    
    "exporters": {
        "prometheus": {
            "enabled": True,
            "port": 9090
        },
        "grafana": {
            "enabled": True,
            "dashboard_url": "http://grafana:3000"
        }
    }
}
```

### 6.2 性能优化建议

```python
# 性能优化建议生成
class PerformanceOptimizer:
    """性能优化器"""
    
    def analyze_and_suggest(self, metrics: Dict) -> List[Dict]:
        """分析指标并给出优化建议"""
        suggestions = []
        
        # 延迟分析
        if metrics.get("p99_latency", 0) > 500:
            suggestions.append({
                "category": "latency",
                "severity": "high",
                "issue": "P99延迟超过500ms",
                "suggestions": [
                    "检查慢查询，添加适当索引",
                    "启用查询结果缓存",
                    "考虑使用CDN加速静态资源",
                    "优化数据库连接池配置"
                ]
            })
        
        # 缓存命中率分析
        if metrics.get("cache_hit_rate", 1) < 0.8:
            suggestions.append({
                "category": "cache",
                "severity": "medium",
                "issue": "缓存命中率低于80%",
                "suggestions": [
                    "增加缓存容量",
                    "调整缓存键设计策略",
                    "检查缓存过期时间是否合理",
                    "考虑使用本地缓存热点数据"
                ]
            })
        
        # 数据库分析
        slow_queries = metrics.get("slow_query_count", 0)
        if slow_queries > 10:
            suggestions.append({
                "category": "database",
                "severity": "high",
                "issue": f"慢查询数量过多（{slow_queries}）",
                "suggestions": [
                    "分析并优化慢查询SQL",
                    "添加或调整相关索引",
                    "考虑使用读写分离",
                    "评估是否需要分库分表"
                ]
            })
        
        return suggestions
```
