read -r FIRSTLINE < db_uri.txt
echo \'$FIRSTLINE\'
source venv/bin/activate;
export FLASK_APP=app.py
export FLASK_DEBUG=1
export SQLALCHEMY_DATABASE_URI='postgresql://wojti:wojti@localhost:5432/test'
export SQLALCHEMY_TRACK_MODIFICATIONS=False
flask run
