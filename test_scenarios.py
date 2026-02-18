"""
Test Scenarios for Tech Stack Agent

These tests can be run after configuring the DEEPSEEK_API_KEY in .env file.
Run with: python test_scenarios.py
"""
import sys
from rich.console import Console
from rich.panel import Panel

from src.agent.graph import get_workflow_app

console = Console()


def create_test_state(project_type, team_size, timeline, special_requirements):
    """Create initial state for testing."""
    return {
        "project_type": project_type,
        "team_size": team_size,
        "timeline": timeline,
        "special_requirements": special_requirements,
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


def test_scenario_1_blog():
    """
    场景 1: 小型博客网站
    - 个人项目
    - 快速开发
    - SEO 优先
    """
    console.print(Panel.fit(
        "[bold cyan]测试场景 1: 个人博客网站[/bold cyan]",
        border_style="cyan"
    ))
    
    state = create_test_state(
        project_type="Web应用",
        team_size="1-3人（小型团队）",
        timeline="1个月内",
        special_requirements="需要SEO优化、支持Markdown、快速加载、响应式设计"
    )
    
    console.print("\n[yellow]项目信息：[/yellow]")
    console.print(f"  项目类型: {state['project_type']}")
    console.print(f"  团队规模: {state['team_size']}")
    console.print(f"  时间线: {state['timeline']}")
    console.print(f"  特殊需求: {state['special_requirements']}")
    
    console.print("\n[yellow]预期技术栈：[/yellow]")
    console.print("  框架: Next.js 14")
    console.print("  样式: Tailwind CSS")
    console.print("  内容: MDX")
    console.print("  部署: Vercel")
    
    return state


def test_scenario_2_ecommerce():
    """
    场景 2: 中型电商平台
    - 中型团队
    - 复杂业务逻辑
    - 高性能要求
    """
    console.print(Panel.fit(
        "[bold cyan]测试场景 2: 中型电商平台[/bold cyan]",
        border_style="cyan"
    ))
    
    state = create_test_state(
        project_type="Web应用",
        team_size="4-10人（中型团队）",
        timeline="3-6个月",
        special_requirements="高性能、实时库存更新、支付集成、用户评论系统、购物车、订单管理"
    )
    
    console.print("\n[yellow]项目信息：[/yellow]")
    console.print(f"  项目类型: {state['project_type']}")
    console.print(f"  团队规模: {state['team_size']}")
    console.print(f"  时间线: {state['timeline']}")
    console.print(f"  特殊需求: {state['special_requirements']}")
    
    console.print("\n[yellow]预期技术栈：[/yellow]")
    console.print("  框架: React 18 + Next.js")
    console.print("  状态管理: Zustand")
    console.print("  UI: shadcn/ui")
    console.print("  数据获取: TanStack Query")
    console.print("  实时通信: WebSocket")
    
    return state


def test_scenario_3_enterprise():
    """
    场景 3: 大型企业后台管理系统
    - 大型团队
    - 长期项目
    - 复杂权限和流程
    """
    console.print(Panel.fit(
        "[bold cyan]测试场景 3: 企业后台管理系统[/bold cyan]",
        border_style="cyan"
    ))
    
    state = create_test_state(
        project_type="Web应用",
        team_size="10人以上（大型团队）",
        timeline="6个月以上",
        special_requirements="复杂权限管理、多角色系统、大量表单、数据可视化、报表导出、审批流程"
    )
    
    console.print("\n[yellow]项目信息：[/yellow]")
    console.print(f"  项目类型: {state['project_type']}")
    console.print(f"  团队规模: {state['team_size']}")
    console.print(f"  时间线: {state['timeline']}")
    console.print(f"  特殊需求: {state['special_requirements']}")
    
    console.print("\n[yellow]预期技术栈：[/yellow]")
    console.print("  框架: React 18 + TypeScript")
    console.print("  状态管理: Redux Toolkit")
    console.print("  UI: Ant Design")
    console.print("  表单: React Hook Form + Zod")
    console.print("  图表: Apache ECharts")
    console.print("  测试: Jest + Cypress")
    
    return state


def run_test(scenario_name, state):
    """Run a single test scenario."""
    try:
        console.print(f"\n[bold green]开始执行测试...[/bold green]")
        
        # Note: This would require modifying nodes to work in non-interactive mode
        # For now, we just validate the state structure
        
        required_fields = [
            "project_type", "team_size", "timeline", "special_requirements"
        ]
        
        for field in required_fields:
            assert field in state, f"缺少字段: {field}"
            assert state[field], f"字段为空: {field}"
        
        console.print("[green]✓ 状态验证通过[/green]")
        console.print(f"[dim]注意: 完整测试需要运行工作流，请确保已配置 API Key[/dim]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ 测试失败: {str(e)}[/red]")
        return False


def main():
    """Main test runner."""
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]前端技术栈选型 Agent - 测试套件[/bold green]\n"
        "[dim]测试三个典型场景的技术栈选型[/dim]",
        border_style="green"
    ))
    
    scenarios = [
        ("场景 1: 个人博客", test_scenario_1_blog),
        ("场景 2: 电商平台", test_scenario_2_ecommerce),
        ("场景 3: 企业后台", test_scenario_3_enterprise),
    ]
    
    results = []
    
    for name, scenario_func in scenarios:
        console.print("\n" + "="*80)
        state = scenario_func()
        success = run_test(name, state)
        results.append((name, success))
        console.print("="*80)
    
    # Summary
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]测试总结[/bold cyan]",
        border_style="cyan"
    ))
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "[green]✓ 通过[/green]" if success else "[red]✗ 失败[/red]"
        console.print(f"  {name}: {status}")
    
    console.print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        console.print("\n[bold green]✅ 所有测试通过！[/bold green]")
        return 0
    else:
        console.print("\n[bold red]❌ 部分测试失败[/bold red]")
        return 1


def run_full_workflow_test():
    """
    Run a full workflow test (requires API key).
    This is an example of how to test the complete workflow.
    """
    console.print("\n[bold yellow]完整工作流测试（需要 API Key）[/bold yellow]")
    
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        if not os.getenv("DEEPSEEK_API_KEY"):
            console.print("[yellow]⚠️  未配置 DEEPSEEK_API_KEY，跳过完整测试[/yellow]")
            return
        
        console.print("[green]✓ API Key 已配置[/green]")
        
        # Create a simple test state
        state = create_test_state(
            project_type="Web应用",
            team_size="1-3人（小型团队）",
            timeline="1个月内",
            special_requirements="测试项目"
        )
        
        console.print("[yellow]注意: 完整工作流测试需要交互式输入[/yellow]")
        console.print("[dim]请运行 'python cli.py' 进行完整测试[/dim]")
        
    except Exception as e:
        console.print(f"[red]测试准备失败: {str(e)}[/red]")


if __name__ == "__main__":
    try:
        exit_code = main()
        
        # Optionally run full workflow test
        run_full_workflow_test()
        
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  测试被中断[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n[red]❌ 发生错误: {str(e)}[/red]")
        sys.exit(1)
