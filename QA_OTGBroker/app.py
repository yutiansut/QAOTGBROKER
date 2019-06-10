#!/usr/bin/env python

import asyncio
import websockets
import time
import threading
import click

@click.command()
@click.option('--acc', default='133496')
@click.option('--password', default='QCHL1234')
@click.option('--wsuri', default='ws://www.yutiansut.com:7988')
@click.option('--broker', default='simnow')
@click.option('--bankid', default='')
@click.option('--bankpassword', default='')
def app(acc, password, wsuri, broker, bankid, bankpassword):
    ws = websocket.WebSocketApp(wsuri,
                                on_pong=on_pong,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    def _onopen(ws):
        def run():
            ws.send(login(
                name=acc, password=password, broker=broker))
        threading.Thread(target=run, daemon=False).start()
    ws.on_open = _onopen

    ws.send(querybank(account_cookie=acc, password=password,
                        bankid=bankid, bankpassword=bankpassword))
    time.sleep(1)
    for i in range(100):
        ws.sock.ping('QUANTAXIS')
        time.sleep(1)
