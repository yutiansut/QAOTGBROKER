import websocket
import json
import QUANTAXIS as QA
try:
    import thread
except ImportError:
    import _thread as thread
import time


def send_order(account_cookie, order_direction, volume):
    return json.dumps({
        "aid": "insert_order",                  # //必填, 下单请求
        # //必填, 需要与登录用户名一致, 或为登录用户的子账户(例如登录用户为user1, 则报单 user_id 应当为 user1 或 user1.some_unit)
        "user_id": account_cookie,
        "order_id": "SomeStrategy.Instancex1.0002",  # //必填, 委托单号, 需确保在一个账号中不重复, 限长512字节
        "exchange_id": "SHFE",  # //必填, 下单到哪个交易所
        "instrument_id": "jm1901",               # //必填, 下单合约代码
        "direction": "BUY",                      # //必填, 下单买卖方向
        # //必填, 下单开平方向, 仅当指令相关对象不支持开平机制(例如股票)时可不填写此字段
        "offset":  order_direction,
        "volume":  volume,                             # //必填, 下单手数
        "price_type": "LIMIT",  # //必填, 报单价格类型
        "limit_price": 3528,  # //当 price_type == LIMIT 时需要填写此字段, 报单价格
        "volume_condition": "ANY",
        "time_condition": "GFD",
    })


def peek():
    return json.dumps(
        {
            "aid": "peek_message"
        })


def login(name='131176', password='qchl1234', broker='simnow'):
    return json.dumps({
        "aid": "req_login",
        "bid": str(broker),
        "user_name": str(name),
        "password": str(password),
    })


def on_message(ws, message):
    QA.QA_util_log_info(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        acc1 = '131176'
        login_1 = login(acc1, 'qchl1234')
        QA.QA_util_log_info(login_1)
        ws.send(login_1)
        time.sleep(1)
        ws.send(peek())
        ws.send(send_order(acc1, 'BUY', 1))
        time.sleep(20)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


def on_open2(ws):
    def run(*args):
        acc2 = '106184'
        login_2 = login(acc2, '930426')
        QA.QA_util_log_info(login_2)
        ws.send(login_2)
        time.sleep(1)
        ws.send(peek())
        
        time.sleep(2)
        ws.send(send_order(acc2, 'BUY', 1))
        time.sleep(10)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


def on_open3(ws):
    def run(*args):
        acc3 = '071907'
        login_3 = login(acc3, 'wow111000')
        QA.QA_util_log_info(login_3)
        ws.send(login_3)
        time.sleep(1)
        ws.send(peek())
        time.sleep(2)
        ws.send(send_order(acc3, 'SELL', 1))

        time.sleep(10)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://www.yutiansut.com:7988",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    ws2 = websocket.WebSocketApp("ws://www.yutiansut.com:7988",
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close)
    ws2.on_open = on_open2

    ws3 = websocket.WebSocketApp("ws://www.yutiansut.com:7988",
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close)
    ws3.on_open = on_open3
    ws.run_forever()
    ws2.run_forever()
    ws3.run_forever()
