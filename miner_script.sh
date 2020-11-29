''' Miners Script '''
export FLASK_APP=node_server.py
for x in {8000..8007}
do
    flask run --port $x &
done
