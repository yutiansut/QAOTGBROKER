import websocket
import json
import QUANTAXIS as QA
try:
    import thread
except ImportError:
    import _thread as thread
import time


def send_order(account_cookie, order_direction='BUY', order_offset='OPEN', volume=1, order_id=False, code='rb1905', exchange_id='SHFE'):
    """[summary]

    Arguments:
        account_cookie {[type]} -- [description]

    Keyword Arguments:
        order_direction {str} -- [description] (default: {'BUY'})
        order_offset {str} -- [description] (default: {'OPEN'})
        volume {int} -- [description] (default: {1})
        order_id {bool} -- [description] (default: {False})
        code {str} -- [description] (default: {'rb1905'})
        exchange_id {str} -- [description] (default: {'SHFE'})

    Returns:
        [type] -- [description]
    """

    return json.dumps({
        "aid": "insert_order",                  # //必填, 下单请求
        # //必填, 需要与登录用户名一致, 或为登录用户的子账户(例如登录用户为user1, 则报单 user_id 应当为 user1 或 user1.some_unit)
        "user_id": account_cookie,
        # //必填, 委托单号, 需确保在一个账号中不重复, 限长512字节
        "order_id": order_id if order_id else QA.QA_util_random_with_topic('QAOTG'),
        "exchange_id": exchange_id,  # //必填, 下单到哪个交易所
        "instrument_id": code,               # //必填, 下单合约代码
        "direction": order_direction,                      # //必填, 下单买卖方向
        # //必填, 下单开平方向, 仅当指令相关对象不支持开平机制(例如股票)时可不填写此字段
        "offset":  order_offset,
        "volume":  volume,                             # //必填, 下单手数
        "price_type": "LIMIT",  # //必填, 报单价格类型
        "limit_price": 3528,  # //当 price_type == LIMIT 时需要填写此字段, 报单价格
        "volume_condition": "ANY",
        "time_condition": "GFD",
    })


def cancel_order(account_cookie, order_id):
    return json.dumps({
        "aid": "cancel_order",  # //必填, 撤单请求
        "user_id": account_cookie,  # //必填, 下单时的 user_id
        "order_id": order_id               # //必填, 委托单的 order_id
    })


def transfer(account_cookie, password, bankid, bankpassword, amount):
    return json.dumps({
        {
            "aid": "req_transfer",  # //必填, 转账请求
            "future_account": account_cookie,  # //必填, 期货账户
            "future_password": password,  # //必填, 期货账户密码
            "bank_id": bankid,  # //必填, 银行ID
            "bank_password": bankpassword,  # //必填, 银行账户密码
            "currency": "CNY",  # //必填, 币种代码
            "amount": float(amount)  # //必填, 转账金额, >0 表示转入期货账户, <0 表示转出期货账户
        }
    })


def peek():
    return json.dumps(
        {
            "aid": "peek_message"
        })


class ORDER_TYPE():

    """        
    Name	Value/Description
    TRADE	交易指令
    SWAP	互换交易指令
    EXECUTE	期权行权指令
    QUOTE	期权询价指令"""
    TRADE = 'TRADE'
    SWAP = 'SWAP'
    EXECUTE = 'EXECUTE'
    QUOTE = 'QUOTE'


def login(name='131176', password='qchl1234', broker='simnow24'):
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
        ws.send(send_order(acc1, 'BUY'))
        time.sleep(20)
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

    ws.run_forever()
