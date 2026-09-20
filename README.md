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

- Yangi foydalanuvchi ro'yxatdan o'tganda **avtomatik xabar**
- O'qituvchi yangi savol qo'shganda **avtomatik xabar** (tekshiruvda)
- `/stats` — kunlik statistika (foydalanuvchilar, savollar, faollik)

Qo'lda ishga tushirish:

```bash
cd backend
python manage.py tg_send "Assalomu alaykum!"
python manage.py tg_stats                 # kunlik statistika
python manage.py telegram_poll            # botni uzluksiz ishga tushiradi
```

> Har kuni avtomatik statistika uchun: `python manage.py tg_stats` ni cron
> (masalan `0 9 * * *`) ga qo'ying.

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
git clone <repo-url> abuturend
cd abuturend
cp .env.example .env
# .env ichida DJANGO_SECRET_KEY, POSTGRES_PASSWORD va domenlarni o'rnating
docker compose up -d --build
```

Nginx `nginx/nginx.conf` reverse-proxy sifatida `frontend:3000` ga yo'naltiradi;
HTTPS Let's Encrypt orqali yoki yuqori qatlamda qo'shiladi.

## Status

- PHASE 1 (Foundation): ✅ backend check + migratsiya + health / frontend build + lint + i18n + landing
- PHASE 2 (Authentication): ✅ session-based auth (register/login/logout/me/change-password/csrf), 7 test PASS, protected pages
- PHASE 3 (Subjects/Topics): ✅ Subject/Topic/Subtopic modellari + API + admin + seed_catalog (13 DTM fani), 7 test PASS, subjects ro'yxati + detail sahifalari
- PHASE 4 (Question bank): ✅ Question/QuestionOption modellari, o'qituvchi CRUD + student browse (javobsiz), difficulty/explanation/source_type, 7 test PASS, teacher/questions panel, 21 umumiy backend test
- PHASE 5 (Practice engine): ✅ `practice` app — practice/exam session, immediate feedback + explanation, finish report; 8 test PASS; PracticePlayer (klaviatura qo'llab-quvvatlash A–D/Enter, streak, score ring)
- PHASE 6 (Analytics): ✅ `GET /api/stats/summary/` — accuracy, streak, weekly activity, subject breakdown, weak topics, recent sessions; `GET /api/sessions/` list; Dashboard real statistika asosida (Eduva uslubi), subjects katalog izlash + premium kartalar, auth split-screen (Figma mos template'laridan qilingan dizayn upgrade)
- PHASE 7 (Universities): ✅ `universities` app — University/Direction modellari + admin + seed_universities + `GET /api/universities/`, `/{slug}/`, `/api/directions/?subject=`; universite katalogi: izlash, fan kesimida filter, ochiluvchi yo'nalishlar (fanlar + davomiylik)
- PHASE 8 (Mock exam): ✅ Sinov imtihoni oqimi — fan/count/vaqt tanlash, taymer (avtomatik yakunlanadi), bepul navigatsiya (`/sessions/{id}/questions/` javob yashirilgan), yakunlanishda score ring + har bir savol bo'yicha tahlil, natijalar tarixi (`/sessions/` exam filter)
- Backend test: **46/46 PASS** (uni katalogi 6, session report/questions 2 yangi testlar bilan)
- Landing: ✅ 3 ta theme-aware SVG illyustratsiya, aurora/grid hero, scroll reveal
- API indeks: ✅ `GET /api/` — barcha endpointlar katalogi (resolve testi bilan himoyalangan); security header'lar (CSP/RP/Permissions-Policy)