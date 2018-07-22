import bitcoin
import hashlib
import bitcoin.rpc

from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL, OP_RETURN, OP_ELSE, OP_ENDIF, OP_IF, OP_CHECKLOCKTIMEVERIFY, OP_DROP, OP_DUP
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH

bitcoin.SelectParams('regtest')  # regression test net


def demo():
    """Start: A: d  | B: y BCH

        End:  A: y BCH | B: d
    """

    d = "This is a test string"
    y = 0.001

    proxy = bitcoin.rpc.Proxy(
        service_url='http://test:test@47.105.119.12:18332')

    block = proxy.getblock(proxy.getblockhash(1))
    print(block)  # test rpc
    balance = proxy.getbalance()
    print(balance)
    # print(proxy.listunspent())

    # step 1
    h_a = hashlib.sha256(b'a').digest()
    sk_a = CBitcoinSecret.from_secret_bytes(h_a)
    g_sk_a = sk_a.pub
    h_b = hashlib.sha256(b'b').digest()
    sk_b = CBitcoinSecret.from_secret_bytes(h_b)
    g_sk_b = sk_b.pub

    print('A\'s Pub: {}'.format(g_sk_a))
    print('B\'s Pub: {}'.format(g_sk_b))

    #addr_a = proxy.getnewaddress('testa')
    #addr_b = proxy.getnewaddress('testb')
    addr_a = P2PKHBitcoinAddress.from_pubkey(sk_a.pub)
    addr_b = P2PKHBitcoinAddress.from_pubkey(sk_b.pub)

    print(type(sk_a.pub))
    print(type(sk_a))

    print('A\'s Address: {}'.format(addr_a))
    print('B\'s Address: {}'.format(addr_b))

    # step 2
    sk_c = sk_a + sk_b
    sk_c = CBitcoinSecret.from_secret_bytes(sk_c)
    g_sk_c = g_sk_a + g_sk_b
    addr_c = P2PKHBitcoinAddress.from_pubkey(sk_c.pub)

    print('C\'s Private: {}'.format(sk_c))
    print('C\'s Pub: {}'.format(g_sk_c))

    # step 3

    # convert little-endian hex to bytes
    # tx from last block (202)
    txid = lx('39550b284f858318ffb358dcf73587fb2b7184abbd4d0b6056e87c7aee2c3811')
    vout = 0

    # Create the txin structure, which includes the outpoint. The scriptSig
    # defaults to being empty.
    txin = CMutableTxIn(COutPoint(txid, vout))

    # We also need the scriptPubKey of the output we're spending because
    # SignatureHash() replaces the transaction scriptSig's with it.
    #
    # Here we'll create that scriptPubKey from scratch using the pubkey that
    # corresponds to the secret key we generated above.
    txin_scriptPubKey = CScript(
        [OP_RETURN, addr_c, str(y).encode(), d.encode(), True])

    # Create the txout. This time we create the scriptPubKey from shared peer c's address
    txout = CMutableTxOut(y * COIN, addr_c.to_scriptPubKey())

    # Create the unsigned transaction.
    tx = CMutableTransaction([txin], [txout])

    # Calculate the signature hash for that transaction.
    sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)

    # Now sign it. We have to append the type of signature we want to the end, in
    # this case the usual SIGHASH_ALL.
    sig = sk_a.sign(sighash) + bytes([SIGHASH_ALL])

    # Set the scriptSig of our transaction input appropriately.
    txin.scriptSig = CScript([sig, sk_a.pub])

    # Done! Print the transaction to standard output with the bytes-to-hex
    # function.
    print('='*10+'TRANSACTION OUTPUT'+'='*10)
    print(b2x(tx.serialize()))

    #step 4
    # b sends CLTV

    # if it reaches nLockTime the cancel, if not then A can take d away
    txid = lx('39550b284f858318ffb358dcf73587fb2b7184abbd4d0b6056e87c7aee2c3811')
    vout = 0
    txin = CMutableTxIn(COutPoint(txid, vout))
    txin_scriptPubKey = CScript([OP_IF, proxy.getblockcount(), OP_CHECKLOCKTIMEVERIFY, OP_DROP, g_sk_b, OP_CHECKSIG] +[OP_ELSE, OP_HASH160, Hash160(sk_a.pub), OP_EQUALVERIFY, g_sk_a, OP_CHECKSIG, OP_ENDIF])
    txout = CMutableTxOut(y * COIN, addr_c.to_scriptPubKey())
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)
    sig = sk_a.sign(sighash) + bytes([SIGHASH_ALL])
    txin.scriptSig = CScript([sig, sk_a.pub])
    print('='*10+'TRANSACTION OUTPUT'+'='*10)
    print(b2x(tx.serialize()))


    # step 5
    # a gets y BCH by sk_a
    txid = lx('39550b284f858318ffb358dcf73587fb2b7184abbd4d0b6056e87c7aee2c3811')
    vout = 0
    txin = CMutableTxIn(COutPoint(txid, vout))
    txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(sk_a.pub), OP_EQUALVERIFY, OP_CHECKSIG])
    txout = CMutableTxOut(y * COIN, addr_a.to_scriptPubKey())
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)
    sig = sk_c.sign(sighash) + bytes([SIGHASH_ALL])
    txin.scriptSig = CScript([sig, sk_c.pub])
    VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))
    print('='*10+'TRANSACTION OUTPUT'+'='*10)
    print(b2x(tx.serialize()))


    # step 6
    #b gets the the ownership of sk_a, sk_b
    txid = lx('39550b284f858318ffb358dcf73587fb2b7184abbd4d0b6056e87c7aee2c3811')
    vout = 0
    txin = CMutableTxIn(COutPoint(txid, vout))
    txin_scriptPubKey = CScript(
        [OP_RETURN, addr_b, str(y).encode(), d.encode(), True])
    txout = CMutableTxOut(y * COIN, addr_b.to_scriptPubKey())
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)
    sig = sk_c.sign(sighash) + bytes([SIGHASH_ALL])
    txin.scriptSig = CScript([sig, sk_c.pub])
    print('='*10+'TRANSACTION OUTPUT'+'='*10)
    print(b2x(tx.serialize()))



    # step 7
    # convert little-endian hex to bytes
    # tx from last block (202)
    #txid = proxy.getblockhash(proxy.getblockcount())
    #txid = lx(txid.decode())
    txid = lx('39550b284f858318ffb358dcf73587fb2b7184abbd4d0b6056e87c7aee2c3811')
    vout = 0
    txin = CMutableTxIn(COutPoint(txid, vout))
    txin_scriptPubKey = CScript(
        [OP_RETURN, addr_b, str(y).encode(), d.encode(), True])
    txout = CMutableTxOut(y * COIN, addr_b.to_scriptPubKey())
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)
    sig = sk_c.sign(sighash) + bytes([SIGHASH_ALL])
    txin.scriptSig = CScript([sig, sk_c.pub])
    print('='*10+'TRANSACTION OUTPUT'+'='*10)
    print(b2x(tx.serialize()))


demo()
