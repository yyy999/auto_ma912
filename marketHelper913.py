#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 21:57:24 2019
@author: Haiyi
@email: 806935610@qq.com
@wechart: yyy99966
@github: https://github.com/yyy999

"""
import exchangeConnection.huobi.huobiService
import exchangeConnection.huobi.huobiService913
import utils.helper as uh


# 包装一个不同市场的统一接口 方便同一调用
class Market:
    def __init__(self, market_name="huobi"):
        self.market_name = market_name

    def market_detail(self, base_cur,quotes_cur):
        """
        获取市场盘口信息
        :param base_cur:
        :param quote_cur:
        :return:
        """
        symbol=base_cur+quotes_cur
#        print(symbol)
        if self.market_name == "huobi":
            return exchangeConnection.huobi.huobiService913.get_depth(symbol,"step0").get("tick")
        else:
            return None

    def account_available(self, cur_name, cur_market_name=None):
        """
        获取某个currency的可用量
        :param cur_name:
        :param cur_market_name:
        :return:
        """
        if self.market_name == "huobi":
#            base_cur, quote_cur = cur_market_name.split("_")
            bitex_acc = exchangeConnection.huobi.huobiService913.get_balance()
            now_list=uh.find_currency(bitex_acc.get("data").get("list"),cur_name)
            return float(now_list[0].get("balance"))
        else:
            return None

    def buy(self, cur_market_name, price, amount):
        # print("buy", cur_market_name, price, amount)
        if self.market_name == "huobi":
#            base_cur, quote_cur = cur_market_name.split("_")
            return exchangeConnection.huobi.huobiService.buy(cur_market_name, price, amount)
        else:
            return None

    def sell(self, cur_market_name, price, amount):
        # print("sell", cur_market_name, price, amount)
        if self.market_name == "huobi":
            return exchangeConnection.huobi.huobiService.sell(cur_market_name, price, amount)

        else:
            return None

    def buy_market(self, cur_market_name, amount):
        """
        市价买
        :param cur_market_name: 货币对的名称
        :param amount: 买的总价
        :return:
        """
        # print("buy_market:", cur_market_name, amount)
        if self.market_name == "huobi":
            return exchangeConnection.huobi.huobiService.buyMarket(cur_market_name, amount)
        else:
            return None

    def sell_market(self, cur_market_name, amount):
        """
        市价卖
        :param cur_market_name: 货币对的名称
        :param amount: 卖的数量
        :return:
        """
        # print("sell_market:", cur_market_name, amount)
        if self.market_name == "huobi":
            return exchangeConnection.huobi.huobiService.SellMarket(cur_market_name, amount)
        else:
            return None

    def order_normal(self, order_result, cur_market_name):
        """
        是否成功下单
        :param order_result: 下单返回结果
        :param cur_market_name: 货币对名称
        :return:
        """
        if self.market_name == "huobi":
#            base_cur, quote_cur = cur_market_name.split("_")
            if order_result.get("status") == "ok":
                return True
            else:
                return False



    def get_order_processed_amount(self, order_result, cur_market_name=None):
        # print("get_order_processed_amount:", order_result, cur_market_name)
        if self.market_name == "huobi":
            result = exchangeConnection.huobi.huobiService913.order_info(order_result.get("data"))
#            print(result)
            return result.get('data').get("field-amount")
        else:
            return None

    def cancel_order(self, order_result, cur_market_name=None):
        if self.market_name == "huobi":
#            base_cur, quote_cur = cur_market_name.split("_")
#            if quote_cur == "usdt":
#                if base_cur == "eth":
#                    return exchangeConnection.bitex.bitexService.BitexServiceAPIKey(key_index="USDT_1")\
#                        .cancel_order(str(order_result.get("data")))  # {'status': 'ok', 'data': '2705970'}
#                elif base_cur == "etc":
#                    return exchangeConnection.bitex.bitexService.BitexServiceAPIKey(key_index="USDT_1")\
#                        .cancel_order(str(order_result.get("data")))  # {'status': 'ok', 'data': '2705970'}
#                elif base_cur == "btc":
            return exchangeConnection.huobi.huobiService913.cancel_order(order_result.get("data"))# {'status': 'ok', 'data': '2705970'}
#                elif base_cur == "ltc":
#                    return exchangeConnection.huobi.huobiService.cancelOrder(
#                        2, order_result.get("id"), "usdt", "cancel_order")
#            elif quote_cur == "btc":
#                if base_cur == "ltc" or base_cur == "eth" or base_cur =="etc":
#                    return exchangeConnection.pro.proService.ProServiceAPIKey(key_index="USDT_1").cancel_order(
#                           order_result.get("data"))
        else:
            return None

    def get_order_status(self, order_result, cur_market_name):
        # print("get_order_status:", order_result, cur_market_name)
        if self.market_name == "huobi":
#            base_cur, quote_cur = cur_market_name.split("_")
            result = exchangeConnection.huobi.huobiService913.order_info(order_result.get("data"))
            return result('data').get("status")
        else:
            return None


# test
if __name__ == "__main__":
     huobi = Market()
     print(huobi.market_detail("eth","btc"))
#     print(huobi.market_detail("eosusdt"))
##     print(huobi.market_detail("ltc", "usdt"))
##     print(huobi.market_detail("eth", "usdt"))
#     print(huobi.market_detail("eos", "eth"))
#     print("以太币可用", huobi.account_available("eth", "eth_usdt"))
     print("MTN可用", huobi.account_available("mtn"))
#     print(exchangeConnection.huobi.huobiService.getAccountInfo("usdt",'get'))
#     print(exchangeConnection.huobi.huobiService.getOrderInfo('mtxeth','usdt','get'))
#     result = exchangeConnection.huobi.huobiService.buy("mtneth",0.0000320, 100, None, None, "usdt", "buy")
#
     result={'status': 'ok', 'data': '48217662306'}
     print(result)
     result=huobi.get_order_processed_amount(result)
# {'result': 'success', 'id': 4491600137}
#     result = exchangeConnection.huobi.huobiService.cancelOrder(1,47588337890, "usdt", "cancel_order")
#     result = exchangeConnection.huobi.HbTradeDemo.cancel_order(47588337890)

     print(result)
#     print(exchangeConnection.huobi.huobiService.getOrderInfo(1, result.get("id"), "usdt", "order_info"))
# {'id': 4491348833, 'type': 1, 'order_price': '20000.00', 'order_amount': '0.0020', 'processed_price': '19997.98', 'processed_amount': '0.0020', 'vot': '39.99', 'fee': '0.0000', 'total': '39.99', 'status': 2}

# result = exchangeConnection.huobi.huobiService.buyMarket(1, 2000, None, None, "usdt", "buy_market")
# print(result)
#     result= exchangeConnection.huobi.HbTradeDemo.get_kline("btcusdt","1day")
#     print(result)


