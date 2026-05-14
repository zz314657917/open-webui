# Open WebUI 项目知识入口

更新时间：2026-05-14 15:31 +08:00

## 项目定位

- 本仓库是 `open-webui`，一个自托管 AI Web UI 平台。
- 本地扫描确认技术栈为 SvelteKit/Vite 前端 + FastAPI/Python 后端。
- 仓库当前没有项目级 `AGENTS.md`，后续会话应先读本文件，再按任务类型补读相关知识文件。

## 优先读取顺序

1. `knowledge/00-start-here.md`：项目入口、常用命令和知识索引。
2. `knowledge/project-architecture.md`：前后端结构、路由、数据模型和部署入口。
3. `knowledge/development-guide.md`：本地开发、验证、格式化和风险提示。
4. `knowledge/release-highlights.md`：最近版本新增功能摘要，适合快速了解项目最近能力变化。
5. `knowledge/tasks/current-task.md`：当前任务快照，只记录正在做什么和下一步。
6. `knowledge/tasks/timeline.md`：阶段时间轴，记录重要扫描、决策、验证和遗留问题。

## 主要目录

- `src/`：SvelteKit 前端源码。
- `src/routes/`：页面路由，包含 `(app)`、`auth`、`error`、`s`、`watch`。
- `src/lib/`：前端 API、组件、状态、工具、i18n、workers 等共享代码。
- `backend/open_webui/`：Python 后端包。
- `backend/open_webui/main.py`：FastAPI 应用组装入口，挂载 WebSocket、API router 和静态资源。
- `backend/open_webui/routers/`：后端 HTTP API 接入层。
- `backend/open_webui/models/`：后端数据模型层。
- `backend/open_webui/internal/`：数据库、迁移等内部基础设施。
- `backend/open_webui/utils/`：后端工具、集成和服务型逻辑。
- `cypress/`：端到端测试。
- `docs/`：项目文档。
- `scripts/`：构建辅助脚本，例如 Pyodide 资源准备。

## 常用命令

- 安装依赖：`npm.cmd ci`
- 前端开发：`npm.cmd run dev`
- 指定端口前端开发：`npm.cmd run dev:5050`
- 前端构建：`npm.cmd run build`
- Svelte/TypeScript 检查：`npm.cmd run check`
- 前端测试：`npm.cmd run test:frontend`
- 综合 lint：`npm.cmd run lint`
- Python 后端格式化：`npm.cmd run format:backend`
- Docker Compose 启动：`docker compose up -d` 或 `make install`

## 入口事实

- `package.json` 声明版本为 `0.9.5`，Node 支持范围为 `>=18.13.0 <=22.x.x`。
- `pyproject.toml` 要求 Python `>=3.11, <3.13.0a1`。
- `backend/open_webui/__init__.py` 提供 Typer CLI，`open-webui serve` 默认监听 `0.0.0.0:8080`。
- `svelte.config.js` 使用 `@sveltejs/adapter-static`，构建输出目录为 `build`，fallback 为 `index.html`。
- `vite.config.ts` 注入 `APP_VERSION` 和 `APP_BUILD_HASH`，并复制 `onnxruntime-web` wasm 资源。

## 维护规则

- 修改业务前先读相关前后端入口，优先遵循项目已有分层。
- 不把密钥、token、私有地址、账号写入 `knowledge/`。
- 时间轴只记录高信号事实、关键决策、验证记录和遗留问题；当前工作状态写 `current-task.md`。
- README 在当前终端显示存在乱码字符，知识库内容优先基于配置文件和源码扫描结果。
