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
python3 PyPingServer/RunServer.py
````

##Python client
Run 
````
python3 Client/ConnectMkt.py
````

Test Package
````
pytest tests
````