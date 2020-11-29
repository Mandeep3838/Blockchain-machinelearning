curl -X POST http://127.0.0.1:8000/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8001/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8002/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8003/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8004/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8005/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8006/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8007/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8001/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8002/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8003/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8004/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8005/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8006/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

start=0
end=25
z=0
peers=(http://127.0.0.1:8000 http://127.0.0.1:8001 http://127.0.0.1:8002 http://127.0.0.1:8003 http://127.0.0.1:8004 http://127.0.0.1:8005 http://127.0.0.1:8006 http://127.0.0.1:8007)


for x in {5000..5043}
do
    export PEER=${peers[$RANDOM % ${#peers[@]}]}
    export START_IND=$start
    export END_IND=$end
    if [ $z -le 5015 ]
    then
        export NOISE=1
    else
        export NOISE=0
    fi
    export FLASK_APP=run_app.py
    flask run --port $x &
    let "start+=25"
    let "end+=25"
    sleep 5
done

# start the clients
for x in {5000..5043}
do
    firefox http://127.0.0.1:$x &
done
i=0
# test
for x in {9000..9007}
do
    export PEER=${peers[$i]}
    export ERROR_FILE=$i
    export FLASK_APP=test_error.py
    flask run --port $x &
    sleep 5
    curl -X GET http://127.0.0.1:$x/test &
    let "i=i+1"
done


for x in {8000..8007}
do
    firefox http://127.0.0.1:$x/chain &
done

# train the clients
for x in {5000..5043}
do
    curl -X GET http://127.0.0.1:$x/submit &
done

# mine
for x in {8000..8007}
do
    curl -X GET http://127.0.0.1:$x/mine &
done

# export PEER="http://127.0.0.1:8001"
# export START_IND=100
# export END_IND=200
# export NOISE=1
# export FLASK_APP=run_app.py
# flask run --port 5001 &
# sleep 5

# export PEER="http://127.0.0.1:8000"
# export START_IND=200
# export END_IND=300
# export NOISE=0
# export FLASK_APP=run_app.py
# flask run --port 5002 &
# sleep 5

# export PEER="http://127.0.0.1:8001"
# export START_IND=300
# export END_IND=400
# export NOISE=1
# export FLASK_APP=run_app.py
# flask run --port 5003 &
# sleep 5

# export PEER="http://127.0.0.1:8000"
# export START_IND=400
# export END_IND=500
# export NOISE=1
# export FLASK_APP=run_app.py
# flask run --port 5004 &
# sleep 5

# export PEER="http://127.0.0.1:8001"
# export START_IND=500
# export END_IND=600
# export FLASK_APP=run_app.py
# export NOISE=1
# flask run --port 5005 &
# sleep 5

# export PEER="http://127.0.0.1:8000"
# export START_IND=600
# export END_IND=700
# export NOISE=1
# export FLASK_APP=run_app.py
# flask run --port 5006 &
# sleep 5

# export PEER="http://127.0.0.1:8001"
# export START_IND=700
# export END_IND=800
# export NOISE=1
# export FLASK_APP=run_app.py
# flask run --port 5007 &
# sleep 5

# export PEER="http://127.0.0.1:8000"
# export START_IND=800
# export END_IND=900
# export NOISE=1
# export FLASK_APP=run_app.py
# flask run --port 5008 &
# sleep 5

# export PEER="http://127.0.0.1:8001"
# export START_IND=900
# export END_IND=1000
# export NOISE=0
# export FLASK_APP=run_app.py
# flask run --port 5009 &
# sleep 5

# export PEER="http://127.0.0.1:8000"
# export START_IND=1000
# export END_IND=1100
# export NOISE=1
# export FLASK_APP=run_app.py
# flask run --port 5010 &
# sleep 5

