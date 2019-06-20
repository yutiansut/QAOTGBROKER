#!/usr/bin/env python

import asyncio
import websocket
import time
import threading
import click
import QUANTAXIS as QA
from QA_OTGBroker import on_pong, on_error, on_close, querybank, login, peek, transfer, query_settlement


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
            # ws.send(querybank(account_cookie=acc, password=capitalpassword,
            #                   bankid=bankid, bankpassword=bankpassword))
        threading.Thread(target=run, daemon=False).start()

    ws.on_open = _onopen

    threading.Thread(target=ws.run_forever, name='sub_websock {}'.format(
        acc), daemon=False).start()

    time.sleep(1)


    for i in range(10):
        ws.sock.ping('QUANTAXIS')
        time.sleep(1)
        
    try:
        print('send query bank again')
        res = querybank(account_cookie=acc, password=capitalpassword,
                        bankid=bankid, bankpassword=bankpassword)
        print(res)

        ws.send(res)
        print('send')
    except:
        pass
#     {
#   "aid": "req_transfer",                                    //必填, 转账请求
#   "future_account": "0001",                                 //必填, 期货账户
#   "future_password": "0001",                                //必填, 期货账户密码
#   "bank_id": "0001",                                        //必填, 银行ID
#   "bank_password": "0001",                                  //必填, 银行账户密码
#   "currency": "CNY",                                        //必填, 币种代码
#   "amount": 135.4                                           //必填, 转账金额, >0 表示转入期货账户, <0 表示转出期货账户
# }
    try:
        print('prepare to transfer')
        # ws.send(transfer(account_cookie=acc, password=capitalpassword,
        #                  bankid=bankid, bankpassword=bankpassword, amount=-200))
        ws.send(peek())
    except Exception as e:
        print(e)
        pass

    time.sleep(1)
    for i in range(100):
        print('query_again')
        ws.sock.ping('QUANTAXIS')
        time.sleep(1)
        ws.send(res)
        ws.send(query_settlement('20190620'))
    ws.close()
