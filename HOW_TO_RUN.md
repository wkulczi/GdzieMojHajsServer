### Jak uruchomić serwer GdzieMójHajs

##### 1. Linux (albo WSL)

- zainstaluj postgresql [tutorial](https://tecadmin.net/install-postgresql-server-on-ubuntu/)
- utwórz bazę danych (`CREATE DATABASE nazwa;`)
- ustaw hasło do użytkownika psql (będąc w konsoli psql: `\password <hasło>`)
- w pierwszej linii pliku `db_uri.txt` umieść adres do swojej bazy danych (tutorial inside, MUSI być jako pierwsza linia)
- uruchom `dev_unix_script.sh`i powinno wszystko śmigać

##### 2. Windows
- no fucking idea (yet!)



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


Testy jak na razie wystarczy odpalić komendą `pytest`, powinna być zainstalowana w venv.

Dokumentacja libek:

[flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
[marhsmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/#)
[flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/)
[marshmallow](https://marshmallow.readthedocs.io/en/stable/#)

Polecam serdecznie też serię [tych](https://hackersandslackers.com/flask-sqlalchemy-database-models/) artykułów.