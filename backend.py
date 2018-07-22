from flask import Flask
from bitcoinrpc.authproxy import AuthServiceProxy

app = Flask(__name__)

rpc_conn = AuthServiceProxy("http://test:test@47.105.119.12:18332")

@app.route("/wallet/create")
def create_wallet(account=None):
    return rpc_conn.getnewaddress(account) #return new addrress

@app.route("/wallet/import/<account>", methods=['GET'])
def import_wallet(account):
    return rpc_conn.getaccountaddress(account) #return new addrress

@app.route("/tx/<txid>", methods=['GET'])
def get_tx(txid):
    return rpc_conn.gettransaction(txid) #return new addrress

if __name__ == "__main__":
    app.run()

