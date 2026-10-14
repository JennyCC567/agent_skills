#!/usr/bin/env python3
"""
技能知识图谱模块（Phase 3 增强）

功能：
1. 构建技能之间的关联关系图谱（分类树、依赖关系、等价关系）
2. 提供技能关联查询和技能距离计算
3. 在 talent_matcher.py 中调用：当候选人技能与JD技能不完全匹配时，通过图谱查找关联技能给予部分加分
4. 可视化输出：将技能图谱关系导出为JSON格式（节点+边），供报告生成器使用

纯Python实现，不依赖外部图谱库（如networkx），用标准库dict/list实现
"""

import json
import argparse
from typing import Dict, List, Any, Set, Tuple, Optional
from collections import defaultdict, deque


class SkillGraph:
    """技能知识图谱"""

    # =====================================================================
    # 技能分类树：领域 -> 子领域 -> 具体技能
    # =====================================================================
    SKILL_TAXONOMY = {
        "AI/ML": {
            "深度学习": {
                "PyTorch", "TensorFlow", "Keras", "JAX", "PaddlePaddle",
                "模型蒸馏", "模型量化", "模型剪枝", "分布式训练", "模型优化"
            },
            "NLP": {
                "NLP", "文本分类", "命名实体识别", "机器翻译", "情感分析",
                "问答系统", "文本生成"
            },
            "LLM": {
                "大模型", "LLM", "LangChain", "RAG", "Prompt Engineering",
                "Function Calling", "Agent开发", "向量数据库",
                "提示工程", "检索增强生成", "微调", "RLHF", "对齐"
            },
            "计算机视觉": {
                "Computer Vision", "CV", "YOLO", "OpenCV", "目标检测",
                "图像分割", "图像分类", "人脸识别"
            },
            "强化学习": {
                "强化学习", "Reinforcement Learning", "RLHF",
                "多智能体", "博弈论"
            },
            "机器学习基础": {
                "机器学习", "Machine Learning", "scikit-learn",
                "特征工程", "模型评估", "XGBoost", "LightGBM"
            }
        },
        "工程/运维": {
            "后端开发": {
                "Python", "Java", "Go", "C++", "Rust", "Spring Boot",
                "FastAPI", "Django", "Flask"
            },
            "云原生/DevOps": {
                "Docker", "Kubernetes", "容器化", "容器编排",
                "CI/CD", "持续集成", "MLOps", "机器学习运维",
                "TensorFlow Serving", "模型部署"
            },
            "数据工程": {
                "Spark", "Flink", "Kafka", "Hadoop", "数据仓库",
                "ETL", "数据治理"
            }
        },
        "管理/规划": {
            "技术管理": {
                "团队管理", "项目管理", "技术规划", "AI架构设计",
                "技术专家", "首席科学家"
            }
        }
    }

    # =====================================================================
    # 技能等价关系（双向映射）
    # =====================================================================
    SKILL_EQUIVALENCES = [
        {"大模型", "LLM", "Large Language Model"},
        {"分布式训练", "Distributed Training"},
        {"模型优化", "Model Optimization"},
        {"机器学习", "Machine Learning"},
        {"深度学习", "Deep Learning"},
        {"计算机视觉", "Computer Vision", "CV"},
        {"自然语言处理", "NLP", "Natural Language Processing"},
        {"提示工程", "Prompt Engineering"},
        {"检索增强生成", "RAG", "Retrieval Augmented Generation"},
        {"容器化", "Docker"},
        {"容器编排", "Kubernetes", "K8s"},
        {"持续集成", "CI/CD"},
        {"机器学习运维", "MLOps"},
        {"API框架", "FastAPI"},
        {"推理优化", "TensorRT"},
        {"目标检测", "YOLO"},
        {"计算机视觉库", "OpenCV"},
        {"强化学习", "Reinforcement Learning", "RL"},
    ]

    # =====================================================================
    # 技能依赖关系：A 依赖 B（掌握A通常需要先掌握B）
    # =====================================================================
    SKILL_DEPENDENCIES = [
        # 深度学习框架依赖
        {"skill": "分布式训练", "depends_on": ["PyTorch", "CUDA"]},
        {"skill": "分布式训练", "depends_on": ["TensorFlow"]},
        {"skill": "模型蒸馏", "depends_on": ["PyTorch"]},
        {"skill": "模型量化", "depends_on": ["PyTorch"]},
        {"skill": "模型剪枝", "depends_on": ["PyTorch"]},
        {"skill": "模型优化", "depends_on": ["深度学习"]},
        # LLM 相关依赖
        {"skill": "大模型", "depends_on": ["NLP", "深度学习"]},
        {"skill": "LangChain", "depends_on": ["大模型", "Python"]},
        {"skill": "RAG", "depends_on": ["大模型", "向量数据库"]},
        {"skill": "Agent开发", "depends_on": ["大模型", "Function Calling"]},
        {"skill": "Prompt Engineering", "depends_on": ["大模型"]},
        {"skill": "微调", "depends_on": ["大模型", "PyTorch"]},
        {"skill": "RLHF", "depends_on": ["大模型", "强化学习"]},
        # NLP 依赖
        {"skill": "NLP", "depends_on": ["机器学习", "Python"]},
        {"skill": "文本生成", "depends_on": ["NLP"]},
        {"skill": "问答系统", "depends_on": ["NLP"]},
        # CV 依赖
        {"skill": "Computer Vision", "depends_on": ["深度学习"]},
        {"skill": "YOLO", "depends_on": ["PyTorch", "Computer Vision"]},
        {"skill": "OpenCV", "depends_on": ["Python"]},
        # 部署/运维依赖
        {"skill": "模型部署", "depends_on": ["Docker"]},
        {"skill": "TensorFlow Serving", "depends_on": ["TensorFlow"]},
        {"skill": "MLOps", "depends_on": ["Docker", "Kubernetes"]},
        # 管理依赖
        {"skill": "AI架构设计", "depends_on": ["大模型", "分布式训练"]},
        {"skill": "技术规划", "depends_on": ["团队管理"]},
    ]

    # =====================================================================
    # 技能关联强度（0-1）：非直接等价但有相关性
    # =====================================================================
    SKILL_AFFINITIES = [
        {"skill_a": "PyTorch", "skill_b": "TensorFlow", "strength": 0.7},
        {"skill_a": "NLP", "skill_b": "大模型", "strength": 0.85},
        {"skill_a": "大模型", "skill_b": "Prompt Engineering", "strength": 0.8},
        {"skill_a": "大模型", "skill_b": "RAG", "strength": 0.8},
        {"skill_a": "大模型", "skill_b": "LangChain", "strength": 0.75},
        {"skill_a": "大模型", "skill_b": "分布式训练", "strength": 0.7},
        {"skill_a": "大模型", "skill_b": "强化学习", "strength": 0.6},
        {"skill_a": "深度学习", "skill_b": "PyTorch", "strength": 0.8},
        {"skill_a": "深度学习", "skill_b": "TensorFlow", "strength": 0.8},
        {"skill_a": "Computer Vision", "skill_b": "YOLO", "strength": 0.75},
        {"skill_a": "Computer Vision", "skill_b": "OpenCV", "strength": 0.7},
        {"skill_a": "Docker", "skill_b": "Kubernetes", "strength": 0.7},
        {"skill_a": "模型部署", "skill_b": "Docker", "strength": 0.65},
        {"skill_a": "模型优化", "skill_b": "TensorRT", "strength": 0.7},
        {"skill_a": "NLP", "skill_b": "文本生成", "strength": 0.75},
        {"skill_a": "Python", "skill_b": "FastAPI", "strength": 0.6},
        {"skill_a": "Python", "skill_b": "PyTorch", "strength": 0.6},
        {"skill_a": "分布式训练", "skill_b": "CUDA", "strength": 0.65},
    ]

    def __init__(self):
        """初始化技能知识图谱"""
        self.nodes: Dict[str, Dict[str, Any]] = {}  # skill_name -> node_info
        self.edges: List[Dict[str, Any]] = []  # edge list
        self._equivalence_groups: List[Set[str]] = []  # 等价组列表
        self._equivalence_map: Dict[str, Set[str]] = {}  # skill -> set of equivalent skills
        self._affinity_map: Dict[str, Dict[str, float]] = defaultdict(dict)  # skill -> {related_skill: strength}
        self._dependency_map: Dict[str, List[str]] = defaultdict(list)  # skill -> list of dependencies
        self._taxonomy_map: Dict[str, str] = {}  # skill -> category path

        self._build_graph()

    def _normalize_skill_name(self, skill: str) -> str:
        """技能名称归一化"""
        return skill.strip()

    def _build_graph(self):
        """构建完整的技能知识图谱"""
        # 1. 构建分类树
        for domain, sub_domains in self.SKILL_TAXONOMY.items():
            self._add_node(domain, {"type": "domain", "category": domain})
            for sub_domain, skills in sub_domains.items():
                self._add_node(sub_domain, {"type": "sub_domain", "category": domain})
                self._add_edge(domain, sub_domain, "contains", 1.0)
                for skill in skills:
                    self._add_node(skill, {"type": "skill", "category": domain, "sub_category": sub_domain})
                    self._add_edge(sub_domain, skill, "contains", 1.0)
                    self._taxonomy_map[skill.lower()] = f"{domain}/{sub_domain}"

        # 2. 构建等价关系
        for group in self.SKILL_EQUIVALENCES:
            normalized_group = set(self._normalize_skill_name(s) for s in group)
            self._equivalence_groups.append(normalized_group)
            for skill in normalized_group:
                self._add_node(skill, {"type": "skill"})
                self._equivalence_map[skill] = normalized_group - {skill}
            # 添加等价边
            for skill_a in normalized_group:
                for skill_b in normalized_group:
                    if skill_a != skill_b:
                        self._add_edge(skill_a, skill_b, "equivalent", 1.0)

        # 3. 构建依赖关系
        for dep in self.SKILL_DEPENDENCIES:
            skill = self._normalize_skill_name(dep["skill"])
            self._add_node(skill, {"type": "skill"})
            for dependency in dep["depends_on"]:
                dependency = self._normalize_skill_name(dependency)
                self._add_node(dependency, {"type": "skill"})
                self._add_edge(skill, dependency, "depends_on", 0.9)
                self._dependency_map[skill].append(dependency)

        # 4. 构建关联关系（affinity）
        for aff in self.SKILL_AFFINITIES:
            skill_a = self._normalize_skill_name(aff["skill_a"])
            skill_b = self._normalize_skill_name(aff["skill_b"])
            strength = aff["strength"]
            self._add_node(skill_a, {"type": "skill"})
            self._add_node(skill_b, {"type": "skill"})
            self._add_edge(skill_a, skill_b, "affinity", strength)
            self._affinity_map[skill_a][skill_b] = strength
            self._affinity_map[skill_b][skill_a] = strength

    def _add_node(self, name: str, attributes: Dict[str, Any] = None):
        """添加技能节点"""
        name = self._normalize_skill_name(name)
        if name not in self.nodes:
            self.nodes[name] = {"name": name, "attributes": attributes or {}}
        else:
            if attributes:
                self.nodes[name]["attributes"].update(attributes)

    def _add_edge(self, source: str, target: str, relation: str, weight: float = 1.0):
        """添加边（关系）"""
        source = self._normalize_skill_name(source)
        target = self._normalize_skill_name(target)
        # 避免重复边
        for edge in self.edges:
            if (edge["source"] == source and edge["target"] == target
                    and edge["relation"] == relation):
                return
        self.edges.append({
            "source": source,
            "target": target,
            "relation": relation,
            "weight": weight
        })

    # =====================================================================
    # 公共 API
    # =====================================================================

    def add_skill_node(self, name: str, attributes: Dict[str, Any] = None):
        """添加技能节点"""
        self._add_node(name, attributes or {"type": "custom_skill"})

    def define_relation(self, source: str, target: str, relation: str, weight: float = 1.0):
        """
        定义技能关系

        Args:
            source: 源技能
            target: 目标技能
            relation: 关系类型（equivalent/depends_on/affinity/contains）
            weight: 关系权重 (0-1)
        """
        self._add_node(source, {"type": "skill"})
        self._add_node(target, {"type": "skill"})
        self._add_edge(source, target, relation, weight)

        if relation == "equivalent":
            if source not in self._equivalence_map:
                self._equivalence_map[source] = set()
            if target not in self._equivalence_map:
                self._equivalence_map[target] = set()
            self._equivalence_map[source].add(target)
            self._equivalence_map[target].add(source)
        elif relation == "affinity":
            self._affinity_map[source][target] = weight
            self._affinity_map[target][source] = weight
        elif relation == "depends_on":
            self._dependency_map[source].append(target)

    def get_equivalent_skills(self, skill: str) -> Set[str]:
        """获取等价技能"""
        skill = self._normalize_skill_name(skill)
        return self._equivalence_map.get(skill, set())

    def is_equivalent(self, skill_a: str, skill_b: str) -> bool:
        """判断两个技能是否等价"""
        skill_a = self._normalize_skill_name(skill_a)
        skill_b = self._normalize_skill_name(skill_b)
        return skill_b in self._equivalence_map.get(skill_a, set())

    def get_related_skills(self, skill: str, max_depth: int = 2, min_strength: float = 0.3) -> Dict[str, float]:
        """
        查询关联技能（BFS遍历，返回关联技能及其关联强度）

        Args:
            skill: 目标技能
            max_depth: 最大搜索深度
            min_strength: 最小关联强度阈值

        Returns:
            {related_skill: strength} 字典
        """
        skill = self._normalize_skill_name(skill)
        result = {}

        # 1. 等价技能（强度=1.0）
        for equiv in self.get_equivalent_skills(skill):
            result[equiv] = 1.0

        # 2. 直接关联技能
        if skill in self._affinity_map:
            for related, strength in self._affinity_map[skill].items():
                if strength >= min_strength:
                    result[related] = max(result.get(related, 0), strength)

        # 3. 深度搜索（BFS）
        if max_depth > 1:
            visited = {skill}
            queue = deque([(skill, 0)])
            while queue:
                current, depth = queue.popleft()
                if depth >= max_depth:
                    continue
                # 通过关联边扩展
                if current in self._affinity_map:
                    for neighbor, strength in self._affinity_map[current].items():
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append((neighbor, depth + 1))
                            # 衰减强度
                            decayed_strength = strength * (0.6 ** depth)
                            if decayed_strength >= min_strength:
                                result[neighbor] = max(result.get(neighbor, 0), decayed_strength)
                # 通过等价边扩展
                for equiv in self.get_equivalent_skills(current):
                    if equiv not in visited:
                        visited.add(equiv)
                        queue.append((equiv, depth + 1))
                        # 等价技能衰减更慢
                        decayed = 0.9 ** (depth + 1)
                        if decayed >= min_strength:
                            result[equiv] = max(result.get(equiv, 0), decayed)

        # 移除自身
        result.pop(skill, None)
        return result

    def calculate_skill_distance(self, skill_a: str, skill_b: str) -> float:
        """
        计算两个技能之间的距离（0=完全相同/等价，1=无关联）

        基于图谱中最短路径的边权重计算：
        distance = 1 - max_path_strength

        Args:
            skill_a: 技能A
            skill_b: 技能B

        Returns:
            技能距离 (0-1)
        """
        skill_a = self._normalize_skill_name(skill_a)
        skill_b = self._normalize_skill_name(skill_b)

        if skill_a == skill_b:
            return 0.0

        # 等价技能距离为0
        if self.is_equivalent(skill_a, skill_b):
            return 0.0

        # BFS搜索最强路径
        visited = {skill_a: 1.0}  # skill -> best_strength_to_reach
        queue = deque([skill_a])

        while queue:
            current = queue.popleft()
            current_strength = visited[current]

            if current == skill_b:
                return 1.0 - current_strength

            # 通过关联边
            if current in self._affinity_map:
                for neighbor, edge_strength in self._affinity_map[current].items():
                    path_strength = current_strength * edge_strength
                    if neighbor == skill_b:
                        return 1.0 - max(path_strength, visited.get(skill_b, 0))
                    if path_strength > visited.get(neighbor, 0):
                        visited[neighbor] = path_strength
                        queue.append(neighbor)

            # 通过等价边
            for equiv in self.get_equivalent_skills(current):
                path_strength = current_strength * 1.0  # 等价边权重=1
                if equiv == skill_b:
                    return 0.0
                if path_strength > visited.get(equiv, 0):
                    visited[equiv] = path_strength
                    queue.append(equiv)

        return 1.0  # 无路径

    def calculate_skill_bonus(self, job_skills: List[str], candidate_skills: List[str],
                              max_bonus: float = 0.15) -> Tuple[float, Dict[str, Any]]:
        """
        计算技能关联加分

        当候选人技能与JD技能不完全匹配时，通过图谱查找关联技能给予部分加分

        Args:
            job_skills: 岗位要求的技能列表
            candidate_skills: 候选人拥有的技能列表
            max_bonus: 最大加分值 (0-1)

        Returns:
            (加分数值, 加分详情字典)
        """
        job_set = set(self._normalize_skill_name(s) for s in job_skills)
        cand_set = set(self._normalize_skill_name(s) for s in candidate_skills)

        # 直接匹配的技能
        direct_match = job_set & cand_set
        # 未直接匹配的JD技能
        unmatched_job_skills = job_set - direct_match

        if not unmatched_job_skills:
            return 0.0, {"bonus": 0.0, "details": [], "message": "所有JD技能已直接匹配"}

        bonus = 0.0
        details = []

        for job_skill in unmatched_job_skills:
            best_related = None
            best_strength = 0.0

            for cand_skill in cand_set:
                # 检查等价
                if self.is_equivalent(job_skill, cand_skill):
                    best_related = cand_skill
                    best_strength = 1.0
                    break

                # 检查关联
                related = self.get_related_skills(cand_skill, max_depth=2, min_strength=0.3)
                if job_skill in related:
                    strength = related[job_skill]
                    if strength > best_strength:
                        best_strength = strength
                        best_related = cand_skill

            if best_related and best_strength > 0:
                # 加分 = 关联强度 * max_bonus * (技能在JD中的权重)
                skill_bonus = best_strength * max_bonus / len(job_set)
                bonus += skill_bonus
                details.append({
                    "job_skill": job_skill,
                    "matched_via": best_related,
                    "relation_strength": round(best_strength, 4),
                    "bonus_points": round(skill_bonus * 100, 2)
                })

        bonus = min(bonus, max_bonus)

        return round(bonus, 4), {
            "bonus": round(bonus, 4),
            "details": details,
            "message": f"通过技能图谱关联匹配，额外加分 {round(bonus * 100, 2)} 分"
        }

    def get_skill_category(self, skill: str) -> Optional[str]:
        """获取技能所属分类"""
        skill = self._normalize_skill_name(skill)
        return self._taxonomy_map.get(skill.lower())

    def get_skill_dependencies(self, skill: str) -> List[str]:
        """获取技能的前置依赖"""
        skill = self._normalize_skill_name(skill)
        return self._dependency_map.get(skill, [])

    def export_graph_json(self) -> Dict[str, Any]:
        """
        导出技能图谱为JSON格式（节点+边），供报告生成器使用

        Returns:
            {"nodes": [...], "edges": [...], "metadata": {...}}
        """
        nodes = []
        for name, info in self.nodes.items():
            node = {
                "id": name,
                "label": name,
                "type": info["attributes"].get("type", "skill"),
                "category": info["attributes"].get("category", ""),
                "sub_category": info["attributes"].get("sub_category", "")
            }
            nodes.append(node)

        edges = []
        for edge in self.edges:
            edges.append({
                "source": edge["source"],
                "target": edge["target"],
                "relation": edge["relation"],
                "weight": edge["weight"]
            })

        return {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "equivalence_groups": len(self._equivalence_groups),
                "affinity_pairs": sum(len(v) for v in self._affinity_map.values()) // 2,
                "dependency_relations": sum(len(v) for v in self._dependency_map.values())
            }
        }

    def get_graph_summary(self) -> Dict[str, Any]:
        """获取图谱摘要信息"""
        categories = defaultdict(int)
        for node_info in self.nodes.values():
            cat = node_info["attributes"].get("type", "unknown")
            categories[cat] += 1

        relation_counts = defaultdict(int)
        for edge in self.edges:
            relation_counts[edge["relation"]] += 1

        return {
            "total_skills": len(self.nodes),
            "total_relations": len(self.edges),
            "node_type_distribution": dict(categories),
            "relation_type_distribution": dict(relation_counts),
            "equivalence_groups": len(self._equivalence_groups),
            "taxonomy_domains": list(self.SKILL_TAXONOMY.keys())
        }


# =====================================================================
# 独立运行入口
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description='技能知识图谱（Phase 3）')
    parser.add_argument('--export', help='导出图谱JSON到指定路径')
    parser.add_argument('--query', help='查询指定技能的关联技能')
    parser.add_argument('--distance', nargs=2, metavar=('SKILL_A', 'SKILL_B'),
                        help='计算两个技能之间的距离')
    parser.add_argument('--bonus', nargs=2, metavar=('JOB_SKILLS', 'CAND_SKILLS'),
                        help='计算技能关联加分（逗号分隔技能列表）')

    args = parser.parse_args()

    graph = SkillGraph()

    # 打印图谱摘要
    summary = graph.get_graph_summary()
    print("=" * 60)
    print("技能知识图谱摘要")
    print("=" * 60)
    print(f"  技能节点总数: {summary['total_skills']}")
    print(f"  关系边总数: {summary['total_relations']}")
    print(f"  等价组数量: {summary['equivalence_groups']}")
    print(f"  分类领域: {', '.join(summary['taxonomy_domains'])}")
    print(f"\n  节点类型分布:")
    for t, count in summary['node_type_distribution'].items():
        print(f"    {t}: {count}")
    print(f"\n  关系类型分布:")
    for r, count in summary['relation_type_distribution'].items():
        print(f"    {r}: {count}")

    # 查询关联技能
    if args.query:
        print(f"\n{'=' * 60}")
        print(f"查询技能 [{args.query}] 的关联技能")
        print("=" * 60)
        related = graph.get_related_skills(args.query, max_depth=2, min_strength=0.3)
        equiv = graph.get_equivalent_skills(args.query)
        deps = graph.get_skill_dependencies(args.query)
        category = graph.get_skill_category(args.query)

        print(f"  分类: {category or '未分类'}")
        print(f"  等价技能: {', '.join(equiv) if equiv else '无'}")
        print(f"  依赖技能: {', '.join(deps) if deps else '无'}")
        print(f"  关联技能:")
        if related:
            for skill, strength in sorted(related.items(), key=lambda x: x[1], reverse=True):
                print(f"    {skill}: 关联强度={strength:.2f}")
        else:
            print("    无关联技能")

    # 计算技能距离
    if args.distance:
        skill_a, skill_b = args.distance
        distance = graph.calculate_skill_distance(skill_a, skill_b)
        print(f"\n{'=' * 60}")
        print(f"技能距离计算: [{skill_a}] <-> [{skill_b}]")
        print("=" * 60)
        print(f"  距离: {distance:.4f} (0=完全相同/等价, 1=无关联)")

    # 计算技能关联加分
    if args.bonus:
        job_skills = [s.strip() for s in args.bonus[0].split(',')]
        cand_skills = [s.strip() for s in args.bonus[1].split(',')]
        bonus, details = graph.calculate_skill_bonus(job_skills, cand_skills)
        print(f"\n{'=' * 60}")
        print("技能关联加分计算")
        print("=" * 60)
        print(f"  JD技能: {', '.join(job_skills)}")
        print(f"  候选人技能: {', '.join(cand_skills)}")
        print(f"  关联加分: {details['bonus'] * 100:.2f} 分")
        print(f"  {details['message']}")
        if details['details']:
            print(f"\n  关联详情:")
            for d in details['details']:
                print(f"    JD技能 [{d['job_skill']}] <- 关联匹配 <- 候选人技能 [{d['matched_via']}]")
                print(f"      关联强度: {d['relation_strength']}, 加分: {d['bonus_points']}")

    # 导出图谱
    if args.export:
        graph_data = graph.export_graph_json()
        with open(args.export, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
        print(f"\n{'=' * 60}")
        print(f"图谱已导出到: {args.export}")
        print(f"  节点数: {graph_data['metadata']['total_nodes']}")
        print(f"  边数: {graph_data['metadata']['total_edges']}")
        print("=" * 60)
    else:
        # 默认导出到标准输出
        graph_data = graph.export_graph_json()
        print(f"\n{'=' * 60}")
        print("图谱JSON数据（前5个节点和前5条边预览）")
        print("=" * 60)
        print(f"  节点示例: {json.dumps(graph_data['nodes'][:5], ensure_ascii=False)}")
        print(f"  边示例: {json.dumps(graph_data['edges'][:5], ensure_ascii=False)}")

    print("\n技能知识图谱构建完成!")


if __name__ == "__main__":
    main()
