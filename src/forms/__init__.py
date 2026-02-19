"""
表单模块 - 技术选型 Agent 结构化输入
"""
from src.forms.schema import FIELD_DEFINITIONS, GROUP_ORDER, GROUP_LABELS
from src.forms.collector import collect_form, form_data_to_project_info

__all__ = [
    "FIELD_DEFINITIONS",
    "GROUP_ORDER",
    "GROUP_LABELS",
    "collect_form",
    "form_data_to_project_info",
]
