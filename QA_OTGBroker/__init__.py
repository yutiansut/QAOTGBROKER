import websocket
import json
import QUANTAXIS as QA
try:
    import thread
except ImportError:
    import _thread as thread
import time

"""3种


Account



"CNY": {
  //账号及币种
  "user_id": "423423",                      //用户ID
  "currency": "CNY",                        //币种

  //本交易日开盘前状态
  "pre_balance": 12345,                     //上一交易日结算时的账户权益

  //本交易日内出入金事件的影响
  "deposit": 42344,                         //本交易日内的入金金额
  "withdraw": 42344,                        //本交易日内的出金金额
  "static_balance": 124895,                 //静态权益 = pre_balance + deposit - withdraw

  //本交易日内已完成交易的影响
  "close_profit": 12345,                    //本交易日内的平仓盈亏
  "commission": 123,                        //本交易日内交纳的手续费
  "premium": 123,                           //本交易日内交纳的期权权利金

  //当前持仓盈亏
  "position_profit": 12345,                 //当前持仓盈亏
  "float_profit": 8910.2,                   //当前浮动盈亏

  //当前权益
  "balance": 9963216.55,                    //账户权益 = static_balance + close_profit - commission - premium + position_profit

  //保证金占用, 冻结及风险度
  "margin": 11232.23,                       //持仓占用保证金
  "frozen_margin": 12345,                   //挂单冻结保证金
  "frozen_commission": 123,                 //挂单冻结手续费
  "frozen_premium": 123,                    //挂单冻结权利金
  "available": 9480176.150000002,           //可用资金 = balance - margin - frozen_margin - frozen_commission - frozen_premium
  "risk_ratio": 0.048482375,                //风险度 = 1 - available / balance
}



Position

"SHFE.cu1801":{                             //position_key=symbol
  //交易所和合约代码
  "user_id": "423423",                      //用户ID
  "exchange_id": "SHFE",                    //交易所
  "instrument_id": "cu1801",                //合约在交易所内的代码

  //持仓手数与冻结手数
  "volume_long_today": 5,                   //多头今仓持仓手数
  "volume_long_his": 5,                     //多头老仓持仓手数
  "volume_long": 10,                        //多头持仓手数
  "volume_long_frozen_today": 1,            //多头今仓冻结手数
  "volume_long_frozen_his": 2,              //多头老仓冻结手数
  "volume_short_today": 5,                  //空头今仓持仓手数
  "volume_short_his": 5,                    //空头老仓持仓手数
  "volume_short": 10,                       //空头持仓手数
  "volume_short_frozen_today": 1,           //空头今仓冻结手数
  "volume_short_frozen_his": 2,             //空头老仓冻结手数

  //成本, 现价与盈亏
  "open_price_long": 3203.5,                //多头开仓均价
  "open_price_short": 3100.5,               //空头开仓均价
  "open_cost_long": 3203.5,                 //多头开仓成本
  "open_cost_short": 3100.5,                //空头开仓成本
  "position_price_long": 32324.4,           //多头持仓均价
  "position_price_short": 32324.4,          //空头持仓均价
  "position_cost_long": 32324.4,            //多头持仓成本
  "position_cost_short": 32324.4,           //空头持仓成本
  "last_price": 12345.6,                    //最新价
  "float_profit_long": 32324.4,             //多头浮动盈亏
  "float_profit_short": 32324.4,            //空头浮动盈亏
  "float_profit": 12345.6,                  //浮动盈亏 = float_profit_long + float_profit_short
  "position_profit_long": 32324.4,          //多头持仓盈亏
  "position_profit_short": 32324.4,         //空头持仓盈亏
  "position_profit": 12345.6,               //持仓盈亏 = position_profit_long + position_profit_short

  //保证金占用
  "margin_long": 32324.4,                   //多头持仓占用保证金
  "margin_short": 32324.4,                  //空头持仓占用保证金
  "margin": 32123.5,                        //持仓占用保证金 = margin_long + margin_short
}



Order


"123": {                                    //order_id, 用于唯一标识一个委托单. 对于一个USER, order_id 是永远不重复的

  //委托单初始属性(由下单者在下单前确定, 不再改变)
  "user_id": "423423",                      //用户ID
  "order_id": "123",                        //委托单ID, 对于一个USER, order_id 是永远不重复的
  "exchange_id": "SHFE",                    //交易所
  "instrument_id": "cu1801",                //在交易所中的合约代码
  "direction": "BUY",                       //下单方向
  "offset": "OPEN",                         //开平标志
  "volume_orign": 6,                        //总报单手数
  "price_type": "LIMIT",                    //指令类型, ACTIVE=对价下单, PASSIVE=挂价下单
  "limit_price": 45000,                     //委托价格, 仅当 price_type = LIMIT 时有效
  "time_condition":   "GTD",                  //时间条件
  "volume_condition": "ANY",                //数量条件

  //下单后获得的信息(由期货公司返回, 不会改变)
  "insert_date_time": 1517544321432,        //下单时间, epoch nano
  "exchange_order_id": "434214",            //交易所单号

  //委托单当前状态
  "status": "ALIVE",                        //委托单状态, ALIVE=有效, FINISHED=已完
  "volume_left": 3,                         //未成交手数
  "frozen_margin": 343234,                  //冻结保证金
  "last_msg": "",                           //提示信息

  //内部序号
  "seqno": 4324,
}


TRADE


"123": {                                    //trade_key, 用于唯一标识一条成交记录. 对于一个USER, trade_key 是永远不重复的

  "user_id": "423423",                      //用户ID
  "order_id": "434214",                     //交易所单号
  "trade_id": "123",                        //委托单ID, 对于一个USER, trade_id 是永远不重复的
  "exchange_id": "SHFE",                    //交易所
  "instrument_id": "cu1801",                //在交易所中的合约代码
  "exchange_trade_id": "434214",            //交易所单号
  "direction": "BUY",                       //下单方向
  "offset": "OPEN",                         //开平标志
  "volume": 6,                              //成交手数
  "price": 45000,                           //成交价格
  "trade_date_time":  15175442131,          //成交时间, epoch nano
  "commission": "434214",                   //成交手续费
  "seqno": 4324,
}


交易同步


{
  "aid": "rtn_data",                                      //数据推送
  "data": [                                               //diff数据数组, 一次推送中可能含有多个数据包
  {
    "trade": {                                            //交易相关数据
      "user1": {                                          //登录用户名
        "user_id": "user1",                               //登录用户名
        "accounts": {                                     //账户资金信息
          "CNY": {                                        //account_key, 通常为币种代码
            //核心字段
            "account_id": "423423",                       //账号
            "currency": "CNY",                            //币种
            "balance": 9963216.550000003,                 //账户权益
            "available": 9480176.150000002,               //可用资金
            //参考字段
            "pre_balance": 12345,                         //上一交易日结算时的账户权益
            "deposit": 42344,                             //本交易日内的入金金额
            "withdraw": 42344,                            //本交易日内的出金金额
            "commission": 123,                            //本交易日内交纳的手续费
            "preminum": 123,                              //本交易日内交纳的权利金
            "static_balance": 124895,                     //静态权益
            "position_profit": 12345,                     //持仓盈亏
            "float_profit": 8910.231,                     //浮动盈亏
            "risk_ratio": 0.048482375,                    //风险度
            "margin": 11232.23,                           //占用资金
            "frozen_margin": 12345,                       //冻结保证金
            "frozen_commission": 123,                     //冻结手续费
            "frozen_premium": 123,                        //冻结权利金
            "close_profit": 12345,                        //本交易日内平仓盈亏
            "position_profit": 12345,                     //当前持仓盈亏
          }
        },
        "positions": {                                    //持仓
          "SHFE.cu1801": {                                //合约代码
            //核心字段
            "exchange_id": "SHFE",                        //交易所
            "instrument_id": "cu1801",                    //合约代码
            //参考字段
            "hedge_flag": "SPEC",                         //套保标记
            "open_price_long": 3203.5,                    //多头开仓均价
            "open_price_short": 3100.5,                   //空头开仓均价
            "open_cost_long": 3203.5,                     //多头开仓成本
            "open_cost_short": 3100.5,                    //空头开仓成本
            "float_profit_long": 32324.4,                 //多头浮动盈亏
            "float_profit_short": 32324.4,                //空头浮动盈亏
            "position_cost_long": 32324.4,                //多头持仓成本
            "position_cost_short": 32324.4,               //空头持仓成本
            "position_profit_long": 32324.4,              //多头浮动盈亏
            "position_profit_long": 32324.4,              //空头浮动盈亏
            "volume_long_today": 5,                       //多头今仓持仓手数
            "volume_long_his": 5,                         //多头老仓持仓手数
            "volume_short_today": 5,                      //空头今仓持仓手数
            "volume_short_his": 5,                        //空头老仓持仓手数
            "margin_long": 32324.4,                       //多头持仓占用保证金
            "margin_short": 32324.4,                      //空头持仓占用保证金
            "order_volume_buy_open": 1,                   //买开仓挂单手数
            "order_volume_buy_close": 1,                  //买平仓挂单手数
            "order_volume_sell_open": 1,                  //卖开仓挂单手数
            "order_volume_sell_close": 1,                 //卖平仓挂单手数
          }
        },
        "orders": {                                       //委托单
          "123": {                                        //order_id, 用于唯一标识一个委托单. 对于一个USER, order_id 是永远不重复的
            //核心字段
            "order_id": "123",                            //委托单ID, 对于一个USER, order_id 是永远不重复的
            "order_type": "TRADE",                        //指令类型
            "exchange_id": "SHFE",                        //交易所
            "instrument_id": "cu1801",                    //在交易所中的合约代码
            "direction": "BUY",                           //下单方向, BUY=
            "offset": "OPEN",                             //开平标志
            "volume_orign": 6,                            //总报单手数
            "volume_left": 3,                             //未成交手数
            "trade_type": "TAKEPROFIT",                   //指令类型
            "price_type": "LIMIT",                        //指令类型
            "limit_price": 45000,                         //委托价格, 仅当 price_type = LIMIT 时有效
            "time_condition": "GTD",                      //时间条件
            "volume_condition": "ANY",                    //数量条件
            "min_volume": 0,
            "hedge_flag": "SPECULATION",                  //保值标志
            "status": "ALIVE",                            //委托单状态, ALIVE=有效, FINISHED=已完
            //参考字段
            "last_msg":       "",                               //最后操作信息
            "insert_date_time":       1928374000000000,         //下单时间
            "exchange_order_id": "434214",                //交易所单号
          }
        },
        "trades": {                                       //成交记录
          "123|1": {                                      //trade_key, 用于唯一标识一个成交项
            "order_id": "123",
            "exchange_id": "SHFE",                        //交易所
            "instrument_id": "cu1801",                    //交易所内的合约代码
            "exchange_trade_id": "1243",                  //交易所成交号
            "direction": "BUY",                           //成交方向
            "offset": "OPEN",                             //开平标志
            "volume": 6,                                  //成交手数
            "price": 1234.5,                              //成交价格
            "trade_date_time": 1928374000000000           //成交时间
          }
        },
      },
    },
    ]
  }
}

notify


{
  "aid": "rtn_data",                                        //数据推送
  "data": [                                                 //diff数据数组, 一次推送中可能含有多个数据包
    {
      "notify": {                                           //通知信息
        "2010": {
          "type": "MESSAGE",                                //消息类型
          "level": "INFO",                                  //消息等级
          "code": 1000,                                     //消息代码
          "content": "abcd",                                //消息正文
        }
      },
    }
  ]
}
"""


def send_order(account_cookie, order_direction='BUY', order_offset='OPEN', volume=1, order_id=False, code='rb1905', exchange_id='SHFE', price=3925):
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
        "limit_price": price,  # //当 price_type == LIMIT 时需要填写此字段, 报单价格
        "volume_condition": "ANY",
        "time_condition": "GFD",
    })


def cancel_order(account_cookie, order_id):
    return json.dumps({
        "aid": "cancel_order",  # //必填, 撤单请求
        "user_id": account_cookie,  # //必填, 下单时的 user_id
        "order_id": order_id               # //必填, 委托单的 order_id
    })


def querybank(account_cookie, password, bankid, bankpassword):
    return json.dumps({
        "aid": "qry_bankcapital",
        "bank_id": str(bankid),
        "future_account": str(account_cookie),
        "future_password": str(password),
        "bank_password": str(bankpassword),
        "currency": "CNY"
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


def subscribe_quote(ins_list="SHFE.cu1612,CFFEX.IF1701"):
    return json.loads(
        {
            "aid": "subscribe_quote",  # // 必填, 请求订阅实时报价数据
            "ins_list": ins_list  # // 必填, 需要订阅的合约列表，以逗号分隔
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


def ping(ws):
    return ws.ping()


def parse_rtn(message):
    pass


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


def on_message(ws, message):
    QA.QA_util_log_info(message)


def on_ping(ws, message):
    print('ping')
    QA.QA_util_log_info(message)
    ws.pong(message)


def on_pong(ws, message):
    print('pong')
    QA.QA_util_log_info(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        acc1 = '131176'
        acc1_password = 'qchl123456'
        broker = 'simnow'
        login_1 = login(broker, acc1, acc1_password)
        QA.QA_util_log_info(login_1)

        # 登陆
        ws.send(login_1)
        time.sleep(1)
        # peek
        ws.send(peek())

        # ws.send(querybank(acc1,))
        for i in range(100):
            ws.sock.ping('QUANTAXIS')
            time.sleep(1)
        time.sleep(20)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":

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
