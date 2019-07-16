#
from QAPUBSUB.producer import publisher_routing
from QUANTAXIS.QAEngine import QA_Thread
from QA_OTGBroker import on_pong, on_message, on_error, subscribe_quote, on_close, login, peek
import websocket
import threading
import click
import time


class MARKET_SUBSCRIBER(QA_Thread):
    def __init__(self):
        super().__init__()
        self.ws = websocket.WebSocketApp('ws://openmd.shinnytech.com/t/md/front/mobile',
                                         on_pong=on_pong,
                                         on_message=self.on_message,
                                         on_error=on_error,
                                         on_close=on_close)

        def _onopen(ws):
            def run():
                ws.send(subscribe_quote('SHFE.rb1910,DCE.j909'))
                ws.send(peek())
            threading.Thread(target=run, daemon=False).start()


        self.ws.on_open = _onopen

        threading.Thread(target=self.ws.run_forever,
                         name='market_websock', daemon=False).start()

    def on_message(self, message):
        print(message)
        #self.ws.send(subscribe_quote('SHFE.rb1910,DCE.j1909'))
        self.ws.send(peek())

    def run(self):
        while True:

            time.sleep(1)


MARKET_SUBSCRIBER().run()
