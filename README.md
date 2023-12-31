cd D:/ 
git clone https://github.com/Workbook80/BelAutoParts
cd BelAutoParts
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
npm ci
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Сайт доступен http://127.0.0.1:8000
Административная панель http://127.0.0.1:8000/admin
