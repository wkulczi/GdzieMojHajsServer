read -r FIRSTLINE < db_uri.txt
echo \'$FIRSTLINE\'
source venv/bin/activate;
export FLASK_APP=app.py
export FLASK_DEBUG=1
export SQLALCHEMY_DATABASE_URI=$FIRSTLINE
export SQLALCHEMY_TRACK_MODIFICATIONS=True
flask run
