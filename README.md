# Лаба 1: монолит + Docker + GitHub Actions

Минимальный пример: Flask, Docker, тесты в CI, публикация в **Docker Hub**, деплой на **self-hosted runner** (команды `docker pull` / `docker run` выполняются на твоей машине, например WSL Ubuntu).

## Что внутри

| Файл | Зачем |
|------|--------|
| `app.py` | Веб-приложение (две страницы: `/` и `/health`) |
| `requirements.txt` | Зависимости для компьютера и CI (Flask + pytest) |
| `requirements-app.txt` | Только Flask — ставится в Docker-образ |
| `Dockerfile` | Сборка образа |
| `tests/test_app.py` | Простые тесты |
| `.github/workflows/ci-cd.yml` | Пайплайн при пуше в `main` |

## Локально (Windows)

```powershell
cd "путь\к\папке\проекта"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = "app.py"
python -m flask run
```

Открой в браузере: http://127.0.0.1:5000/

Тесты:

```powershell
pytest
```

Docker на своём ПК:

```powershell
docker build -t lab1-app:local .
docker run --rm -p 5000:5000 lab1-app:local
```

## GitHub

1. Создай репозиторий, залей эту папку, ветка **`main`**.
2. В **Settings → Secrets and variables → Actions** добавь секреты:

| Секрет | Что положить |
|--------|----------------|
| `DOCKERHUB_USERNAME` | Логин Docker Hub |
| `DOCKERHUB_TOKEN` | Токен: Docker Hub → Personal access tokens (Read & Write) |

3. В Docker Hub создай репозиторий **`lab1-app`** (как в workflow). Публичный образ проще; если приватный — деплой всё равно залогинится токеном.

## Self-hosted runner (WSL Ubuntu — как у многих в лабе)

Деплой идёт **на ту же машину**, где крутится runner: после пуша job **deploy** выполняет `docker pull` и `docker run` локально.

1. **WSL**: `wsl --install -d Ubuntu` (если ещё нет). В Ubuntu:
   ```bash
   sudo apt update && sudo apt install -y docker.io
   sudo usermod -aG docker $USER
   ```
   Выйди из сессии WSL и зайди снова. Проверка: `docker ps`.

2. **Docker Desktop** (Windows): Settings → Resources → WSL Integration → включи **Ubuntu**.

3. **Регистрация runner** в репозитории на GitHub: **Settings → Actions → Runners → New self-hosted runner** → выбери **Linux** и **x64**, скопируй команды.

   В WSL (в домашней папке, например `~/actions-runner`):
   ```bash
   mkdir ~/actions-runner && cd ~/actions-runner
   # вставь curl и tar из инструкции GitHub
   ./config.sh --url https://github.com/ВЛАДЕЛЕЦ/РЕПО --token ОДНОРАЗОВЫЙ_ТОКЕН_ИЗ_СТРАНИЦЫ
   ```
   На вопросы можно Enter (default), имя runner — любое (например `wsl-lab`).

4. **Запуск runner** (пока окно открыто — runner онлайн):
   ```bash
   ./run.sh
   ```
   Для фона: `./svc.sh install && ./svc.sh start` (см. подсказки на странице GitHub после `config.sh`).

5. Пуш в **`main`**: в **Actions** должны пройти **test** → **build-push** → **deploy**. Контейнер слушает **порт 80** внутри **WSL**. Открыть в браузере Windows: адрес **IP WSL** (команда в WSL: `hostname -I`, первый адрес), например `http://172.x.x.x/`. Либо настрой проброс; для проверки из WSL: `curl -s http://127.0.0.1/`.

Если **порт 80** занят или нужны права — в workflow можно заменить `80:5000` на `8080:5000` и открывать `http://IP:8080/`.

## Отчёт по заданию (кратко)

1. Приложение — Flask (`app.py`).
2. Контейнер — `Dockerfile`.
3. CI/CD — GitHub Actions: тесты, сборка, Docker Hub, деплой на **self-hosted runner** (`docker pull` / `docker run` на машине с runner).
