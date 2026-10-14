#!/usr/bin/env python3
"""
数据标准化脚本
功能：对公司名、职位名、技能标签进行标准化处理
"""

import argparse
import json
import re
from typing import Dict, List, Any
from collections import defaultdict


class DataNormalizer:
    """数据标准化处理器"""

    def __init__(self, mapping_rules: Dict[str, Dict[str, str]]):
        """
        初始化标准化器

        Args:
            mapping_rules: 映射规则，支持两种键名格式：
                - 标准格式: {"company_mapping": {...}, "title_mapping": {...}, "skill_normalization": {...}}
                - 旧格式: {"company": {...}, "job": {...}, "skill": {...}}
        """
        # 兼容两种键名格式：优先使用文档标准的 company_mapping/title_mapping/skill_normalization
        # 回退到旧的 company/job/skill 键名
        self.company_map = mapping_rules.get("company_mapping", mapping_rules.get("company", {}))
        self.job_map = mapping_rules.get("title_mapping", mapping_rules.get("job", {}))
        self.skill_map = mapping_rules.get("skill_normalization", mapping_rules.get("skill", {}))

        # 构建反向索引用于快速查找
        self.company_reverse = self._build_reverse_index(self.company_map)
        self.job_reverse = self._build_reverse_index(self.job_map)
        self.skill_reverse = self._build_reverse_index(self.skill_map)

    def _build_reverse_index(self, mapping: Dict[str, str]) -> Dict[str, str]:
        """构建反向索引，支持模糊匹配"""
        reverse = {}
        for key, value in mapping.items():
            # 精确匹配
            reverse[key.lower()] = value
            # 模糊匹配（提取关键词）
            keywords = re.findall(r'\w+', key.lower())
            for kw in keywords:
                if len(kw) > 2:  # 忽略过短的关键词
                    if kw not in reverse:
                        reverse[kw] = value
        return reverse

    def normalize_company(self, company_name: str) -> str:
        """
        标准化公司名称

        Args:
            company_name: 原始公司名称

        Returns:
            标准化后的公司名称
        """
        if not company_name:
            return "Unknown"

        # 去除特殊字符和多余空格
        cleaned = re.sub(r'[^\w\s\-\.]', '', company_name.strip())
        cleaned = ' '.join(cleaned.split())

        # 精确匹配
        if cleaned.lower() in self.company_reverse:
            return self.company_reverse[cleaned.lower()]

        # 模糊匹配
        for keyword, standard_name in self.company_reverse.items():
            if keyword in cleaned.lower():
                return standard_name

        # 无法匹配则返回原值（已清洗）
        return cleaned

    def normalize_job(self, job_title: str) -> str:
        """
        标准化职位名称

        Args:
            job_title: 原始职位名称

        Returns:
            标准化后的职位名称
        """
        if not job_title:
            return "Unknown"

        # 去除特殊字符和多余空格
        cleaned = re.sub(r'[^\w\s\-\+]', '', job_title.strip())
        cleaned = ' '.join(cleaned.split())

        # 精确匹配
        if cleaned.lower() in self.job_reverse:
            return self.job_reverse[cleaned.lower()]

        # 模糊匹配
        for keyword, standard_name in self.job_reverse.items():
            if keyword in cleaned.lower():
                return standard_name

        # 无法匹配则返回原值（已清洗）
        return cleaned

    def normalize_skills(self, skills: List[str]) -> List[str]:
        """
        标准化技能标签

        Args:
            skills: 原始技能列表

        Returns:
            标准化后的技能列表
        """
        if not skills:
            return []

        normalized_skills = []
        seen = set()

        for skill in skills:
            if not skill:
                continue

            # 去除特殊字符和多余空格
            cleaned = re.sub(r'[^\w\s\-\+\.]', '', skill.strip())
            cleaned = ' '.join(cleaned.split())

            if not cleaned:
                continue

            # 精确匹配
            if cleaned.lower() in self.skill_reverse:
                standard_skill = self.skill_reverse[cleaned.lower()]
            else:
                # 模糊匹配
                matched = False
                for keyword, standard_name in self.skill_reverse.items():
                    if keyword in cleaned.lower():
                        standard_skill = standard_name
                        matched = True
                        break
                if not matched:
                    standard_skill = cleaned

            # 去重
            if standard_skill.lower() not in seen:
                normalized_skills.append(standard_skill)
                seen.add(standard_skill.lower())

        return normalized_skills

    def normalize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化单条人才记录

        Args:
            record: 原始人才记录

        Returns:
            标准化后的人才记录
        """
        normalized = record.copy()

        # 标准化公司经历
        if "work_experience" in normalized:
            for exp in normalized["work_experience"]:
                if "company" in exp:
                    exp["company"] = self.normalize_company(exp["company"])
                if "job_title" in exp:
                    exp["job_title"] = self.normalize_job(exp["job_title"])
                if "skills" in exp:
                    exp["skills"] = self.normalize_skills(exp["skills"])

        # 标准化当前职位
        if "current_company" in normalized:
            normalized["current_company"] = self.normalize_company(normalized["current_company"])
        if "current_job_title" in normalized:
            normalized["current_job_title"] = self.normalize_job(normalized["current_job_title"])

        # 标准化顶级 company/title 字段（兼容简化的记录格式）
        if "company" in normalized:
            normalized["company"] = self.normalize_company(normalized["company"])
        if "title" in normalized:
            normalized["title"] = self.normalize_job(normalized["title"])

        # 标准化技能标签
        if "skills" in normalized:
            normalized["skills"] = self.normalize_skills(normalized["skills"])

        return normalized

    def normalize_batch(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量标准化人才记录

        Args:
            records: 原始人才记录列表

        Returns:
            标准化后的人才记录列表
        """
        return [self.normalize_record(record) for record in records]


def load_mapping_rules(mapping_file: str) -> Dict[str, Dict[str, str]]:
    """加载映射规则文件"""
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_data(input_file: str) -> List[Dict[str, Any]]:
    """加载输入数据"""
    with open(input_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data: List[Dict[str, Any]], output_file: str) -> None:
    """保存输出数据"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='数据标准化脚本')
    parser.add_argument('--input', required=True, help='输入数据文件路径（JSON格式）')
    parser.add_argument('--mapping', required=True, help='映射规则文件路径（JSON格式）')
    parser.add_argument('--output', required=True, help='输出数据文件路径（JSON格式）')

    args = parser.parse_args()

    # 加载数据和映射规则
    print(f"加载数据: {args.input}")
    records = load_data(args.input)
    print(f"加载映射规则: {args.mapping}")
    mapping_rules = load_mapping_rules(args.mapping)

    # 标准化处理
    print(f"开始标准化处理 {len(records)} 条记录...")
    normalizer = DataNormalizer(mapping_rules)
    normalized_records = normalizer.normalize_batch(records)

    # 保存结果
    print(f"保存结果到: {args.output}")
    save_data(normalized_records, args.output)

    # 输出统计信息（使用normalizer实例中的实际映射规则数，兼容两种键名格式）
    print("\n标准化统计:")
    print(f"  处理记录数: {len(normalized_records)}")
    print(f"  公司映射规则数: {len(normalizer.company_map)}")
    print(f"  职位映射规则数: {len(normalizer.job_map)}")
    print(f"  技能映射规则数: {len(normalizer.skill_map)}")

    print("\n标准化完成!")


if __name__ == "__main__":
    main()
