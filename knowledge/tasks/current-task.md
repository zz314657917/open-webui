# 当前任务快照

更新时间：2026-05-15 00:00 +08:00

## 当前阶段

已完成项目初始扫描，当前在整理最近版本的新功能，并把可复用的功能变化沉淀到知识库。

## 已确认事实

- 仓库路径：`F:/java/open-webui-main`。
- 项目无现成 `AGENTS.md`，此前无 `knowledge/` 目录。
- 项目为 Open WebUI，本地配置显示前端是 SvelteKit/Vite，后端是 FastAPI/Python。
- 已读取入口配置：`package.json`、`pyproject.toml`、`README.md`、`Dockerfile`、`Makefile`、`svelte.config.js`、`vite.config.ts`、`backend/open_webui/main.py`、`backend/open_webui/__init__.py`。
- README 在当前终端显示有乱码字符，本次知识库不引用不可读字符内容。

## 本轮产物

- `knowledge/00-start-here.md`
- `knowledge/project-architecture.md`
- `knowledge/development-guide.md`
- `knowledge/release-highlights.md`
- `knowledge/tasks/current-task.md`
- `knowledge/tasks/timeline.md`

## 下一步

- 如继续整理新功能，优先补充 `knowledge/release-highlights.md` 和相关入口源码。
- 如要修 bug，补读相关 router/model/component，并运行最小验证命令。
- 如要长期维护知识库，后续阶段结束时追加 `knowledge/tasks/timeline.md`，当前工作状态更新本文件。
