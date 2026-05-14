# 开发与验证指南

更新时间：2026-05-14 15:31 +08:00

## 环境要求

- Node.js：`>=18.13.0 <=22.x.x`。
- npm：`>=6.0.0`。
- Python：`>=3.11, <3.13.0a1`。
- Windows 下执行 npm 命令优先使用 `npm.cmd`，避免 PowerShell 执行策略拦截。

## 前端开发

- 安装依赖：`npm.cmd ci`
- 启动开发服务器：`npm.cmd run dev`
- 指定端口：`npm.cmd run dev:5050`
- 构建：`npm.cmd run build`
- 预览构建产物：`npm.cmd run preview`
- 类型与 Svelte 检查：`npm.cmd run check`
- 前端单测：`npm.cmd run test:frontend`

注意：`dev` 和 `build` 会先执行 `npm run pyodide:fetch`，对应脚本是 `scripts/prepare-pyodide.js`。

## 后端开发

- 后端 CLI 入口：`backend/open_webui/__init__.py`。
- 默认服务命令：`open-webui serve`，默认监听 `0.0.0.0:8080`。
- 开发服务命令：`open-webui dev`，默认 `reload=True`。
- Python 依赖和约束主要看 `pyproject.toml`、`uv.lock`、`backend/requirements.txt`。

## 格式化与检查

- 综合 lint：`npm.cmd run lint`
- 前端 eslint：`npm.cmd run lint:frontend`
- 类型检查：`npm.cmd run lint:types`
- 后端 pylint：`npm.cmd run lint:backend`
- 前端格式化：`npm.cmd run format`
- 后端格式化：`npm.cmd run format:backend`

## 测试入口

- Cypress E2E：`npm.cmd run cy:open`
- 前端 Vitest：`npm.cmd run test:frontend`
- 后端 Python 测试依赖在 `pyproject.toml` 的 `dependency-groups.dev` 和 optional `all` 中可见，例如 `pytest`、`pytest-asyncio`、`pytest-docker`。

## Docker 与部署

- `Dockerfile` 使用多阶段构建：Node 构建前端，Python 镜像运行后端。
- `docker-compose.yaml` 是默认 compose 入口，另有 GPU、AMD GPU、OpenTelemetry、Playwright、API、data 等变体 compose 文件。
- `Makefile` 封装了 `install`、`start`、`stop`、`startAndBuild`、`update`。

## 风险提示

- 不要把 `.webui_secret_key`、API key、数据库文件、私有地址写入知识库或提交。
- 涉及 `backend/open_webui/config.py`、认证、权限、SCIM、文件访问、终端、代码执行、工具调用时，默认视为高风险改动，需要更细验证。
- 涉及数据库模型和迁移时，先确认 `models/`、`internal/migrations/`、Alembic/Peewee 迁移路径的关系。
- README 在当前 PowerShell 输出存在乱码，做文档沉淀时优先从源码、配置和可验证命令提取事实。
