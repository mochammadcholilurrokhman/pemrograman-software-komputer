# Cara Menjalankan Project Django + PostgreSQL

## 1. Clone Repository
```bash
git clone https://github.com/mochammadcholilurrokhman/pemrograman-software-komputer.git
cd nama-repository
```

## 2. Buat Virtual Environment
### Windows
```bash
python -m venv env
env\Scripts\activate
```

### Linux / Mac
```bash
python3 -m venv env
source env/bin/activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Setup PostgreSQL
Masuk ke PostgreSQL:
```bash
psql -U postgres
```

Buat database:
```sql
CREATE DATABASE nama_database;
```

## 5. Konfigurasi Database
Edit `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'frozeria',
        'USER': 'sesuai user anda',
        'PASSWORD': 'sesuai password anda',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 6. Jalankan Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

## 7. Jalankan Server
```bash
python manage.py runserver
```

Buka di browser:
```bash
http://127.0.0.1:8000/
```
