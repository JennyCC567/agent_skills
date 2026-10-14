#!/usr/bin/env python3
"""
敏感信息脱敏脚本
自动识别并脱敏以下敏感信息：
- 手机号（138****0000格式）
- 邮箱（m***@email.com格式）
- 身份证号（全部掩码）
- 银行账号（全部掩码）
- 详细地址（[已脱敏地址]格式）
- 护照号码（全部掩码）
- 社保号码（全部掩码）

注意：期望薪资保留，不作脱敏处理（用于人岗匹配分析）
"""

import argparse
import re
import sys


def mask_phone(text):
    """
    脱敏手机号
    格式：138****0000
    
    Args:
        text: 原始文本
        
    Returns:
        str: 脱敏后的文本
    """
    # 匹配中国大陆手机号（11位，1开头）
    pattern = re.compile(r'1[3-9]\d{9}')
    
    def replace_func(match):
        phone = match.group()
        return phone[:3] + '****' + phone[-4:]
    
    return pattern.sub(replace_func, text)


def mask_email(text):
    """
    脱敏邮箱
    格式：m***@email.com
    
    Args:
        text: 原始文本
        
    Returns:
        str: 脱敏后的文本
    """
    # 匹配邮箱格式
    pattern = re.compile(r'([a-zA-Z0-9])[a-zA-Z0-9._%+-]{0,}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    
    def replace_func(match):
        email = match.group()
        # 保留首字母，中间用***替代，保留@和域名
        at_pos = email.find('@')
        return email[0] + '***' + email[at_pos:]
    
    return pattern.sub(replace_func, text)


def mask_id_card(text):
    """
    脱敏身份证号
    格式：**************
    
    Args:
        text: 原始文本
        
    Returns:
        str: 脱敏后的文本
    """
    # 匹配18位身份证号
    pattern = re.compile(r'\d{17}[\dXx]')
    
    def replace_func(match):
        return '**************'
    
    return pattern.sub(replace_func, text)


def mask_bank_account(text):
    """
    脱敏银行账号
    格式：[已脱敏]
    
    Args:
        text: 原始文本
        
    Returns:
        str: 脱敏后的文本
    """
    # 匹配银行卡号（16-19位数字）
    pattern = re.compile(r'\b\d{16,19}\b')
    
    def replace_func(match):
        return '[已脱敏]'
    
    return pattern.sub(replace_func, text)


def mask_address(text):
    """
    脱敏详细地址
    格式：[已脱敏]
    
    Args:
        text: 原始文本
        
    Returns:
        str: 脱敏后的文本
    """
    # 匹配详细地址（省市区+详细地址）
    pattern = re.compile(r'((?:[^0-9\\n]{2,10}[省市区县])|(?:[^\\n]{5,30}?(?:路|街|道|巷|号|栋|单元|室|楼)))[^\\n]{0,50}')
    
    def replace_func(match):
        return '[已脱敏地址]'
    
    return pattern.sub(replace_func, text)


def mask_passport(text):
    """
    脱敏护照号码
    格式：[已脱敏]
    
    Args:
        text: 原始文本
        
    Returns:
        str: 脱敏后的文本
    """
    # 匹配护照号码（E/G/S/D/P开头+8-9位数字或字母）
    pattern = re.compile(r'[EGSDP]\d{8,9}|[EGSDP][A-Z]\d{7,8}', re.IGNORECASE)
    
    def replace_func(match):
        return '[已脱敏]'
    
    return pattern.sub(replace_func, text)


def mask_social_security(text):
    """
    脱敏社保号码
    格式：[已脱敏]
    
    Args:
        text: 原始文本
        
    Returns:
        str: 脱敏后的文本
    """
    # 匹配社保号码（18位或特殊格式）
    pattern = re.compile(r'\b\d{18}\b')
    
    def replace_func(match):
        return '[已脱敏]'
    
    return pattern.sub(replace_func, text)


def mask_name(text):
    """
    脱敏姓名（可选功能，默认不启用）
    注意：姓名分析可能需要，谨慎使用
    
    Args:
        text: 原始文本
        
    Returns:
        str: 脱敏后的文本
    """
    # 匹配2-4个汉字的姓名
    pattern = re.compile(r'(?<![\\u4e00-\\u9fa5])([\\u4e00-\\u9fa5]{2,4})(?![\\u4e00-\\u9fa5])')
    
    def replace_func(match):
        name = match.group()
        length = len(name)
        if length == 2:
            return name[0] + '*'
        elif length == 3:
            return name[0] + '**'
        else:
            return name[0] + '***'
    
    return pattern.sub(replace_func, text)


def mask_sensitive_info(text):
    """
    综合脱敏处理
    
    Args:
        text: 原始文本
        
    Returns:
        str: 脱敏后的文本
    """
    # 按顺序执行脱敏（注意：期望薪资保留，不作脱敏处理）
    text = mask_phone(text)
    text = mask_email(text)
    text = mask_id_card(text)
    # 薪资信息保留用于人岗匹配分析，不做脱敏处理
    text = mask_bank_account(text)
    text = mask_address(text)
    text = mask_passport(text)
    text = mask_social_security(text)

    return text


def main():
    parser = argparse.ArgumentParser(description='敏感信息脱敏处理')
    parser.add_argument('--text', '-t', required=True, help='待脱敏的文本内容')
    
    args = parser.parse_args()
    
    # 执行脱敏
    masked_text = mask_sensitive_info(args.text)
    
    # 输出脱敏后的文本
    print(masked_text)


if __name__ == '__main__':
    main()
