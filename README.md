# CineGame - system rekomendacji filmów i gier

Projekt Django przygotowany jako aplikacja katalogowo-rekomendacyjna dla filmów
i gier. Schemat bazy danych jest zarządzany przez migracje Django.

## Uruchomienie

1. Utwórz środowisko wirtualne:

```powershell
python -m venv .venv
```

2. Aktywuj środowisko:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Zainstaluj zależności:

```powershell
pip install -r requirements.txt
```

4. Skopiuj plik konfiguracyjny:

```powershell
copy .env.example .env
```

5. Wykonaj migracje:

```powershell
python manage.py migrate
```

6. Uruchom aplikację:

```powershell
python manage.py runserver
```

## Baza danych

Domyślnie projekt może działać na SQLite, co ułatwia uruchomienie i sprawdzanie
pracy na świeżym komputerze. Jeśli chcesz użyć MySQL, ustaw w `.env`:

```env
DB_ENGINE=mysql
DB_NAME=recommender_db
DB_USER=root
DB_PASSWORD=your-database-password
DB_HOST=127.0.0.1
DB_PORT=3307
```

Aktualnym źródłem prawdy dla schematu są modele w aplikacji `recommender` oraz
migracje Django. Ręczne skrypty SQL w katalogu `database` należy traktować jako
materiał pomocniczy lub archiwalny.

## Testy

```powershell
python manage.py test
```
