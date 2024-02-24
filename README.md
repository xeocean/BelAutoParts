# Инструкция

# Скачать и установить Python 
### https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
# Скачать и установить Git 
### https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe

### При установке добавить в переменную PATH

# Выполнить команды в командной строке (cmd):

### 1. cd D:/ 
### 2. git clone https://github.com/Workbook80/BelAutoParts
### 3. cd BelAutoParts
### 4. python -m venv venv
### 5. venv\Scripts\activate
### 6. pip install -r requirements.txt
### 7. npm ci
### 8. python manage.py migrate
### 9. python manage.py createsuperuser

# *Опционально: Импорт марок и моделей в базу
### 10. python json_to_db.py

# Запуск сервера:

### 11.  python manage.py runserver

### Сайт доступен http://127.0.0.1:8000

### Административная панель http://127.0.0.1:8000/admin
