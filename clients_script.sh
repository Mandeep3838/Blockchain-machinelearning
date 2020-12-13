
echo "Building Network"
curl -X POST http://127.0.0.1:8000/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

curl -X POST http://127.0.0.1:8001/register_with -H 'Content-Type: application/json' -d '{"node_address": "http://127.0.0.1:8000"}'

echo "Network betweem Miners Established"
start=0
end=100
z=5001
i=1
peers=(http://127.0.0.1:8000 http://127.0.0.1:8001)

echo "Init Client nodes"
for x in {5000..5010}
do
    export PEER=${peers[$i]}
    export START_IND=$start
    export END_IND=$end
    if [ $x -le $z ]
    then
        export NOISE=1
    else
        export NOISE=0
    fi
    export FLASK_APP=run_app.py
    flask run --port $x &
    let "start+=100"
    let "end+=100"
    sleep 5
    let "i=1-i"
done
echo "Client nodes started"

echo "Opening UI for client nodes"
# start the clients
for x in {5000..5010}
do
    firefox http://127.0.0.1:$x &
done
echo "Client nodes opened"

echo "Starting Test node"
# testing node

export PEER="http://127.0.0.1:8000"
export ERROR_FILE="9000"  
export FLASK_APP=test_error.py
flask run --port 9000 &
sleep 5
curl -X GET http://127.0.0.1:9000/test &

echo "Test node Running"

echo "Opening UI for miners"
for x in {8000..8001}
do
    firefox http://127.0.0.1:$x/chain &
done
echo "Miner Nodes opened"

echo "Start training on Client Nodes"
# train the clients
for x in {5000..5010}
do
    curl -X GET http://127.0.0.1:$x/submit &
done
echo "Training Started"

echo "Start Mining"
# mine
for x in {8000..8001}
do
    curl -X GET http://127.0.0.1:$x/mine &
done

echo "Mining Started"