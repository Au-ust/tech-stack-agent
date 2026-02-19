"""
表单字段定义 - 极简版技术选型 Agent
仅保留影响选型的硬核字段
"""

FIELD_DEFINITIONS = {
    "project_type": {
        "group": "project_basic",
        "type": "list",
        "message": "项目类型",
        "choices": ["Web-C端", "Web-B端", "小程序", "移动端开发"],
        "default": "Web-C端",
    },
    "project_stage": {
        "group": "project_basic",
        "type": "list",
        "message": "项目阶段",
        "choices": ["全新开发", "项目新增", "局部模块替换"],
        "default": "全新开发",
    },
    "frontend_count": {
        "group": "project_basic",
        "type": "number",
        "message": "本次参与前端人数",
        "default": 1,
    },
    "existing_stack": {
        "group": "project_basic",
        "type": "textarea",
        "message": "现有技术栈（新项目可不填；已有项目填框架/库/版本）",
    },
    "package_json": {
        "group": "project_basic",
        "type": "textarea",
        "message": "package.json（项目新增/局部替换时强烈建议粘贴）",
    },
    "core_features": {
        "group": "business",
        "type": "textarea",
        "message": "业务核心功能（如：后台管理、商品列表、表单、图表、实时消息、视频、3D等）",
    },
    "key_features": {
        "group": "business",
        "type": "textarea",
        "message": "关键特性（如：SEO、虚拟滚动、弱网兼容、离线、高并发、低延迟、动画流畅等）",
    },
    "dev_preference": {
        "group": "constraints",
        "type": "textarea",
        "message": "开发偏好（新项目填：React/Vue/轻量化/高性能/TS优先等；已有项目可不填）",
    },
    "forbidden_items": {
        "group": "constraints",
        "type": "textarea",
        "message": "禁忌与不接受项（如：太重、包体积大、生态停更、难定制、版权、学习成本高等）",
    },
}

GROUP_ORDER = ["project_basic", "business", "constraints"]

GROUP_LABELS = {
    "project_basic": "项目基础",
    "business": "业务与需求",
    "constraints": "开发偏好与约束",
}
