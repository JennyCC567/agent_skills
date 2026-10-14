#!/usr/bin/env python3
"""
数据去重脚本
功能：基于多维度指纹进行人才数据去重
"""

import argparse
import json
import hashlib
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict


class DataDeduplicator:
    """数据去重器"""

    def __init__(self, dedup_config: Dict[str, Any]):
        """
        初始化去重器

        Args:
            dedup_config: 去重配置，包含字段优先级和匹配阈值
        """
        self.field_priority = dedup_config.get("field_priority", [
            "phone", "email", "id_card"
        ])
        self.match_threshold = dedup_config.get("match_threshold", 0.8)

    def _generate_fingerprint(self, record: Dict[str, Any], fields: List[str]) -> str:
        """
        生成记录指纹

        Args:
            record: 人才记录
            fields: 用于生成指纹的字段列表

        Returns:
            指纹字符串
        """
        fingerprint_parts = []

        for field in fields:
            value = record.get(field, "")
            if value:
                # 规范化：去除空格、转小写
                normalized = str(value).strip().lower()
                fingerprint_parts.append(normalized)

        if not fingerprint_parts:
            # 如果关键字段都为空，使用工作经历生成指纹
            fingerprint_parts = self._generate_experience_fingerprint(record)

        # 生成 MD5 哈希
        fingerprint_str = "|".join(fingerprint_parts)
        return hashlib.md5(fingerprint_str.encode('utf-8')).hexdigest()

    def _generate_experience_fingerprint(self, record: Dict[str, Any]) -> List[str]:
        """
        基于工作经历生成指纹（用于弱唯一性识别）

        Args:
            record: 人才记录

        Returns:
            指纹组成部分列表
        """
        fingerprint_parts = []

        # 姓名 + 最高学历
        name = record.get("name", "").strip().lower()
        education = record.get("education_level", "").strip().lower()
        if name and education:
            fingerprint_parts.append(f"{name}|{education}")

        # 工作经历指纹
        work_experience = record.get("work_experience", [])
        for exp in work_experience:
            company = exp.get("company", "").strip().lower()
            job_title = exp.get("job_title", "").strip().lower()
            start_date = exp.get("start_date", "")
            if company and job_title:
                fingerprint_parts.append(f"{company}|{job_title}|{start_date}")

        return fingerprint_parts

    def _exact_match(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """
        精确匹配（基于强唯一标识）

        Args:
            record1: 记录1
            record2: 记录2

        Returns:
            是否精确匹配
        """
        # 检查手机号
        phone1 = record1.get("phone", "").strip()
        phone2 = record2.get("phone", "").strip()
        if phone1 and phone2 and phone1 == phone2:
            return True

        # 检查邮箱
        email1 = record1.get("email", "").strip().lower()
        email2 = record2.get("email", "").strip().lower()
        if email1 and email2 and email1 == email2:
            return True

        # 检查身份证号
        id_card1 = record1.get("id_card", "").strip()
        id_card2 = record2.get("id_card", "").strip()
        if id_card1 and id_card2 and id_card1 == id_card2:
            return True

        return False

    def _fuzzy_match(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> float:
        """
        模糊匹配（基于弱唯一标识）

        Args:
            record1: 记录1
            record2: 记录2

        Returns:
            相似度分数 (0-1)
        """
        score = 0.0
        total_weight = 0.0

        # 姓名匹配
        name1 = record1.get("name", "").strip().lower()
        name2 = record2.get("name", "").strip().lower()
        if name1 and name2:
            if name1 == name2:
                score += 0.3
            elif self._name_similarity(name1, name2) > 0.8:
                score += 0.15
            total_weight += 0.3

        # 工作经历匹配
        exp1 = record1.get("work_experience", [])
        exp2 = record2.get("work_experience", [])
        if exp1 and exp2:
            exp_similarity = self._experience_similarity(exp1, exp2)
            score += exp_similarity * 0.7
            total_weight += 0.7

        # 学历匹配
        edu1 = record1.get("education_level", "").strip().lower()
        edu2 = record2.get("education_level", "").strip().lower()
        if edu1 and edu2 and edu1 == edu2:
            score += 0.2
            total_weight += 0.2

        return score / total_weight if total_weight > 0 else 0.0

    def _name_similarity(self, name1: str, name2: str) -> float:
        """
        计算姓名相似度（简单实现）

        Args:
            name1: 姓名1
            name2: 姓名2

        Returns:
            相似度 (0-1)
        """
        # 去除空格和特殊字符
        clean1 = ''.join(c for c in name1 if c.isalpha())
        clean2 = ''.join(c for c in name2 if c.isalpha())

        if clean1 == clean2:
            return 1.0

        # 计算编辑距离
        len1, len2 = len(clean1), len(clean2)
        if len1 == 0 or len2 == 0:
            return 0.0

        # 简单的编辑距离计算
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                if clean1[i-1] == clean2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1

        max_len = max(len1, len2)
        return 1.0 - dp[len1][len2] / max_len

    def _experience_similarity(self, exp1: List[Dict], exp2: List[Dict]) -> float:
        """
        计算工作经历相似度

        Args:
            exp1: 工作经历1
            exp2: 工作经历2

        Returns:
            相似度 (0-1)
        """
        if not exp1 or not exp2:
            return 0.0

        # 提取公司+职位组合
        set1 = set(
            f"{exp.get('company', '').strip().lower()}|{exp.get('job_title', '').strip().lower()}"
            for exp in exp1
        )
        set2 = set(
            f"{exp.get('company', '').strip().lower()}|{exp.get('job_title', '').strip().lower()}"
            for exp in exp2
        )

        # 计算交集和并集
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        if union == 0:
            return 0.0

        return intersection / union

    def deduplicate(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, List[str]]]:
        """
        执行去重

        Args:
            records: 人才记录列表

        Returns:
            (去重后的记录列表, 去重映射表 {主记录ID: [重复记录ID列表]})
        """
        unique_records = []
        duplicate_groups = {}
        fingerprints = defaultdict(list)

        # 第一轮：精确匹配
        print("执行精确匹配...")
        exact_processed = set()
        for i, record in enumerate(records):
            if i in exact_processed:
                continue

            duplicates = [i]
            for j in range(i + 1, len(records)):
                if j in exact_processed:
                    continue

                if self._exact_match(record, records[j]):
                    duplicates.append(j)
                    exact_processed.add(j)

            if len(duplicates) > 1:
                # 保留信息最完整的记录
                main_idx = self._select_main_record([records[idx] for idx in duplicates])
                duplicate_groups[f"record_{duplicates[main_idx]}"] = [f"record_{idx}" for idx in duplicates if idx != duplicates[main_idx]]
                unique_records.append(records[duplicates[main_idx]])
            else:
                unique_records.append(record)

            exact_processed.add(i)

        # 第二轮：模糊匹配
        print("执行模糊匹配...")
        final_records = []
        fuzzy_processed = set()

        for i, record in enumerate(unique_records):
            if i in fuzzy_processed:
                continue

            # 生成指纹
            fingerprint = self._generate_fingerprint(record, self.field_priority)
            fingerprints[fingerprint].append(i)

            # 检查是否有相同指纹的记录
            if len(fingerprints[fingerprint]) > 1:
                # 已存在相同指纹，进行合并
                continue

            fuzzy_processed.add(i)
            final_records.append(record)

        # 处理指纹相同的记录（模糊匹配）
        for fingerprint, indices in fingerprints.items():
            if len(indices) == 1:
                continue

            # 检查是否需要合并
            main_record = final_records[indices[0]]
            merged = False

            for idx in indices[1:]:
                similarity = self._fuzzy_match(main_record, unique_records[idx])
                if similarity >= self.match_threshold:
                    # 合并记录
                    merged_record = self._merge_records(main_record, unique_records[idx])
                    main_record = merged_record
                    merged = True

            if merged:
                # 更新主记录
                # 找到 main_record 在 final_records 中的位置并更新
                for i, rec in enumerate(final_records):
                    if rec.get("id") == main_record.get("id"):
                        final_records[i] = main_record
                        break

        return final_records, duplicate_groups

    def _select_main_record(self, records: List[Dict[str, Any]]) -> int:
        """
        选择主记录（保留信息最完整的）

        Args:
            records: 重复记录列表

        Returns:
            主记录的索引
        """
        def completeness_score(record: Dict[str, Any]) -> int:
            """计算记录完整度分数"""
            score = 0
            if record.get("name"):
                score += 1
            if record.get("phone"):
                score += 2
            if record.get("email"):
                score += 2
            if record.get("skills"):
                score += len(record["skills"])
            if record.get("work_experience"):
                score += len(record["work_experience"])
            if record.get("education"):
                score += len(record["education"])
            return score

        scores = [completeness_score(rec) for rec in records]
        return scores.index(max(scores))

    def _merge_records(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并两条记录，保留更完整的信息

        Args:
            record1: 记录1
            record2: 记录2

        Returns:
            合并后的记录
        """
        merged = record1.copy()

        # 合并技能（去重）
        skills1 = set(merged.get("skills", []))
        skills2 = set(record2.get("skills", []))
        merged["skills"] = list(skills1 | skills2)

        # 合并工作经历（保留更多）
        exp1 = merged.get("work_experience", [])
        exp2 = record2.get("work_experience", [])
        if len(exp2) > len(exp1):
            merged["work_experience"] = exp2

        # 合并教育经历（保留更多）
        edu1 = merged.get("education", [])
        edu2 = record2.get("education", [])
        if len(edu2) > len(edu1):
            merged["education"] = edu2

        # 补充缺失字段
        for field in ["phone", "email", "id_card"]:
            if not merged.get(field) and record2.get(field):
                merged[field] = record2[field]

        return merged


def load_json(file_path: str) -> Any:
    """加载 JSON 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Any, file_path: str) -> None:
    """保存 JSON 文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='数据去重脚本')
    parser.add_argument('--input', required=True, help='输入数据文件路径（JSON格式）')
    parser.add_argument('--config', required=True, help='去重配置文件路径（JSON格式）')
    parser.add_argument('--output', required=True, help='输出数据文件路径（JSON格式）')

    args = parser.parse_args()

    # 加载数据和配置
    print(f"加载数据: {args.input}")
    records = load_json(args.input)

    print(f"加载去重配置: {args.config}")
    dedup_config = load_json(args.config)

    # 执行去重
    print(f"开始去重处理，共有 {len(records)} 条记录...")
    deduplicator = DataDeduplicator(dedup_config)
    unique_records, duplicate_groups = deduplicator.deduplicate(records)

    # 保存结果
    print(f"保存去重结果到: {args.output}")
    save_json(unique_records, args.output)

    # 保存去重映射表
    if duplicate_groups:
        mapping_file = args.output.replace(".json", "_mapping.json")
        print(f"保存去重映射表到: {mapping_file}")
        save_json(duplicate_groups, mapping_file)

    # 输出统计信息
    print("\n去重统计:")
    print(f"  输入记录数: {len(records)}")
    print(f"  输出记录数: {len(unique_records)}")
    print(f"  去重数量: {len(records) - len(unique_records)}")
    print(f"  去重率: {(len(records) - len(unique_records)) / len(records) * 100:.2f}%")
    print(f"  发现重复组数: {len(duplicate_groups)}")

    print("\n去重完成!")


if __name__ == "__main__":
    main()
