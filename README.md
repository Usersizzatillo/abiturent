# Abiturend — DTM / ABITURIYENT PLATFORM

Abituriyentlar uchun ta'lim, test, imtihon, natija, progress, universitet va yo'nalish
ma'lumotlarini boshqaruvchi zamonaviy platforma.

## Texnologik stack

| Layer     | Texnologiya                          |
| --------- | ------------------------------------ |
| Frontend  | Next.js 16 (App Router, TypeScript)  |
| Backend   | Django 6 + Django REST Framework      |
| Database  | PostgreSQL 17                        |
| Auth      | Session-based cookies (DRF)          |
| i18n      | next-intl (O'zbek / Русский / English)|
| Deploy    | Docker Compose + Nginx               |

## Tuzilma

```text
├── backend/          # Django REST API
│   ├── config/       # settings / urls
│   ├── core/         # tayanch app (health, izoh)
│   ├── telegrambot/  # Telegram admin bot (bildirishnomalar + statistika)
│   └── requirements.txt
├── frontend/         # Next.js ilova
│   ├── app/[locale]/ # sahifalar (uz/ru/en)
│   ├── components/   # UI kit va layout
│   ├── i18n/         # routing / request
│   └── messages/     # tarjimalar
├── nginx/nginx.conf  # production reverse-proxy
└── docker-compose.yml
```

## Lokal ishga tushirish

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
# PostgreSQL mavjud bo'lsa: POSTGRES_PASSWORD muhitini o'rnating
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Healthcheck: `GET http://127.0.0.1:8000/api/health/`

### Telegram bot

`.env` da token va chat id ko'rsatilgach ishlaydi:

| Env                        | Tavsif                                  |
| -------------------------- | --------------------------------------- |
| `TELEGRAM_BOT_TOKEN`       | `@BotFather` -> `/newbot` orqali olinadi |
| `TELEGRAM_CHAT_ID`         | Admin chat id (`@userinfobot`)           |
| `TELEGRAM_ALLOWED_CHAT_IDS`| Vergul bilan qo'shimcha chat id'lar      |
| `TELEGRAM_WEBHOOK_SECRET`  | Webhook xavfsizlik kaliti (ixtiyoriy token) |
| `TELEGRAM_WEBHOOK_HOST`    | Domen (masalan `abituriyent.orgtrace.uz`) |

- Yangi foydalanuvchi ro'yxatdan o'tganda **avtomatik xabar**
- O'qituvchi yangi savol qo'shganda **avtomatik xabar** (tekshiruvda)
- `/stats` — kunlik statistika (foydalanuvchilar, savollar, faollik)
- `/trend` — so'nggi 7 kun faolligi
- `/help` — buyruqlar ro'yxati, `/id` — chat ID

Arxitektura: **webhook** asosida — Telegram `/webhooks/telegram/` ga to'g'ridan-to'g'ri
POST yuboradi (polling servisi shart emas). Webhook deploy paytida avtomatik ro'yxatdan
o'tkaziladi:

```bash
cd backend
python manage.py tg_set_webhook --drop          # webhook bekor qilish
python manage.py tg_set_webhook                 # domenni ALLOWED_HOSTS/`TELEGRAM_WEBHOOK_HOST` dan o'qiydi
python manage.py tg_set_webhook --url https://domen/webhooks/telegram/
```

Qo'lda xabar yuborish:

```bash
python manage.py tg_send "Assalomu alaykum!"
python manage.py tg_stats                 # kunlik statistika
python manage.py tg_monitor               # uptime tekshiruvi (nosozlikda xabar)
```

> Har kuni avtomatik statistika uchun: `python manage.py tg_stats` ni cron
> (masalan `0 9 * * *`) ga qo'ying. Monitoring: `*/5 * * * *` da `tg_monitor`.
>
> Lokal sinov uchun polling rejimi hali ham mavjud:
> `python manage.py telegram_poll`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Ochiq: `http://localhost:3000` (avtomatik `/uz` ga yo'naltiriladi).

### 3. Docker (to'liq stack)

```bash
cp .env.example .env   # keyin kerakli qiymatlarni o'zgartiring
docker compose up -d --build
```

## Production deploy

Serverda:

```bash
git clone <repo-url> abiturend
cd abiturend
cp .env.example .env
# .env ichida DJANGO_SECRET_KEY, POSTGRES_PASSWORD va domenlarni o'rnating
docker compose up -d --build
```

Nginx `nginx/nginx.conf` reverse-proxy sifatida `frontend:3000` ga yo'naltiradi;
HTTPS Let's Encrypt orqali yoki yuqori qatlamda qo'shiladi.

### Avtomatik deploy (CI/CD)

`.github/workflows/deploy.yml` — `main` branch'ga push bo'lganida avtomatik
deploy'laydi. GitHub repo settings → Secrets and variables → Actions:

| Secret            | Tavsif                                  |
| ----------------- | --------------------------------------- |
| `DEPLOY_HOST`     | Server IP (masalan `189.74.97.158`)     |
| `DEPLOY_USER`     | SSH foydalanuvchi (masalan `root`)      |
| `DEPLOY_PORT`     | SSH port (ixtiyoriy, default `22`)      |
| `DEPLOY_SSH_KEY`  | Serverdagi `~/.ssh/authorized_keys` ga qo'yilgan **private** SSH key |

Oqim avtomatik: pull → build → migrate → collectstatic → webhook o'rnatish.

### Monitoring

`python manage.py tg_monitor` sayt va API uptime'ni tekshiradi; nosozlik
topilsa Telegramga xabar yuboradi. Serverda crontab orqali ishga tushiriladi:

```text
*/5 * * * * root docker exec $(docker ps -qf name=abiturend-backend) python manage.py tg_monitor
```

Kunlik statistika (har kuni 09:00):

```text
0 9 * * * root docker exec $(docker ps -qf name=abiturend-backend) python manage.py tg_stats
```

## Status

- PHASE 1 (Foundation): ✅ backend check + migratsiya + health / frontend build + lint + i18n + landing
- PHASE 2 (Authentication): ✅ session-based auth (register/login/logout/me/change-password/csrf), 7 test PASS, protected pages
- PHASE 3 (Subjects/Topics): ✅ Subject/Topic/Subtopic modellari + API + admin + seed_catalog (13 DTM fani), 7 test PASS, subjects ro'yxati + detail sahifalari
- PHASE 4 (Question bank): ✅ Question/QuestionOption modellari, o'qituvchi CRUD + student browse (javobsiz), difficulty/explanation/source_type, 7 test PASS, teacher/questions panel, 21 umumiy backend test
- PHASE 5 (Practice engine): ✅ `practice` app — practice/exam session, immediate feedback + explanation, finish report; 8 test PASS; PracticePlayer (klaviatura qo'llab-quvvatlash A–D/Enter, streak, score ring)
- PHASE 6 (Analytics): ✅ `GET /api/stats/summary/` — accuracy, streak, weekly activity, subject breakdown, weak topics, recent sessions; `GET /api/sessions/` list; Dashboard real statistika asosida (Eduva uslubi), subjects katalog izlash + premium kartalar, auth split-screen (Figma mos template'laridan qilingan dizayn upgrade)
- PHASE 7 (Universities): ✅ `universities` app — University/Direction modellari + admin + seed_universities + `GET /api/universities/`, `/{slug}/`, `/api/directions/?subject=`; universite katalogi: izlash, fan kesimida filter, ochiluvchi yo'nalishlar (fanlar + davomiylik)
- PHASE 8 (Mock exam): ✅ Sinov imtihoni oqimi — fan/count/vaqt tanlash, taymer (avtomatik yakunlanadi), bepul navigatsiya (`/sessions/{id}/questions/` javob yashirilgan), yakunlanishda score ring + har bir savol bo'yicha tahlil, natijalar tarixi (`/sessions/` exam filter)
- PHASE 9 (MCP): ✅ `mcpbridge` — Streamable HTTP transport `/mcp/`, 11 tool test PASS, docker `mcp` servisi + nginx proxy
- Backend test: **73/73 PASS** (accounts 8, catalog 7, core 4, questions 9, practice 18, universities 6, telegrambot 10, MCP 11)
- Landing: ✅ 3 ta theme-aware SVG illyustratsiya, aurora/grid hero, scroll reveal
- API indeks: ✅ `GET /api/` — barcha endpointlar katalogi (resolve testi bilan himoyalangan); security header'lar (CSP/RP/Permissions-Policy)