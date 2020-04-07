ssh -o StrictHostKeyChecking=no -i ./deploy_key $USR@$HOST << EOF
pkill gunicorn;
cd wkulczi/GdzieMojHajsServer/;
git pull -q;
source venv/bin/activate; nohup gunicorn3 app:app &
exit 0;
EOF
