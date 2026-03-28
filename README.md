# Лаба 1: монолит + Docker + GitHub Actions

Минимальный пример: маленькое приложение на Flask, контейнер, тесты в CI, публикация в **Docker Hub**, деплой на сервер по **SSH** (без Ansible).

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
| `DOCKERHUB_TOKEN` | Токен: Docker Hub → Account Settings → Security → New Access Token |
| `SERVER_HOST` | IP или домен сервера |
| `SERVER_USER` | Логин SSH (например `ubuntu` или `root`) |
| `SERVER_SSH_KEY` | **Приватный** ключ OpenSSH (содержимое файла `id_rsa`), без пароля на ключ |

3. Образ в Docker Hub сделай **публичным** (или на сервере один раз выполни `docker login` вручную — для лабы проще публичный репозиторий).

## Сервер (Ubuntu-подобный)

На машине должны быть установлены Docker и право пользователю запускать `docker` без пароля (часто так: `sudo usermod -aG docker $USER` и перелогиниться).

После пуша в `main` GitHub сам: запустит тесты → соберёт образ → отправит в Docker Hub → по SSH обновит контейнер. Сайт слушает **порт 80** на сервере.

## Отчёт по заданию (кратко)

1. Приложение — Flask (`app.py`).
2. Контейнер — `Dockerfile`.
3. CI/CD — GitHub Actions: тесты, сборка, Docker Hub, деплой через SSH-команды (`docker pull` / `docker run`).
