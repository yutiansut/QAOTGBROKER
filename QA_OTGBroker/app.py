#!/usr/bin/env python

import asyncio
import websocket
import time
import threading
import click
import QUANTAXIS as QA
from QA_OTGBroker import on_pong, on_error, on_close, querybank, login, peek

def on_message(ws, message):
    QA.QA_util_log_info(message)
    ws.send(peek())


@click.command()
@click.option('--acc', default='133496')
@click.option('--password', default='QCHL1234')
@click.option('--wsuri', default='ws://www.yutiansut.com:7988')
@click.option('--broker', default='simnow')
@click.option('--bankid', default='')
@click.option('--bankpassword', default='')
@click.option('--bankid', default='')
@click.option('--capitalpassword', default='')
def app(acc, password, wsuri, broker, bankid, bankpassword, capitalpassword):
    ws = websocket.WebSocketApp(wsuri,
                                on_pong=on_pong,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    def _onopen(ws):
        def run():
            ws.send(login(
                name=acc, password=password, broker=broker))
            ws.send(peek())
            ws.send(querybank(account_cookie=acc, password=capitalpassword,
                        bankid=bankid, bankpassword=bankpassword))
        threading.Thread(target=run, daemon=False).start()
    
    ws.on_open = _onopen

    threading.Thread(target=ws.run_forever, name='sub_websock {}'.format(
            acc), daemon=False).start()


    
    time.sleep(1)
    try: 
        print('send query bank again')
        ws.send(querybank(account_cookie=acc, password=capitalpassword,
                    bankid=bankid, bankpassword=bankpassword))

    except:
        pass

    for i in range(100):
        ws.sock.ping('QUANTAXIS')
        time.sleep(1)
    ws.close()