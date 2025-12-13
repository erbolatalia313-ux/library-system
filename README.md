Проект атауы
# Library System Backend

2️.Проект сипаттамасы
Бұл жоба — FastAPI негізінде жасалған кітапхана жүйесінің backend API.

3️.Қолданылған технологиялар
## Технологиялар
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy
- Docker, docker-compose
- Pytest

4️🚀 Іске қосу нұсқаулығы (ЕҢ МАҢЫЗДЫ)
## Іске қосу

1. Репозиторийді клондау:
git clone https://github.com/erbolatalia313-ux/library-system.git
cd library-system

2. Docker арқылы іске қосу:
docker-compose up --build

3. API қолжетімді:
http://localhost:8000

4. Swagger UI:
http://localhost:8000/docs
5.Seed деректер
## Seed деректер
Админ аккаунт seed_data.py арқылы қосылады:
email: admin@example.com
password: admin123

6.Тесттерді іске қосу
## Тесттер
docker exec -it library_backend python -m pytest

7️.GitHub сілтемесі
## Репозиторий
https://github.com/erbolatalia313-ux/library-system
