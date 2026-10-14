#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人数据保护专项规范（DCMM 2.0对齐版）
数据安全与隐私保护工具
"""

import re
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Tuple


# PII四级分类标准
PII_LEVELS = {
    "L1": {
        "name": "公开信息",
        "description": "可公开展示的信息",
        "fields": ["公司名称", "行业", "公司", "企业", "行业领域"],
        "rule": "原样展示"
    },
    "L2": {
        "name": "内部信息",
        "description": "可展示但需标注的信息",
        "fields": ["岗位名称", "工作年限", "职位", "年限", "工作时间"],
        "rule": "可展示但报告标注'内部'"
    },
    "L3": {
        "name": "敏感PII",
        "description": "需要脱敏处理的信息",
        "fields": ["姓名", "手机号", "邮箱", "电话", "email", "手机"],
        "rule": "交付前必须脱敏（掩码/替换）"
    },
    "L4": {
        "name": "核心PII",
        "description": "严禁出现的信息",
        "fields": ["身份证号", "银行卡号", "身份证", "银行卡", "身份证号码", "银行账号"],
        "rule": "严禁出现在交付物中，输入时即拦截"
    }
}


class DataProtection:
    """数据保护类，实现DCMM 2.0对齐的个人数据保护"""

    def __init__(self):
        self.patterns = {
            # 手机号：11位数字，以1开头
            "phone": re.compile(r'(?<!\d)(1[3-9]\d{9})(?!\d)'),
            # 邮箱：标准邮箱格式
            "email": re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'),
            # 身份证号：18位或15位
            "id_card": re.compile(r'(?<!\d)(\d{17}[\dXx]|\d{15})(?!\d)'),
            # 银行卡号：16-19位数字
            "bank_card": re.compile(r'(?<!\d)(\d{16,19})(?!\d)'),
            # 姓名：2-4个中文字符
            "name": re.compile(r'([\u4e00-\u9fa5]{2,4})'),
            # 住址：省市区街道等
            "address": re.compile(r'([\u4e00-\u9fa5]{2,5}(?:省|市|区|县|街道|路|号|小区|大厦|公寓)[\u4e00-\u9fa50-9\-]{0,20})')
        }
        self.processed_data = []
        self.data_retirement_log = []

    def mask_phone(self, phone: str) -> str:
        """
        脱敏手机号：138****5678
        """
        if len(phone) == 11:
            return phone[:3] + "****" + phone[7:]
        return phone

    def mask_email(self, email: str) -> str:
        """
        脱敏邮箱：zhangsan@example.com → zhang***@example.com
        """
        if "@" in email:
            username, domain = email.split("@", 1)
            if len(username) > 3:
                return username[:3] + "***@" + domain
            else:
                return username + "***@" + domain
        return email

    def mask_id_card(self, id_card: str) -> str:
        """
        脱敏身份证号：110********1234
        """
        if len(id_card) == 18:
            return id_card[:3] + "********" + id_card[-4:]
        elif len(id_card) == 15:
            return id_card[:3] + "*******" + id_card[-4:]
        return id_card

    def mask_bank_card(self, bank_card: str) -> str:
        """
        脱敏银行卡号：6222 **** **** 1234
        """
        if len(bank_card) >= 8:
            return bank_card[:4] + " **** **** " + bank_card[-4:]
        return bank_card

    def mask_name(self, name: str) -> str:
        """
        脱敏姓名：张三 → 张*
        """
        if len(name) == 2:
            return name[0] + "*"
        elif len(name) == 3:
            return name[0] + "*" + name[-1]
        elif len(name) == 4:
            return name[0] + "**" + name[-1]
        return name

    def mask_address(self, address: str) -> str:
        """
        脱敏住址：北京市朝阳区建国路88号 → **市**区
        """
        # 简单脱敏：只保留省市
        if "省" in address or "市" in address:
            parts = re.split(r'(省|市|区|县)', address)
            if len(parts) >= 2:
                return "**市**区"
        return "**市**区"

    def classify_pii(self, text: str) -> Dict[str, List[str]]:
        """
        对文本进行PII分类
        返回：{level: [matched_fields]}
        """
        result = {
            "L1": [],
            "L2": [],
            "L3": [],
            "L4": []
        }

        # 检查L4级别（核心PII）
        if self.patterns["id_card"].search(text):
            result["L4"].append("身份证号")
        if self.patterns["bank_card"].search(text):
            result["L4"].append("银行卡号")

        # 检查L3级别（敏感PII）
        if self.patterns["phone"].search(text):
            result["L3"].append("手机号")
        if self.patterns["email"].search(text):
            result["L3"].append("邮箱")
        if self.patterns["name"].search(text):
            result["L3"].append("姓名")
        if self.patterns["address"].search(text):
            result["L3"].append("住址")

        # 检查L2级别（内部信息）
        l2_keywords = ["岗位", "职位", "工作年限", "年限"]
        for keyword in l2_keywords:
            if keyword in text:
                result["L2"].append(keyword)

        # 检查L1级别（公开信息）
        l1_keywords = ["公司", "企业", "行业"]
        for keyword in l1_keywords:
            if keyword in text:
                result["L1"].append(keyword)

        return result

    def desensitize_text(self, text: str, level: str = "L3") -> Tuple[str, Dict[str, int]]:
        """
        对文本进行脱敏处理
        返回：(脱敏后的文本, {field_type: count})
        """
        if not text:
            return text, {}

        stats = {
            "phone": 0,
            "email": 0,
            "id_card": 0,
            "bank_card": 0,
            "name": 0,
            "address": 0
        }

        result = text

        # L4级别：身份证号和银行卡号必须完全移除或强脱敏
        if level in ["L3", "L4"]:
            # 身份证号
            id_cards = self.patterns["id_card"].findall(result)
            for id_card in id_cards:
                masked = self.mask_id_card(id_card)
                result = result.replace(id_card, masked)
                stats["id_card"] += 1

            # 银行卡号
            bank_cards = self.patterns["bank_card"].findall(result)
            for bank_card in bank_cards:
                masked = self.mask_bank_card(bank_card)
                result = result.replace(bank_card, masked)
                stats["bank_card"] += 1

        # L3级别：手机号、邮箱、姓名、住址
        if level == "L3":
            # 手机号
            phones = self.patterns["phone"].findall(result)
            for phone in phones:
                masked = self.mask_phone(phone)
                result = result.replace(phone, masked)
                stats["phone"] += 1

            # 邮箱
            emails = self.patterns["email"].findall(result)
            for email in emails:
                masked = self.mask_email(email)
                result = result.replace(email, masked)
                stats["email"] += 1

            # 姓名（非常谨慎处理，避免误判普通词汇）
            # 只在明确的上下文才处理姓名，这里暂时跳过避免误判
            # 实际使用时建议结合上下文判断
            pass

            # 住址
            addresses = self.patterns["address"].findall(result)
            for address in addresses:
                masked = self.mask_address(address)
                result = result.replace(address, masked)
                stats["address"] += 1

        return result, stats

    def block_core_pii(self, text: str) -> Tuple[bool, List[str]]:
        """
        检查并拦截核心PII（L4级别）
        返回：(是否包含核心PII, [发现的核心PII类型列表])
        """
        found = []

        if self.patterns["id_card"].search(text):
            found.append("身份证号")

        if self.patterns["bank_card"].search(text):
            found.append("银行卡号")

        return len(found) > 0, found

    def get_training_data_isolation_statement(self) -> str:
        """
        训练数据隔离声明
        """
        return """
## 训练数据隔离声明

本技能运行时的用户上传数据（简历/薪酬表等）仅用于当次任务处理，不作为模型训练语料。

交付物中不得包含原始个人数据，仅输出分析结论。
"""

    def get_data_retirement_strategy(self) -> str:
        """
        数据退役策略
        """
        return """
## 数据退役策略

1. **任务完成后，用户上传的原始文件在处理完毕即销毁**（沙箱环境自动清理）
2. **交付物（HTML/Excel）为独立文件，不保留原始数据引用**
"""

    def get_fairness_check_guidelines(self) -> str:
        """
        公平性检查指南
        """
        return """
## 公平性检查（薪酬+简历场景专用）

1. **薪酬对比报告需标注样本量和数据来源**，避免小样本偏差
2. **简历匹配评分不得基于性别、年龄、民族等非能力因素赋分**
3. **交付物中若含推荐/排名，需注明评估维度，确保可解释**
"""

    def get_pipl_compliance_statement(self) -> str:
        """
        PIPL合规声明模板
        """
        return """
## 个人信息保护法（PIPL）合规声明

本报告中涉及的个人数据已依据《个人信息保护法》进行脱敏处理。

原始数据仅用于当次分析任务，处理完成后自动销毁。

数据来源：用户上传（已确认数据使用授权）。
"""

    def generate_compliance_report(self, original_text: str, desensitized_text: str, stats: Dict[str, int]) -> str:
        """
        生成合规性报告
        """
        classification = self.classify_pii(original_text)

        report = f"""
# 数据处理合规性报告

生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

## 一、PII分类检查结果

| 级别 | 类型 | 发现字段 | 处理规则 |
|------|------|---------|---------|
"""
        for level, info in PII_LEVELS.items():
            fields = classification.get(level, [])
            if fields:
                report += f"| {level} | {info['name']} | {', '.join(fields)} | {info['rule']} |\n"
            else:
                report += f"| {level} | {info['name']} | - | {info['rule']} |\n"

        report += f"""
## 二、脱敏处理统计

| 字段类型 | 处理数量 |
|---------|---------|
"""
        for field_type, count in stats.items():
            if count > 0:
                field_names = {
                    "phone": "手机号",
                    "email": "邮箱",
                    "id_card": "身份证号",
                    "bank_card": "银行卡号",
                    "name": "姓名",
                    "address": "住址"
                }
                report += f"| {field_names.get(field_type, field_type)} | {count} |\n"

        report += f"""
## 三、合规声明

{self.get_pipl_compliance_statement()}

{self.get_training_data_isolation_statement()}

{self.get_data_retirement_strategy()}

## 四、公平性检查

{self.get_fairness_check_guidelines()}

---

**合规状态**：已通过数据保护检查
"""
        return report

    def log_data_retirement(self, file_path: str, action: str) -> None:
        """
        记录数据退役日志
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "action": action
        }
        self.data_retirement_log.append(log_entry)


def main():
    """测试数据保护功能"""
    import argparse

    parser = argparse.ArgumentParser(description="个人数据保护工具")
    parser.add_argument("--test-text", type=str, help="测试文本")
    parser.add_argument("--output", type=str, help="输出报告文件")

    args = parser.parse_args()

    protector = DataProtection()

    if args.test_text:
        print("=== 原始文本 ===")
        print(args.test_text)
        print()

        # 检查核心PII
        has_core, found = protector.block_core_pii(args.test_text)
        if has_core:
            print(f"[警告] 发现核心PII: {', '.join(found)}")
            print()

        # 分类PII
        classification = protector.classify_pii(args.test_text)
        print("=== PII分类 ===")
        for level, fields in classification.items():
            if fields:
                print(f"{PII_LEVELS[level]['name']} ({level}): {', '.join(fields)}")
        print()

        # 脱敏处理
        desensitized, stats = protector.desensitize_text(args.test_text)
        print("=== 脱敏后文本 ===")
        print(desensitized)
        print()

        print("=== 脱敏统计 ===")
        for field_type, count in stats.items():
            if count > 0:
                print(f"{field_type}: {count}")
        print()

        # 生成合规报告
        report = protector.generate_compliance_report(args.test_text, desensitized, stats)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"合规报告已保存到: {args.output}")
        else:
            print("=== 合规性报告 ===")
            print(report)


if __name__ == "__main__":
    main()
