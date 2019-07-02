#!/usr/bin/env python

import asyncio
import websocket
import time
import threading
import click
import QUANTAXIS as QA
from QA_OTGBroker import on_pong, on_error, on_close, querybank, login, peek, transfer, query_settlement, subscribe_quote


def on_message(ws, message):
    QA.QA_util_log_info(message)
    ws.send(peek())


@click.command()
@click.option('--acc', )
@click.option('--password', )
@click.option('--wsuri',)
@click.option('--broker',)
@click.option('--bankid')
@click.option('--bankpassword')
@click.option('--bankid')
@click.option('--capitalpassword')
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
            # ws.send(querybank(account_cookie=acc, password=capitalpassword,
            #                   bankid=bankid, bankpassword=bankpassword))
        threading.Thread(target=run, daemon=False).start()

    ws.on_open = _onopen

    threading.Thread(target=ws.run_forever, name='sub_websock {}'.format(
        acc), daemon=False).start()

    time.sleep(1)
    # x1 = query_settlement('20190617')
    # x2 = query_settlement('20190618')
    ws.send(subscribe_quote('SHFE.rb1910,DCE.j1909'))

    #x3 = query_settlement(20190619)
    #ws.send(query_settlement('20190619'))
    for i in range(10):
        ws.sock.ping('QUANTAXIS')
        time.sleep(1)
        ws.send(subscribe_quote('SHFE.rb1910,DCE.j1909'))


    ws.close()
