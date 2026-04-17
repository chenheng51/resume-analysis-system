import re
from typing import Dict, Any, Optional


class InformationExtractor:
    @staticmethod
    def extract_name(text: str) -> Optional[str]:
        patterns = [
            r'姓名[：:]\s*([\u4e00-\u9fa5]{2,4})',
            r'^([\u4e00-\u9fa5]{2,4})\s',
            r'([\u4e00-\u9fa5]{2,4})\s*先生',
            r'([\u4e00-\u9fa5]{2,4})\s*女士'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        pattern = r'1[3-9]\d{9}'
        match = re.search(pattern, text)
        return match.group(0) if match else None

    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else None

    @staticmethod
    def extract_address(text: str) -> Optional[str]:
        patterns = [
            r'地址[：:]\s*([^\n]{3,50})',
            r'住址[：:]\s*([^\n]{3,50})',
            r'所在地[：:]\s*([^\n]{3,50})',
            r'现居地[：:]\s*([^\n]{3,50})'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None

    @staticmethod
    def extract_job_intention(text: str) -> Optional[str]:
        patterns = [
            r'求职意向[：:]\s*([^\n]{2,100})',
            r'应聘职位[：:]\s*([^\n]{2,100})',
            r'期望职位[：:]\s*([^\n]{2,100})'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None

    @staticmethod
    def extract_salary(text: str) -> Optional[str]:
        patterns = [
            r'期望薪资[：:]\s*([^\n]{2,50})',
            r'期望工资[：:]\s*([^\n]{2,50})',
            r'薪资要求[：:]\s*([^\n]{2,50})'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None

    @staticmethod
    def extract_years(text: str) -> Optional[str]:
        patterns = [
            r'工作年限[：:]\s*([^\n]{1,30})',
            r'工作经验[：:]\s*([^\n]{1,30})',
            r'(\d+)\s*年.*工作经验'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None

    @staticmethod
    def extract_education(text: str) -> Optional[str]:
        patterns = [
            r'学历[：:]\s*([^\n]{2,50})',
            r'教育背景[：:]\s*([^\n]{2,100})',
            r'(博士|硕士|本科|大专|高中|中专)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None

    @staticmethod
    def extract_projects(text: str) -> Optional[str]:
        patterns = [
            r'项目经历[：:]\s*([\s\S]{10,500}?)(?=(?:工作经验|教育背景|技能|求职意向|$))',
            r'项目经验[：:]\s*([\s\S]{10,500}?)(?=(?:工作经验|教育背景|技能|求职意向|$))'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None

    @classmethod
    def extract_all(cls, text: str) -> Dict[str, Any]:
        return {
            "basic_info": {
                "name": cls.extract_name(text),
                "phone": cls.extract_phone(text),
                "email": cls.extract_email(text),
                "address": cls.extract_address(text)
            },
            "job_info": {
                "job_intention": cls.extract_job_intention(text),
                "expected_salary": cls.extract_salary(text)
            },
            "background_info": {
                "work_years": cls.extract_years(text),
                "education": cls.extract_education(text),
                "projects": cls.extract_projects(text)
            }
        }
