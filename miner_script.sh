
# Miners Script
echo "Init Miner Nodes"
export FLASK_APP=node_server.py
for x in {8000..8001}
do
    flask run --port $x &
done
echo "Miner Nodes Initiated"
