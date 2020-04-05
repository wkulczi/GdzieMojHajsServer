### Jak uruchomić serwer GdzieMójHajs

###### 1.1 Konfiguracja bazy danych
- zainstaluj postgresql [tutorial linux](https://tecadmin.net/install-postgresql-server-on-ubuntu/)/[dl link Win](https://www.postgresql.org/download/windows/)
- uruchom psql
- utwórz bazę danych (`CREATE DATABASE nazwa;`) 
- ustaw hasło do użytkownika psql (będąc w konsoli psql: `\password <hasło>`) [tylko linux, win ma defaultowe 'postgres']

###### 1.2 Konfiguracja PyCharma
- dodaj nowy interpreter (venv)
- kliknij w plik `requirements'
- pobierz paczki z requirements, `pip install -r requirements.txt` (albo zainstaluj plugin 'requirements' i kliknij żeby sam pobrał)
- wejdź w edycję ustawień (Run/Debug Configurations)
- znajdź sekcję environment i kliknij w tym okienku tę małą ikonkę
![](https://i.ibb.co/ByPFwKP/Adnotacja-2020-04-04-111958.png)
- dodaj zmienne środowiskowe 
![](https://i.ibb.co/d0znpyb/Adnotacja-2020-04-04-112316.png)

`export FLASK_APP=app.py;`
`export FLASK_DEBUG=1;`
`export SQLALCHEMY_DATABASE_URI=` _URL BAZY DANYCH_*
`export SQLALCHEMY_TRACK_MODIFICATIONS=True;`

*url bazy danych musi wyglądać w taki sposób
`[engine]://[username]:[password]@[host]:[port]/[databasename]`
czyli np. postgresql://postgres:postgres@localhost:5432/test



Budowa projektu oparta na architekturze 'fabryki aplikacji', dlatego tak dziwnie wygląda.

Model MVC trochę kuleje, nie mam możliwości rozpisania każdej encji na osobne pliki, bo są problemy z circular dependency. W takim razie proponuję rozwiązanie podziału plików:

```
GMH
|-- .travis
|-- application
|   |-- controllers
|   |   |-- __init__.py                         <-- nie zrób mojego błędu, nie usuwaj tego pliku :V
|   |   |-- user_controller.py
|   |   |-- .
|   |   |-- .
|   |   `-- ...<reszta kontrolerów>
|   |-- __init__.py
|   |-- models.py                                <-- wszystkie modele i mapowania
|   `-- routes.py                                <--- możliwie najprostsze funkcje z kontrolerów 
|-- test
|   `-- <tutaj testy>
`-- 
```


Koncepcja taka, że nie wrzucamy venv na gita tylko w razie czego aktualizujemy requirements.txt

Testy jak na razie wystarczy odpalić komendą `pytest`, powinna być zainstalowana w venv.

Dokumentacja libek:

[flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
[marhsmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/#)
[flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/)
[marshmallow](https://marshmallow.readthedocs.io/en/stable/#)

Polecam serdecznie też serię [tych](https://hackersandslackers.com/flask-sqlalchemy-database-models/) artykułów.