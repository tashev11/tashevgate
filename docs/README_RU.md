<p align="center">
  <img src="assets/hero.svg" alt="TashevGate — production gate для AI-собранного ПО" width="100%">
</p>

# TashevGate — production gate для вайбкодинга

**TashevGate** отвечает на один практический вопрос:

> Можно ли двигать AI-собранный проект к production или уже сейчас есть очевидная блокирующая проблема?

Результат — **READY** или **BLOCKED**, плюс конкретные доказательства. Без рекламного рейтинга и «87/100 безопасности».

<p align="center">
  <img src="assets/validation.svg" alt="Проверка релиза TashevGate v0.1" width="100%">
</p>

## Что проверяется в v0.1

<p align="center">
  <img src="assets/rule-matrix.svg" alt="Категории встроенных правил TashevGate" width="100%">
</p>

- реальные секреты и private keys в проекте;
- `.env` внутри репозитория;
- секреты, случайно вынесенные в публичные переменные frontend;
- разрушительные SQL-миграции;
- защита `.gitignore`;
- lock-файлы зависимостей;
- наличие тестов и CI;
- наличие backup + rollback процесса при миграциях;
- включённый debug;
- wildcard CORS;
- подозрительные admin routes без очевидного auth-маркера.

Всего в v0.1 — **18 встроенных правил**.

## Как принимается решение

<p align="center">
  <img src="assets/pipeline.svg" alt="Как TashevGate принимает решение READY или BLOCKED" width="100%">
</p>

TashevGate сначала собирает факты, затем применяет выбранную политику релиза.

```text
репозиторий
   ↓
проверки и доказательства
   ↓
политика проекта
   ↓
READY / BLOCKED
   ↓
Console / Markdown / JSON / SARIF
```

## Запуск

```bash
git clone https://github.com/tashev11/tashevgate.git
cd tashevgate

python3 -m venv .venv
source .venv/bin/activate
pip install -e .

tashevgate check /путь/к/проекту
```

<p align="center">
  <img src="assets/terminal.svg" alt="Пример работы TashevGate в терминале" width="92%">
</p>

## Встроить в свой GitHub-проект

```bash
cd project

tashevgate init
tashevgate check .
```

Команда `tashevgate init` добавит:

- `.tashevgate.yml`;
- workflow GitHub Actions;
- безопасные строки для секретных файлов в `.gitignore`.

Существующая конфигурация не перезаписывается.

## GitHub Action

```yaml
- uses: actions/checkout@v4

- uses: tashev11/tashevgate@v0.1.0
  with:
    path: "."
    fail-on: "blocker"
```

Если найден блокирующий риск — job завершается ошибкой и релиз можно остановить автоматически.

## Автоисправление

```bash
tashevgate fix .
```

На первом этапе TashevGate исправляет только то, что можно изменить **детерминированно и безопасно**.

Например:

- добавляет защиту `.env` и private keys;
- создаёт `.env.example` только с названиями переменных;
- никогда не копирует значения секретов.

Он **не должен молча переписывать auth, платежи или базу данных**.

## Форматы отчётов

TashevGate умеет выдавать:

- **Console** — для разработчика;
- **Markdown** — для аудита и документации;
- **JSON** — для агентов и автоматизации;
- **SARIF 2.1.0** — для GitHub/code scanning.

## Куда развиваем

Следующий большой этап — реальный **staging sandbox**:

**build → database → registration → login → permissions → migrations → backup → restore → browser smoke tests → release evidence**

Дальше:

- framework-aware auth для Next.js / FastAPI / Supabase;
- Docker и IaC проверки;
- supply-chain проверки;
- PR diff/baseline режим;
- автоматический deploy + health check + rollback;
- **Vibe Certificate** — проверяемое доказательство готовности проекта.

После этого TashevGate станет не просто сканером, а **предрелизным полигоном для вайбкодеров**.

## Полезные ссылки

- [Главный README](../README.md)
- [Все правила](../RULES.md)
- [Архитектура](../ARCHITECTURE.md)
- [Roadmap](../ROADMAP.md)
- [Security](../SECURITY.md)
- [Issues](https://github.com/tashev11/tashevgate/issues)
- [Релиз v0.1.0](https://github.com/tashev11/tashevgate/releases/tag/v0.1.0)
