# TashevGate — production gate для вайбкодинга

**TashevGate** отвечает на один практический вопрос:

> Можно ли двигать AI-собранный проект к production или уже сейчас есть очевидная блокирующая проблема?

Он не ставит проекту рекламный балл. Результат — **READY** или **BLOCKED**, плюс конкретные доказательства.

## Что проверяется в v0.1

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

## Запуск

```bash
git clone https://github.com/tashev11/tashevgate.git
cd tashevgate
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

tashevgate check /путь/к/проекту
```

## Встроить в свой GitHub-проект

```bash
cd project
tashevgate init
```

Команда добавит конфигурацию TashevGate, workflow GitHub Actions и безопасные строки в `.gitignore`.

## Автоисправление

```bash
tashevgate fix .
```

На первом этапе TashevGate специально исправляет только то, что можно изменить без понимания бизнес-логики. Например, он может добавить защиту секретных файлов и создать `.env.example` только с названиями переменных.

Он **не должен молча переписывать auth, платежи или базу данных**.

## Куда развиваем

Следующий большой этап — временно поднимать проект в sandbox и уже реально проходить:

**build → database → registration → login → permissions → migrations → backup → restore → browser smoke tests → release evidence**.

После этого TashevGate сможет стать настоящим предрелизным полигоном для вайбкодеров.
