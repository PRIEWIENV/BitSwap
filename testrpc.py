from bitcoinrpc.authproxy import AuthServiceProxy
from datetime import datetime

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://test:test@47.105.119.12:18332")
best_block_hash = rpc_connection.getblockhash(202)
print(rpc_connection.getblock(best_block_hash))

print(rpc_connection.getblockcount())
print(rpc_connection.listreceivedbyaddress())
print(rpc_connection.listaddressgroupings())
print(rpc_connection.listaccounts())
print(rpc_connection.getnewaddress())

print('='*20)
# batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
commands = [["getblockhash", height] for height in range(100)]
block_hashes = rpc_connection.batch_(commands)
blocks = rpc_connection.batch_([["getblock", h] for h in block_hashes])
block_times = [datetime.utcfromtimestamp(block["time"]).strftime(
    "%Y-%m-%d %H:%M:%S") for block in blocks]
print(block_times)
print('='*20)
#rpc_connection.sendrawtransaction('test')


print('='*20)
import hashlib
import bitcoin
import bitcoin.rpc
#from bitcoin.core.serialize import Serializable
from bitcoin.core import *
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress

bitcoin.SelectParams('regtest')
proxy_conn = bitcoin.rpc.Proxy(service_url='http://test:test@47.105.119.12:18332')
block = proxy_conn.getblock(proxy_conn.getblockhash(2))
print(block)
print(proxy_conn.getblockcount())

txid = lx('39550b284f858318ffb358dcf73587fb2b7184abbd4d0b6056e87c7aee2c3811')
#proxy_conn.sendrawtransaction(CTransaction([CMutableTxIn()],[CMutableTxOut()]))
h = hashlib.sha256(b'correct horse battery staple').digest()
seckey = CBitcoinSecret.from_secret_bytes(h)
vout = 1

# Create the txin structure, which includes the outpoint. The scriptSig
# defaults to being empty.
txin = CMutableTxIn(COutPoint(txid, vout))

# We also need the scriptPubKey of the output we're spending because
# SignatureHash() replaces the transaction scriptSig's with it.
#
# Here we'll create that scriptPubKey from scratch using the pubkey that
# corresponds to the secret key we generated above.
txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(seckey.pub), OP_EQUALVERIFY, OP_CHECKSIG])

# Create the txout. This time we create the scriptPubKey from a Bitcoin
# address.
#txout = CMutableTxOut(0.001*COIN, CBitcoinAddress('1BpEi6DfDAUFd7GtittLSdBeYJvcoaVggu').to_scriptPubKey())
addr = P2PKHBitcoinAddress.from_pubkey(seckey.pub)
txout = CMutableTxOut(0.001*COIN, addr)

# Create the unsigned transaction.
tx = CMutableTransaction([txin], [txout])

# Calculate the signature hash for that transaction.
sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)

# Now sign it. We have to append the type of signature we want to the end, in
# this case the usual SIGHASH_ALL.
sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])

# Set the scriptSig of our transaction input appropriately.
txin.scriptSig = CScript([sig, seckey.pub])

# Verify the signature worked. This calls EvalScript() and actually executes
# the opcodes in the scripts to see if everything worked out. If it doesn't an
# exception will be raised.
VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))

# Done! Print the transaction to standard output with the bytes-to-hex
# function.
print(b2x(tx.serialize()))


import subprocess

def command(*args, stdout=subprocess.PIPE):
    return subprocess.Popen(args, stdout=stdout, encoding="UTF8")

def cli(*args):
    cmd = ["bitcoin-cli", "-regtest", "-rpcport=18332", "-rpcuser=test", "-rpcpassword=test"]
    cmd += list(args)
    process = command(*cmd)
    process.wait()
    return process.stdout.read().strip()

print('='*30)
print(addr)
print(rpc_connection.getreceivedbyaddress('mrdwvWkma2D6n9mGsbtkazedQQuoksnqJV'))
