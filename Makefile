install:
	cd backend && python -m pip install --upgrade pip && pip install -r requirements/dev.txt
	cd frontend && npm install

migrate:
	cd backend && python manage.py migrate

makemigrations:
	cd backend && python manage.py makemigrations

runserver:
	cd backend && python manage.py runserver

worker:
	cd backend && celery -A config worker -l info -P solo

frontend:
	cd frontend && npm run dev

test-backend:
	cd backend && pytest

test-frontend:
	cd frontend && npm test -- --run

lint-backend:
	cd backend && ruff check . && black --check .

lint-frontend:
	cd frontend && npm run lint

seed:
	cd backend && python ..\infra\scripts\seed_demo_data.py