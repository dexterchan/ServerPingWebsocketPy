# ServerPingWebsocketPy


Create your own virtual env
````
python3 -m venv  virtualenv
````

build dependency
````
pip3 install -r requirements.txt
````

##Build package
````
python3 setup.py sdist
````

##Python server
Run
````
export PYTHONPATH=.
python3 PyFlaskSocketIOServer/RunServer.py -p 3000
````

##Python client
Run 
````
python3 Client/ConnectMkt.py -l localhost:3000
````

Test Package
````
pytest tests
````