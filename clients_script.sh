curl -X POST http://127.0.0.1:8000/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8001/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'


export PEER="http://127.0.0.1:8000"
export START_IND=0
export END_IND=100
export FLASK_APP=run_app.py
flask run --port 5000 &
sleep 5

export PEER="http://127.0.0.1:8001"
export START_IND=100
export END_IND=200
export FLASK_APP=run_app.py
flask run --port 5001 &
sleep 5

export PEER="http://127.0.0.1:8000"
export START_IND=200
export END_IND=300
export FLASK_APP=run_app.py
flask run --port 5002 &
sleep 5

export PEER="http://127.0.0.1:8001"
export START_IND=300
export END_IND=400
export FLASK_APP=run_app.py
flask run --port 5003 &
sleep 5

export PEER="http://127.0.0.1:8000"
export START_IND=400
export END_IND=500
export FLASK_APP=run_app.py
flask run --port 5004 &
sleep 5

export PEER="http://127.0.0.1:8001"
export START_IND=500
export END_IND=600
export FLASK_APP=run_app.py
flask run --port 5005 &
sleep 5

export PEER="http://127.0.0.1:8000"
export START_IND=600
export END_IND=700
export FLASK_APP=run_app.py
flask run --port 5006 &
sleep 5

export PEER="http://127.0.0.1:8001"
export START_IND=700
export END_IND=800
export FLASK_APP=run_app.py
flask run --port 5007 &
sleep 5

export PEER="http://127.0.0.1:8000"
export START_IND=800
export END_IND=900
export FLASK_APP=run_app.py
flask run --port 5008 &
sleep 5

export PEER="http://127.0.0.1:8001"
export START_IND=900
export END_IND=1000
export FLASK_APP=run_app.py
flask run --port 5009 &
sleep 5

export PEER="http://127.0.0.1:8000"
export START_IND=1000
export END_IND=1100
export FLASK_APP=run_app.py
flask run --port 5010 &
sleep 5

export PEER="http://127.0.0.1:8001"
export START_IND=1100
export END_IND=1200
export FLASK_APP=run_app.py
flask run --port 5011 &
sleep 5

export PEER="http://127.0.0.1:8000"
export START_IND=1200
export END_IND=1300
export FLASK_APP=run_app.py
flask run --port 5012 &
echo "Done Model Init"