@AGENTS.md

## Claude Code

Правила проекта — в AGENTS.md (подключён импортом выше).

- Скиллы: `.claude/skills/interview-me`, `.claude/skills/implement`.
- Роли скилла implement — субагенты из `.claude/agents/`:
  `demo-implementer`, `demo-test-writer`, `demo-test-runner`, `demo-auditor`.
  Запускай их через инструмент Agent с `subagent_type` равным имени роли, строго по одной.
- Plan mode: `/plan` или Shift+Tab.
- Для Codex те же скиллы лежат в `.agents/skills`, роли — в `.codex/agents`.
