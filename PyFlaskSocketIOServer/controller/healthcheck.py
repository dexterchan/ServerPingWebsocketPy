from PyFlaskSocketIOServer.app import  app



@app.route("/", methods = ['GET'])
def httphealthCheck():
    return {"status":"OK"}


