# 项目架构概览

更新时间：2026-05-14 15:31 +08:00

## 总体结构

- 前端：Svelte 5 + SvelteKit 2 + Vite 5 + TypeScript + Tailwind CSS。
- 后端：FastAPI + Uvicorn + SQLAlchemy async + Peewee migrations + Socket.IO/WebSocket。
- 构建：Dockerfile 先在 Node 22 Alpine 阶段构建前端，再在 Python 3.11 slim 镜像中安装后端依赖并复制 `build/`。
- 包管理：前端使用 `package-lock.json`；Python 依赖在 `pyproject.toml`、`uv.lock` 和 `backend/requirements.txt` 中可见。

## 前端

- `src/routes/` 是 SvelteKit 页面入口：
  - `(app)`：主应用区域。
  - `auth`：认证页面。
  - `error`：错误页。
  - `s`：分享页。
  - `watch`：独立观看页。
- `src/lib/apis/`：前端调用后端 API 的封装入口。
- `src/lib/components/`：UI 组件，已按 `admin`、`app`、`chat`、`workspace`、`common` 等域分组。
- `src/lib/stores/`：前端状态管理。
- `src/lib/i18n/`：多语言资源，已存在 `zh-CN`、`zh-TW` 等 locale。
- `src/lib/workers/` 与 `src/lib/pyodide/`：浏览器侧 worker 和 Pyodide 相关能力。

## 后端

- `backend/open_webui/main.py` 是 FastAPI 应用装配入口：
  - 挂载 `/ws` 到 `open_webui.socket.main` 的 socket app。
  - 注册 Ollama、OpenAI、pipelines、tasks、images、audio、retrieval、auths、users、chats、models、knowledge、tools、skills、memories、files、groups、automations、calendar 等 router。
  - 挂载 `/static` 静态资源。
- `backend/open_webui/__init__.py` 提供 `open-webui serve` 和 `open-webui dev` CLI。
- `backend/open_webui/routers/` 是 HTTP API 接入层，负责请求参数、权限、路由编排。
- `backend/open_webui/models/` 是数据模型层，覆盖用户、聊天、文件、知识库、工具、提示词、分组、自动化等业务对象。
- `backend/open_webui/internal/` 包含数据库基础设施和迁移。
- `backend/open_webui/socket/` 负责 WebSocket/Socket.IO 通信和模型使用状态。
- `backend/open_webui/retrieval/` 与 `backend/open_webui/utils/` 承载 RAG、检索、外部集成和通用后端逻辑。

## 数据与存储

- 本地数据目录在 Dockerfile 中默认为 `/app/backend/data`。
- README 和 Dockerfile 都提示部署时要持久化后端数据目录，避免数据库和缓存丢失。
- 依赖显示支持 SQLite、PostgreSQL、MariaDB/MySQL 相关驱动，以及 Redis、对象存储、多个向量数据库。

## 外部集成热点

- LLM API：Ollama、OpenAI 兼容接口、Anthropic、Google GenAI、pipelines。
- RAG/检索：ChromaDB、OpenSearch、Qdrant、Milvus、Pinecone、Oracle、Azure Search 等依赖可见。
- 文件处理：PDF、Office、Markdown、OCR、音频转写、图像处理等依赖较多。
- 企业能力：OAuth、LDAP、SCIM、trusted headers、Redis session、OpenTelemetry 等模块在依赖和 router 中可见。

## 分层建议

- 新增后端 API 时优先在 `routers/` 做接入和权限校验，把复杂业务下沉到 `utils/`、专门 service 或已有模型层。
- 新增数据对象时先查 `models/` 与 `internal/migrations/` 的既有模式。
- 新增前端页面时优先沿用 `src/routes/(app)` 和 `src/lib/components` 的现有域分组。
- 涉及 WebSocket、任务池、会话池、模型缓存或后台任务时，先读 `backend/open_webui/socket/` 和 `backend/open_webui/utils/session_pool.py`。
