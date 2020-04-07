ssh -o StrictHostKeyChecking=no -i ./deploy_key $USR@$HOST -q << EOF
pkill gunicorn;
cd wkulczi/GdzieMojHajsServer/;
git pull -q;
python3 -m pip install -r requirements.txt;
export FLASK_APP=app.py
export FLASK_DEBUG=1
export SQLALCHEMY_DATABASE_URI=postgresql://$USR:$SQLPWD@localhost:5432/$DB;
export SQLALCHEMY_TRACK_MODIFICATIONS=True
gunicorn app:app &
exit 0;
EOF
^C