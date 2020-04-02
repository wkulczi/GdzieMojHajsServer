ssh -o StrictHostKeyChecking=no -i ./deploy_key root@46.41.149.135 -q << EOF
pkill gunicorn;
cd wkulczi/GdzieMojHajsServer/;
git pull -q;

export FLASK_APP=app.py
export FLASK_DEBUG=0
export SQLALCHEMY_DATABASE_URI='$DATABASE_URI'
export SQLALCHEMY_TRACK_MODIFICATIONS=False
source venv/bin/activate; nohup gunicorn3 app:app &
exit 0
EOF
^C
