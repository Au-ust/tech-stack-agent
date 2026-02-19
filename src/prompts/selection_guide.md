# 前端技术栈选型指南：不同规模项目的技术组合建议

## 概览与原则

- 以业务目标与团队约束为锚：交付速度、SEO、长期维护、多人协作、成本与性能。
- 优先简洁与可替换：尽量使用主流、生态成熟的方案，避免早期过度设计。
- 选型维度：框架与渲染模式、状态管理、路由与数据层、样式系统、工程化与质量、部署与监控。

## 渲染模式对比与选择

- **CSR**：首屏依赖 JS，适合后台与交互型应用；部署简单。
- **SSR**：服务器渲染首屏，SEO 与首屏体验更好；成本较高，需服务端运行环境。
- **SSG**：构建期静态生成，适合内容站点与文档；增量构建可降低发布成本。
- **ISR**：按需再生成，兼顾动态与静态；适合资讯/电商类页面。

**选择建议**：强 SEO/首屏 → SSR/SSG/ISR；复杂交互且登录后为主 → CSR。

## 项目规模划分

- **个人/原型**（1–3人，迭代快，上线验证为主）
- **中小型业务**（3–10人，持续交付，有SEO与稳定诉求）
- **中大型平台**（10人以上，多模块、多仓或工作区，跨团队协作）

## 小型项目技术组合（快速验证）

- **框架与构建**：Vite + Vue3 或 React + TS
- **路由**：Vue Router 或 React Router
- **状态管理**：轻量本地状态 + SWR/React Query 或 Pinia
- **数据请求**：Axios；Mock：Mock.js 就地造数
- **样式**：Tailwind CSS 或 UnoCSS；Icons 使用主流库
- **工程化**：ESLint + Prettier + Husky + lint-staged；Vitest 单测；Playwright 关键路径端到端
- **部署**：Vercel/Netlify；环境变量管理 .env
- **监控**：Sentry 前端错误上报；简单埋点 PV/UV
- **代码组织与约定**：src/features 分主题模块，复用型组件放 src/shared；服务层抽象 HTTP 与缓存策略。

示例 package.json 脚本：

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint --fix src",
    "test": "vitest run",
    "e2e": "playwright test"
  }
}
```

## 中小型业务技术组合（稳定与SEO）

- **渲染模式**：Next.js 或 Nuxt（SSR/SSG 混合，提升首屏与SEO）
- **状态管理**：React Query/SWR 或 Pinia；全局状态尽量少，用服务层抽象
- **数据层**：REST 为主，接口契约管理 Apifox；必要时 GraphQL（前后端协作明确）
- **样式系统**：Tailwind + Design Token；组件库 Ant Design 或 Element Plus
- **表单与校验**：React Hook Form/Yup 或 VeeValidate
- **i18n**：react-i18next 或 vue-i18n
- **工程化与质量**：Jest/Vitest 单测、Playwright 端到端、Commitlint、变更集管理 changelog
- **部署与CDN**：Cloudflare/Vercel；图片与静态资源走 CDN；灰度发布与预览环境
- **监控与可观测性**：Sentry、性能指标采集、埋点与行为回放可选
- **数据契约与错误策略**：统一响应模型，前端对 code/message/data 做解析；分类处理重试/降级；接口版本化避免破坏性更新。

示例 Next.js next.config.js：

```javascript
module.exports = {
  reactStrictMode: true,
  swcMinify: true,
  images: { domains: ["assets.example.com"] }
}
```

## 中大型平台技术组合（可扩展与治理）

- **组织形态**：Monorepo（pnpm workspaces + Turborepo）或多仓；共享包管理组件与工具集
- **框架**：按子系统选型，主站 SSR（Next/Nuxt），后台 SPA（Vue/React）
- **微前端**：谨慎引入 Module Federation 或 qiankun，用在跨团队、不同栈共存的场景
- **状态管理**：跨模块事件流与数据契约优先；必要时 Redux Toolkit 或 RxJS 管理复杂异步
- **数据层**：统一请求封装与错误策略；GraphQL 网关或 BFF（Nest.js/Express）
- **样式与设计系统**：Design Token + 自定义主题；Storybook 作为组件资产中心
- **质量与治理**：单测/端到端覆盖、变更集发布、强制评审与受保护主干、版本与发布日志
- **构建与性能**：按路由与模块分包，资源预取与懒加载，图片与字体优化，监控 TTI/INP/LCP
- **安全与合规**：CSP、依赖漏洞扫描、隐私合规与审计
- **发布与版本策略**：工作区包使用 Changesets 管理版本与 changelog；主站采用灰度与回滚；组件库发布前走可视化对比与基准测试。

Monorepo turbo.json 片段：

```json
{
  "pipeline": {
    "lint": { "outputs": [] },
    "test": { "outputs": [] },
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**"] }
  }
}
```

## 选型决策清单

- 强 SEO 与内容站点：SSR/SSG（Next/Nuxt）优先；静态资源 CDN；预渲染与增量构建
- 交互复杂但 SEO 次要：SPA（Vite + Vue/React）+ 良好分包与懒加载
- 团队多人协作与共享组件：Monorepo + Storybook + 设计令牌；规范提交与版本管理
- 数据复杂、协同开发：GraphQL 或 BFF；在前端以 React Query/Pinia 管理缓存与错误
- 移动端混合场景：轻量 H5 用 SPA；需要原生能力考虑 Capacitor/Tauri
- 低预算快速交付：Vercel/Netlify 托管与自动预览；选择开源组件库与工具链
- **框架选择提示**：Vue 生态在中后台与国内团队支持更强；React 生态在数据可视化与跨端方案更丰富。对 SSR 友好度与团队熟悉度优先。

## 性能与稳定性要点

- **分包策略**：路由级与组件级 Lazy；分析 Bundle 体积并移除未用依赖
- **资源优化**：图片压缩与现代格式、字体子集化、CSS 样式隔离
- **运行时优化**：列表虚拟化、避免不必要的重渲染、合并网络请求
- **监控闭环**：采集 Web Vitals、错误率与慢接口，建立报警与回归用例

构建优化示例（Vite）：

```javascript
// vite.config.js 片段
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'react']
        }
      }
    }
  }
}
```

## 迁移与演进建议

- 保持可替换：数据层与视图解耦；减少对特定框架的深度耦合
- 渐进演进：从 SPA 升级 SSR 可先做关键路由的预渲染
- 文档与约定：将约定沉淀到团队文档与脚手架，降低新人上手成本
- 渐进 SSR 示例（Next.js）：仅为营销页开启 SSG/ISR，其余仍为 CSR，降低迁移风险。

## 场景化组合建议

- **内容站点与文档**：VitePress/Nuxt Content + SSG/ISR + Algolia；图像与静态资源走 CDN。
- **中后台管理**：Vue3 + Vite + Element Plus 或 React + Ant Design；CSR，强调表单与表格效率。
- **复杂交互应用（可视化/编辑器）**：React + Zustand/Redux Toolkit + Canvas/WebGL；按需 SSR。
- **组件库与平台**：Monorepo + Storybook + Changesets；按包发布与版本治理。
