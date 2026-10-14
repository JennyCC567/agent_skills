#!/usr/bin/env python3
"""
交互式查询引擎（Phase 3 增强）

功能：
1. 对已生成的匹配结果提供交互式查询能力：
   - 按条件筛选：filter(skill="PyTorch", min_score=60, location="北京")
   - 按维度排序：sort_by("potential_score", descending=True)
   - 统计聚合：aggregate(by="company") → 每家公司候选人数量和平均分
   - 对比分析：compare(candidate_ids=["T001", "T002"]) → 两位候选人维度对比
2. 提供 QueryEngine 类，接收匹配结果列表，返回查询结果
3. 支持链式调用：engine.filter(...).sort_by(...).aggregate(...)
4. 导出查询结果为JSON/CSV格式

纯Python实现，查询结果可被report_generator.py使用生成分析报告
"""

import json
import csv
import argparse
from typing import Dict, List, Any, Optional, Union
from collections import defaultdict


class QueryEngine:
    """交互式查询引擎（支持链式调用）"""

    def __init__(self, results: List[Dict[str, Any]] = None):
        """
        初始化查询引擎

        Args:
            results: 匹配结果列表
        """
        self._original_results = results or []
        self._results = list(self._original_results)  # 当前工作集（可被链式操作修改）

    def _get_candidate_field(self, candidate: Dict[str, Any], field: str, default: Any = None) -> Any:
        """从候选人数据中获取字段值（支持嵌套profile）"""
        # 直接从结果中获取
        if field in candidate:
            return candidate[field]

        # 从 profile 中获取
        profile = candidate.get("profile", {})
        if field in profile:
            return profile[field]

        # 从 scores 中获取
        scores = candidate.get("scores", {})
        if field in scores:
            return scores[field]

        # 从 potential_subscores 中获取
        potential_subscores = candidate.get("potential_subscores", {})
        if field in potential_subscores:
            return potential_subscores[field]

        # 特殊字段映射
        field_mappings = {
            "score": candidate.get("total_score", default),
            "match_score": candidate.get("total_score", default),
            "total_score": candidate.get("total_score", default),
            "name": candidate.get("candidate_name", profile.get("name", default)),
            "id": candidate.get("candidate_id", profile.get("id", default)),
            "location": profile.get("current_location", default),
            "company": self._get_current_company(candidate),
            "skills": profile.get("skills", candidate.get("skills", [])),
            "experience_years": profile.get("experience_years", default),
            "education_level": profile.get("education_level", default),
            "employment_status": profile.get("employment_status", default),
        }

        return field_mappings.get(field, default)

    def _get_current_company(self, candidate: Dict[str, Any]) -> str:
        """获取当前公司"""
        profile = candidate.get("profile", candidate)
        work_exp = profile.get("work_experience", [])
        if work_exp:
            return work_exp[-1].get("company", "")
        return profile.get("current_company", "")

    def _clone(self, results: List[Dict[str, Any]]) -> 'QueryEngine':
        """创建一个新的QueryEngine实例（用于链式调用）"""
        new_engine = QueryEngine.__new__(QueryEngine)
        new_engine._original_results = self._original_results
        new_engine._results = results
        return new_engine

    # =====================================================================
    # 查询操作
    # =====================================================================

    def filter(self, skill: str = None, min_score: float = None, max_score: float = None,
               location: str = None, company: str = None, employment_status: str = None,
               min_experience: int = None, education_level: str = None,
               candidate_id: str = None) -> 'QueryEngine':
        """
        按条件筛选候选人

        Args:
            skill: 技能筛选（候选人拥有该技能即匹配，支持部分匹配）
            min_score: 最低匹配分数
            max_score: 最高匹配分数
            location: 地域筛选（支持部分匹配）
            company: 公司筛选（支持部分匹配）
            employment_status: 在职状态筛选
            min_experience: 最低工作年限
            education_level: 学历筛选
            candidate_id: 候选人ID筛选

        Returns:
            新的QueryEngine实例（支持链式调用）
        """
        filtered = []

        for candidate in self._results:
            # 技能筛选
            if skill:
                skills = self._get_candidate_field(candidate, "skills", [])
                if isinstance(skills, str):
                    skills = [s.strip() for s in skills.split(",")]
                skill_lower = skill.lower()
                skills_lower = [s.lower() for s in skills]
                if not any(skill_lower in s for s in skills_lower):
                    continue

            # 分数筛选
            score = self._get_candidate_field(candidate, "total_score", 0)
            if min_score is not None and score < min_score:
                continue
            if max_score is not None and score > max_score:
                continue

            # 地域筛选
            if location:
                cand_loc = self._get_candidate_field(candidate, "location", "")
                if location.lower() not in str(cand_loc).lower():
                    continue

            # 公司筛选
            if company:
                cand_company = self._get_current_company(candidate)
                if company.lower() not in str(cand_company).lower():
                    continue

            # 在职状态筛选
            if employment_status:
                cand_status = self._get_candidate_field(candidate, "employment_status", "")
                if employment_status.lower() != str(cand_status).lower():
                    continue

            # 经验年限筛选
            if min_experience is not None:
                exp = self._get_candidate_field(candidate, "experience_years", 0)
                if exp < min_experience:
                    continue

            # 学历筛选
            if education_level:
                cand_edu = self._get_candidate_field(candidate, "education_level", "")
                if education_level.lower() != str(cand_edu).lower():
                    continue

            # ID筛选
            if candidate_id:
                cand_id = self._get_candidate_field(candidate, "id", "")
                if candidate_id != str(cand_id):
                    continue

            filtered.append(candidate)

        return self._clone(filtered)

    def sort_by(self, field: str, descending: bool = True) -> 'QueryEngine':
        """
        按维度排序

        Args:
            field: 排序字段（total_score, skill, experience, education, potential, potential_subscores字段等）
            descending: 是否降序

        Returns:
            新的QueryEngine实例
        """
        def sort_key(candidate):
            value = self._get_candidate_field(candidate, field, 0)
            # 处理None值
            if value is None:
                return 0 if not descending else 0
            return value

        sorted_results = sorted(self._results, key=sort_key, reverse=descending)
        return self._clone(sorted_results)

    def aggregate(self, by: str) -> Dict[str, Any]:
        """
        统计聚合

        Args:
            by: 聚合维度（company, location, education_level, employment_status）

        Returns:
            聚合结果字典 {group_key: {count, avg_score, max_score, min_score, candidates}}
        """
        groups = defaultdict(list)

        for candidate in self._results:
            if by == "company":
                key = self._get_current_company(candidate) or "未知"
            elif by == "location":
                key = self._get_candidate_field(candidate, "location", "未知") or "未知"
            else:
                key = str(self._get_candidate_field(candidate, by, "未知"))

            groups[key].append(candidate)

        result = {}
        for key, candidates in groups.items():
            scores = [self._get_candidate_field(c, "total_score", 0) for c in candidates]
            result[key] = {
                "count": len(candidates),
                "avg_score": round(sum(scores) / len(scores), 2) if scores else 0,
                "max_score": round(max(scores), 2) if scores else 0,
                "min_score": round(min(scores), 2) if scores else 0,
                "candidates": [self._get_candidate_field(c, "name", "") for c in candidates]
            }

        return result

    def compare(self, candidate_ids: List[str]) -> Dict[str, Any]:
        """
        候选人对比分析

        Args:
            candidate_ids: 候选人ID列表

        Returns:
            对比分析结果
        """
        candidates_to_compare = []
        for cid in candidate_ids:
            for c in self._results:
                c_id = self._get_candidate_field(c, "id", "")
                if str(c_id) == str(cid):
                    candidates_to_compare.append(c)
                    break

        if len(candidates_to_compare) < 2:
            return {
                "error": "需要至少2个候选人进行对比",
                "found": len(candidates_to_compare),
                "requested": len(candidate_ids)
            }

        # 构建对比维度
        dimensions = {
            "total_score": "综合匹配分",
            "skill": "技能匹配",
            "experience": "经验匹配",
            "education": "学历匹配",
            "potential": "潜力评分"
        }

        comparison = {
            "candidates": [],
            "dimensions": {},
            "winner_by_dimension": {},
            "overall_winner": None,
            "analysis": ""
        }

        # 收集各候选人信息
        for c in candidates_to_compare:
            scores = c.get("scores", {})
            comparison["candidates"].append({
                "id": self._get_candidate_field(c, "id", ""),
                "name": self._get_candidate_field(c, "name", ""),
                "total_score": self._get_candidate_field(c, "total_score", 0),
                "scores": scores,
                "skills": self._get_candidate_field(c, "skills", []),
                "experience_years": self._get_candidate_field(c, "experience_years", 0),
                "location": self._get_candidate_field(c, "location", ""),
                "current_company": self._get_current_company(c),
                "education_level": self._get_candidate_field(c, "education_level", ""),
            })

        # 逐维度对比
        for dim_key, dim_label in dimensions.items():
            values = {}
            for c in candidates_to_compare:
                name = self._get_candidate_field(c, "name", "Unknown")
                if dim_key == "total_score":
                    values[name] = self._get_candidate_field(c, "total_score", 0)
                else:
                    scores = c.get("scores", {})
                    values[name] = scores.get(dim_key, 0)

            comparison["dimensions"][dim_key] = {
                "label": dim_label,
                "values": values,
                "max": max(values.values()) if values else 0,
                "min": min(values.values()) if values else 0,
                "range": round(max(values.values()) - min(values.values()), 2) if values else 0
            }

            # 找出该维度最高分的候选人
            if values:
                winner = max(values, key=values.get)
                comparison["winner_by_dimension"][dim_key] = {
                    "name": winner,
                    "score": values[winner]
                }

        # 综合最优
        total_scores = {c["name"]: c["total_score"] for c in comparison["candidates"]}
        if total_scores:
            overall_winner = max(total_scores, key=total_scores.get)
            comparison["overall_winner"] = {
                "name": overall_winner,
                "score": total_scores[overall_winner]
            }

        # 生成分析文本
        analysis_parts = []
        names = [c["name"] for c in comparison["candidates"]]
        analysis_parts.append(f"对比候选人: {', '.join(names)}")

        if comparison["overall_winner"]:
            winner = comparison["overall_winner"]
            analysis_parts.append(f"综合最优: {winner['name']}（{winner['score']}分）")

        for dim_key, dim_info in comparison["dimensions"].items():
            winner = comparison["winner_by_dimension"].get(dim_key)
            if winner:
                analysis_parts.append(f"  {dim_info['label']}: {winner['name']}领先（{winner['score']}分）")

        comparison["analysis"] = "\n".join(analysis_parts)

        return comparison

    def top(self, n: int = 5) -> 'QueryEngine':
        """获取前N个候选人"""
        return self._clone(self._results[:n])

    def count(self) -> int:
        """返回当前结果数量"""
        return len(self._results)

    def get_results(self) -> List[Dict[str, Any]]:
        """获取当前查询结果"""
        return self._results

    def get_summary(self) -> Dict[str, Any]:
        """获取当前结果的统计摘要"""
        if not self._results:
            return {"count": 0, "message": "无匹配结果"}

        scores = [self._get_candidate_field(c, "total_score", 0) for c in self._results]
        all_skills = set()
        locations = set()
        companies = set()

        for c in self._results:
            skills = self._get_candidate_field(c, "skills", [])
            if isinstance(skills, str):
                skills = [s.strip() for s in skills.split(",")]
            all_skills.update(skills)
            loc = self._get_candidate_field(c, "location", "")
            if loc:
                locations.add(loc)
            comp = self._get_current_company(c)
            if comp:
                companies.add(comp)

        return {
            "count": len(self._results),
            "avg_score": round(sum(scores) / len(scores), 2),
            "max_score": round(max(scores), 2),
            "min_score": round(min(scores), 2),
            "score_std": round((sum((s - sum(scores) / len(scores)) ** 2 for s in scores) / len(scores)) ** 0.5, 2),
            "unique_skills": len(all_skills),
            "unique_locations": len(locations),
            "unique_companies": len(companies),
            "locations": list(locations),
            "companies": list(companies)
        }

    # =====================================================================
    # 导出功能
    # =====================================================================

    def export_json(self, output_path: str = None) -> str:
        """
        导出查询结果为JSON格式

        Args:
            output_path: 输出文件路径（不提供则返回JSON字符串）

        Returns:
            JSON字符串
        """
        export_data = {
            "query_results": self._results,
            "summary": self.get_summary()
        }
        json_str = json.dumps(export_data, ensure_ascii=False, indent=2)

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"查询结果已导出到: {output_path}")

        return json_str

    def export_csv(self, output_path: str) -> None:
        """
        导出查询结果为CSV格式

        Args:
            output_path: 输出文件路径
        """
        if not self._results:
            print("无结果可导出")
            return

        # 确定列
        headers = [
            "candidate_id", "name", "total_score",
            "skill_score", "experience_score", "education_score", "potential_score",
            "experience_years", "education_level", "location", "current_company",
            "employment_status", "skills", "match_reason"
        ]

        rows = []
        for c in self._results:
            scores = c.get("scores", {})
            profile = c.get("profile", {})
            skills = self._get_candidate_field(c, "skills", [])
            if isinstance(skills, list):
                skills = ", ".join(skills)

            rows.append({
                "candidate_id": self._get_candidate_field(c, "id", ""),
                "name": self._get_candidate_field(c, "name", ""),
                "total_score": self._get_candidate_field(c, "total_score", 0),
                "skill_score": scores.get("skill", 0),
                "experience_score": scores.get("experience", 0),
                "education_score": scores.get("education", 0),
                "potential_score": scores.get("potential", 0),
                "experience_years": self._get_candidate_field(c, "experience_years", 0),
                "education_level": self._get_candidate_field(c, "education_level", ""),
                "location": self._get_candidate_field(c, "location", ""),
                "current_company": self._get_current_company(c),
                "employment_status": self._get_candidate_field(c, "employment_status", ""),
                "skills": skills,
                "match_reason": c.get("match_reason", "")
            })

        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

        print(f"CSV已导出到: {output_path}（{len(rows)}行）")

    # =====================================================================
    # 链式调用支持
    # =====================================================================

    def __len__(self) -> int:
        return len(self._results)

    def __repr__(self) -> str:
        return f"QueryEngine(results={len(self._results)})"

    def __iter__(self):
        return iter(self._results)


# =====================================================================
# 独立运行入口
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description='交互式查询引擎（Phase 3）')
    parser.add_argument('--data', required=True, help='匹配结果JSON文件路径')
    parser.add_argument('--filter-skill', help='按技能筛选')
    parser.add_argument('--filter-min-score', type=float, help='最低分数筛选')
    parser.add_argument('--filter-location', help='按地域筛选')
    parser.add_argument('--sort-by', help='排序字段')
    parser.add_argument('--sort-desc', action='store_true', default=True, help='降序排序')
    parser.add_argument('--aggregate-by', help='聚合维度（company/location/education_level等）')
    parser.add_argument('--compare', nargs='+', help='候选人ID对比（空格分隔多个ID）')
    parser.add_argument('--top', type=int, help='取前N个')
    parser.add_argument('--export-json', help='导出JSON到指定路径')
    parser.add_argument('--export-csv', help='导出CSV到指定路径')

    args = parser.parse_args()

    # 加载数据
    with open(args.data, 'r', encoding='utf-8') as f:
        loaded = json.load(f)

    # Phase 3: 兼容 talent_matcher.py 新输出格式（dict with "results" key）
    if isinstance(loaded, dict) and 'results' in loaded:
        results = loaded['results']
    else:
        results = loaded

    # 初始化查询引擎
    engine = QueryEngine(results)

    print("=" * 60)
    print("交互式查询引擎")
    print("=" * 60)
    print(f"  加载匹配结果: {len(results)} 条")

    # 应用筛选
    if args.filter_skill or args.filter_min_score is not None or args.filter_location:
        engine = engine.filter(
            skill=args.filter_skill,
            min_score=args.filter_min_score,
            location=args.filter_location
        )
        print(f"  筛选后剩余: {engine.count()} 条")
        if args.filter_skill:
            print(f"    - 技能筛选: {args.filter_skill}")
        if args.filter_min_score is not None:
            print(f"    - 最低分数: {args.filter_min_score}")
        if args.filter_location:
            print(f"    - 地域筛选: {args.filter_location}")

    # 应用排序
    if args.sort_by:
        engine = engine.sort_by(args.sort_by, descending=args.sort_desc)
        print(f"  排序字段: {args.sort_by} ({'降序' if args.sort_desc else '升序'})")

    # 取Top N
    if args.top:
        engine = engine.top(args.top)
        print(f"  取前 {args.top} 条")

    # 聚合
    if args.aggregate_by:
        agg_result = engine.aggregate(by=args.aggregate_by)
        print(f"\n{'─' * 60}")
        print(f"  聚合统计（按 {args.aggregate_by} 分组）:")
        print(f"{'─' * 60}")
        for group, stats in agg_result.items():
            print(f"    {group}: 人数={stats['count']}, "
                  f"平均分={stats['avg_score']}, "
                  f"最高分={stats['max_score']}, "
                  f"最低分={stats['min_score']}")

    # 对比
    if args.compare:
        compare_result = engine.compare(args.compare)
        print(f"\n{'─' * 60}")
        print(f"  候选人对比分析:")
        print(f"{'─' * 60}")
        if "error" in compare_result:
            print(f"    错误: {compare_result['error']}")
        else:
            print(f"  {compare_result['analysis']}")
            print(f"\n  逐维度对比:")
            for dim_key, dim_info in compare_result["dimensions"].items():
                values_str = ", ".join(f"{k}={v}" for k, v in dim_info["values"].items())
                print(f"    {dim_info['label']}: {values_str}")
            if compare_result["overall_winner"]:
                w = compare_result["overall_winner"]
                print(f"\n  综合最优: {w['name']}（{w['score']}分）")

    # 输出结果列表
    if not args.aggregate_by and not args.compare:
        print(f"\n{'─' * 60}")
        print(f"  查询结果（共 {engine.count()} 条）:")
        print(f"{'─' * 60}")
        summary = engine.get_summary()
        print(f"  平均分: {summary['avg_score']}, 最高分: {summary['max_score']}, 最低分: {summary['min_score']}")

        for i, c in enumerate(engine.get_results(), 1):
            name = c.get("candidate_name", c.get("profile", {}).get("name", ""))
            score = c.get("total_score", 0)
            scores = c.get("scores", {})
            print(f"    {i}. {name} - 总分: {score} "
                  f"(技能:{scores.get('skill', 0)}, 经验:{scores.get('experience', 0)}, "
                  f"学历:{scores.get('education', 0)}, 潜力:{scores.get('potential', 0)})")

    # 导出
    if args.export_json:
        engine.export_json(args.export_json)

    if args.export_csv:
        engine.export_csv(args.export_csv)

    print(f"\n{'=' * 60}")
    print("查询完成!")


if __name__ == "__main__":
    main()
