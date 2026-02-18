"""
Streamlit Web Interface (Optional)

Run with: streamlit run app.py
"""
import streamlit as st
from datetime import datetime

from src.agent.graph import get_workflow_app
from src.utils.file_manager import get_file_manager

# Page config
st.set_page_config(
    page_title="前端技术栈选型 Agent",
    page_icon="🚀",
    layout="wide",
)

# Title
st.title("🚀 前端技术栈选型 Agent")
st.markdown("基于 LangGraph 和 Deepseek API 的智能技术选型助手")

# Sidebar - Project Information Form
st.sidebar.header("📋 项目信息")

with st.sidebar.form("project_form"):
    project_type = st.selectbox(
        "项目类型",
        ["Web应用", "移动应用", "桌面应用", "小程序", "混合应用", "其他"]
    )
    
    team_size = st.selectbox(
        "团队规模",
        ["1-3人（小型团队）", "4-10人（中型团队）", "10人以上（大型团队）"]
    )
    
    timeline = st.selectbox(
        "开发时间线",
        ["1个月内", "1-3个月", "3-6个月", "6个月以上"]
    )
    
    special_requirements = st.text_area(
        "特殊需求",
        placeholder="例如：需要SEO优化、高性能、实时通信等",
        height=100
    )
    
    submit_button = st.form_submit_button("🎯 开始生成")

# Main area
if submit_button:
    # Initialize state
    initial_state = {
        "project_type": project_type,
        "team_size": team_size,
        "timeline": timeline,
        "special_requirements": special_requirements or "无特殊需求",
        "extracted_requirements": [],
        "tech_constraints": [],
        "search_results": [],
        "recommended_stack": {},
        "final_document": "",
        "current_step": "",
        "needs_search": False,
        "messages": [],
        "output_path": "",
    }
    
    # Progress indicator
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Get workflow
        app = get_workflow_app()
        
        # Note: For proper Streamlit integration, we would need to modify
        # the nodes to not use rich/input(). This is a simplified version.
        
        status_text.text("⏳ 正在分析项目需求...")
        progress_bar.progress(20)
        
        # In a real implementation, we would need to:
        # 1. Modify nodes to work without CLI input
        # 2. Stream progress updates to Streamlit
        # 3. Handle the workflow execution asynchronously
        
        st.warning(
            "⚠️ Streamlit 界面需要对节点进行修改以支持非交互式运行。\n\n"
            "当前请使用 CLI 版本: `python cli.py`"
        )
        
        status_text.text("请使用 CLI 版本")
        progress_bar.progress(100)
        
    except Exception as e:
        st.error(f"❌ 发生错误: {str(e)}")
        st.info("请确保已配置 .env 文件中的 DEEPSEEK_API_KEY")

else:
    # Show welcome message
    st.info("👈 请在左侧填写项目信息，然后点击 '开始生成' 按钮")
    
    st.markdown("---")
    
    # Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 智能分析")
        st.markdown("自动分析项目需求和技术约束")
    
    with col2:
        st.markdown("### 🔍 技术调研")
        st.markdown("在线搜索最新技术趋势")
    
    with col3:
        st.markdown("### 📝 文档生成")
        st.markdown("生成完整的技术选型文档")
    
    st.markdown("---")
    
    # Recent documents
    st.subheader("📚 最近生成的文档")
    
    try:
        file_manager = get_file_manager()
        recent_docs = file_manager.list_outputs()
        
        if recent_docs:
            for doc in recent_docs[:5]:
                st.markdown(f"- 📄 {doc}")
        else:
            st.markdown("_暂无生成的文档_")
    except Exception:
        st.markdown("_无法加载文档列表_")

# Footer
st.markdown("---")
st.markdown(
    "_Powered by [LangGraph](https://github.com/langchain-ai/langgraph) "
    "& [Deepseek](https://www.deepseek.com/)_"
)
