# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 20:13:32 2019

@author: Haiyi
@email: 806935610@qq.com
@wechart: yyy99966
@github: https://github.com/yyy999
"""

import ma_ind as maInd
import marketHelper913 as marketHelper
# 设定账户 accountConfig
import traceback
import time
import os
import logging
# import yaml
import multiprocessing
import math
from utils.helper import *

# 设置logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
#now_dir = os.getcwd()
main_log_handler = logging.FileHandler("log/triangle_main_{0}.log".format(int(time.time())), mode="w", encoding="utf-8")
main_log_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
main_log_handler.setFormatter(formatter)
logger.addHandler(main_log_handler)


class ClassMa:
    """
        交易对：用一种资产（quote currency）去定价另一种资产（base currency）,比如用比特币（BTC）去定价莱特币（LTC），
        就形成了一个LTC/BTC的交易对，
        交易对的价格代表的是买入1单位的base currency（比如LTC）
        需要支付多少单位的quote currency（比如BTC），
        或者卖出一个单位的base currency（比如LTC）
        可以获得多少单位的quote currency（比如BTC）。
        当LTC对BTC的价格上涨时，同等单位的LTC能够兑换的BTC是增加的，而同等单位的BTC能够兑换的LTC是减少的。
    """
#    def __init__(self,symbol="eoseth"):
#        self.base_cur, self.quote_cur = symbol.split("_")

    def __init__(self, base_cur="eos", quote_cur="eth", interval=1):
        """
        初始化
        :param base_cur:  基准资产
        :param quote_cur:  定价资产
        :param mid_cur:  中间资产
        :param interval:  策略触发间隔
        """

        # 设定EA监控交易对
        self.base_cur = base_cur
        self.quote_cur = quote_cur
#        self.mid_cur = mid_cur   # 中间货币，usdt或者btc

        self.base_quote_slippage = 0.002  # 设定市场价滑点百分比
#        self.base_mid_slippage = 0.002
#        self.quote_mid_slippage = 0.002

        self.base_quote_fee = 0.002  # 设定手续费比例
#        self.base_mid_fee = 0.002
#        self.quote_mid_fee = 0.002

        self.order_ratio_base_quote = 0.5  # 设定吃单比例
#        self.order_ratio_base_mid = 0.5

        # 设定监控时间
        self.interval = interval


        #XXX
        # 最小的交易单位设定
        self.min_trade_unit = 0.002   # LTC/BTC交易对，设置为0.2, ETH/BTC交易对，设置为0.02
        self.pos_rate = {'0.10':0.1 ,'0.25':0.25,'0.38':0.38,'0.50':0.5,'0.62':0.62,'0.75':0.75,'1.00':1}
        self.market_price_tick = dict()  # 记录触发套利的条件时的当前行情
        self.pos = False
        self.buyCmd = False
        self.sellCmd = False

    def strategy(self):   # 主策略
        # 检查是否有开仓条件
        try:
            # 初始化为火币市场
            huobi_market = marketHelper.Market()
            self.market_price_tick = dict()
            self.market_price_tick["{0}_{1}".format(self.base_cur, self.quote_cur)] = \
                huobi_market.market_detail(self.base_cur, self.quote_cur)
#            print(self.market_price_tick)
#            print(huobi_market.market_detail(self.base_cur, self.quote_cur))
            market_price_sell_1 = \
                self.market_price_tick["{0}_{1}".format(self.base_cur, self.quote_cur)].get("asks")[0][0]
            market_price_buy_1 = \
                self.market_price_tick["{0}_{1}".format(self.base_cur, self.quote_cur)].get("bids")[0][0]
#            self.market_price_tick["{0}_{1}".format(self.base_cur, self.mid_cur)] = \
#                huobi_market.market_detail(self.base_cur, self.mid_cur)
            print(market_price_sell_1)
            print(market_price_buy_1)
#            print(self.market_price_tick)
#            print(huobi_market.market_detail(self.base_cur, self.quote_cur))
            buylots=self.pos_rate.get('0.10')*self.get_currency_available(huobi_market,self.quote_cur)/market_price_sell_1
            buylots=downRound(buylots,2)
#            matradesys.buy_enter(huobi_market,buylots)
            selllots=self.pos_rate.get('1.00')*self.get_currency_available(huobi_market,self.base_cur)
            selllots = downRound(selllots, 8)
#            matradesys.sell_enter(huobi_market,selllots)
            print('buylots='+str(buylots))
            print('selllots='+str(selllots))

            '''
                MA交易系统的基本思路是，用两个市场（比如BTC/USDT，LTC/USDT）的价格（分别记为P1，P2），

           2019.09.10
           多单
           空单
            '''
#            maValue=list()
            symbol = self.get_market_name(self.base_cur,self.quote_cur)
            maValue0=maInd.get_ma(symbol,'1day',0,1)
            maValue1=maInd.get_ma(symbol,'1day',0,2)
            logger.info("maValue0：{0},mavalue1:{1}".format(maValue0,maValue1))
            print(maValue0)
            print(maValue1)
#            check_open()
#            '''buy check
            if self.sellCmd==False and self.buyCmd==False:
                if(maValue0[0]>maValue0[1] and maValue1[0]<maValue1[1]):
                    self.buyCmd=True
                elif(maValue0[0]<maValue0[1] and maValue1[0]>maValue1[1]):#ma5<ma10
                    self.sellCmd=True

                logger.info("买入条件：{0},卖出条件:{1}".format(self.buyCmd,self.sellCmd))
                print("买入条件：{0},卖出条件:{1}".format(self.buyCmd,self.sellCmd))
                print("bcmd="+str(self.buyCmd))
                print("scmd=",self.sellCmd)
#                return
                if self.buyCmd:
                    market_buy_size =buylots         # self.get_market_buy_size(huobi_market)
                    market_buy_size = downRound(market_buy_size, 2)
                    if market_buy_size >= self.min_trade_unit:
                        self.buy_enter(huobi_market, market_buy_size)
                    else:
                        logger.info("小于最小交易单位")

                # 检查逆循环套利

                elif self.sellCmd:
                    market_sell_size =selllots          # self.get_market_sell_size(huobi_market)
                    market_sell_size = downRound(market_sell_size, 2)
                    if market_sell_size >= self.min_trade_unit:
                        self.sell_enter(huobi_market, market_sell_size)
                    else:
                        logger.info("小于最小交易单位")
            else :
                logger.info('已经开仓')
        except:
            logger.error(traceback.format_exc())
            print(traceback.format_exc())

#    def sum_slippage_fee(self):
#        return self.base_quote_slippage + self.base_mid_slippage + self.quote_mid_slippage + \
#               self.base_quote_fee + self.base_mid_fee + self.quote_mid_fee

    @staticmethod
    def get_market_name(base, quote):
            return "{0}{1}".format(base, quote)

    # 计算最保险的下单数量
    '''
        1.	LTC/BTC卖方盘口吃单数量：ltc_btc_sell1_quantity*order_ratio_ltc_btc，其中ltc_btc_sell1_quantity 代表LTC/BTC卖一档的数量，
            order_ratio_ltc_btc代表本策略在LTC/BTC盘口的吃单比例
        2.	LTC/usdt买方盘口吃单数量：ltc_usdt_buy1_quantity*order_ratio_ltc_usdt，其中order_ratio_ltc_usdt代表本策略在LTC/usdt盘口的吃单比例
        3.	LTC/BTC账户中可以用来买LTC的BTC额度及可以置换的LTC个数：
            btc_available - btc_reserve，可以置换成
            (btc_available – btc_reserve)/ltc_btc_sell1_price个LTC
            其中，btc_available表示该账户中可用的BTC数量，btc_reserve表示该账户中应该最少预留的BTC数量
            （这个数值由用户根据自己的风险偏好来设置，越高代表用户风险偏好越低）。
        4.	BTC/usdt账户中可以用来买BTC的usdt额度及可以置换的BTC个数和对应的LTC个数：
            usdt_available - usdt_reserve, 可以置换成
            (usdt_available-usdt_reserve)/btc_usdt_sell1_price个BTC，
            相当于
            (usdt_available-usdt_reserve)/btc_usdt_sell1_price/ltc_btc_sell1_price
            个LTC
            其中：usdt_available表示该账户中可用的usdt数量，usdt_reserve表示该账户中应该最少预留的usdt数量
            （这个数值由用户根据自己的风险偏好来设置，越高代表用户风险偏好越低）。
        5.	LTC/usdt账户中可以用来卖的LTC额度：
            ltc_available – ltc_reserve
            其中，ltc_available表示该账户中可用的LTC数量，ltc_reserve表示该账户中应该最少预留的LTC数量
            （这个数值由用户根据自己的风险偏好来设置，越高代表用户风险偏好越低）。
    '''
    def get_market_buy_size(self, huobi_market):
        market_buy_size = self.market_price_tick["{0}_{1}".format(self.base_cur, self.quote_cur)].get("asks")[0][1] \
                          * self.order_ratio_base_quote
        base_mid_sell_size = self.market_price_tick["{0}_{1}".format(self.base_cur, self.mid_cur)].get("bids")[0][1] \
                             * self.order_ratio_base_mid
        base_quote_off_reserve_buy_size = \
            (huobi_market.account_available(self.quote_cur, self.get_market_name(self.base_cur, self.quote_cur))
             - self.base_quote_quote_reserve) / \
            self.market_price_tick["{0}_{1}".format(self.base_cur, self.quote_cur)].get("asks")[0][0]
        quote_mid_off_reserve_buy_size = \
            (huobi_market.account_available(self.mid_cur, self.get_market_name(self.quote_cur, self.mid_cur)) -
             self.quote_mid_mid_reserve) / \
            self.market_price_tick["{0}_{1}".format(self.quote_cur, self.mid_cur)].get("asks")[0][0] / \
            self.market_price_tick["{0}_{1}".format(self.base_cur, self.quote_cur)].get("asks")[0][0]
        base_mid_off_reserve_sell_size = \
            huobi_market.account_available(self.base_cur, self.get_market_name(self.base_cur, self.mid_cur)) - \
            self.base_mid_base_reserve
        logger.info("计算数量：{0}，{1}，{2}，{3}，{4}".format(market_buy_size, base_mid_sell_size,
                                                      base_quote_off_reserve_buy_size, quote_mid_off_reserve_buy_size,
                                                      base_mid_off_reserve_sell_size))
        return math.floor(min(market_buy_size, base_mid_sell_size, base_quote_off_reserve_buy_size,
                              quote_mid_off_reserve_buy_size, base_mid_off_reserve_sell_size)*10000)/10000

    '''
        卖出的下单保险数量计算
        假设BTC/usdt盘口流动性好
        1. LTC/BTC买方盘口吃单数量：ltc_btc_buy1_quantity*order_ratio_ltc_btc，其中ltc_btc_buy1_quantity 代表LTC/BTC买一档的数量，
           order_ratio_ltc_btc代表本策略在LTC/BTC盘口的吃单比例
        2. LTC/usdt卖方盘口卖单数量：ltc_usdt_sell1_quantity*order_ratio_ltc_usdt，其中order_ratio_ltc_usdt代表本策略在LTC/usdt盘口的吃单比例
        3. LTC/BTC账户中可以用来卖LTC的数量：
           ltc_available - ltc_reserve，
           其中，ltc_available表示该账户中可用的LTC数量，ltc_reserve表示该账户中应该最少预留的LTC数量
          （这个数值由用户根据自己的风险偏好来设置，越高代表用户风险偏好越低）。
        4.	BTC/usdt账户中可以用来卖BTC的BTC额度和对应的LTC个数：
            btc_available - btc_reserve, 可以置换成
            (btc_available-btc_reserve) / ltc_btc_sell1_price个LTC
            其中：btc_available表示该账户中可用的BTC数量，btc_reserve表示该账户中应该最少预留的BTC数量
           （这个数值由用户根据自己的风险偏好来设置，越高代表用户风险偏好越低）。
        5.	LTC/usdt账户中可以用来卖的usdt额度：
            usdt_available – usdt_reserve，相当于
            (usdt_available – usdt_reserve) / ltc_usdt_sell1_price个LTC
            其中，usdt_available表示该账户中可用的usdt数量，usdt_reserve表示该账户中应该最少预留的usdt数量
            （这个数值由用户根据自己的风险偏好来设置，越高代表用户风险偏好越低）。

    '''
    def get_market_sell_size(self, huobi_market):
        market_sell_size = self.market_price_tick["{0}_{1}".format(self.base_cur, self.quote_cur)].get("bids")[0][1] \
                           * self.order_ratio_base_quote
        base_mid_buy_size = self.market_price_tick["{0}_{1}".format(self.base_cur, self.mid_cur)].get("asks")[0][1] \
                            * self.order_ratio_base_mid
        base_quote_off_reserve_sell_size = \
            huobi_market.account_available(self.base_cur, self.get_market_name(self.base_cur, self.quote_cur)) \
            - self.base_quote_base_reserve
        quote_mid_off_reserve_sell_size = \
            (huobi_market.account_available(self.quote_cur, self.get_market_name(self.quote_cur, self.mid_cur)) -
             self.quote_mid_quote_reserve) / \
            self.market_price_tick["{0}_{1}".format(self.base_cur, self.quote_cur)].get("bids")[0][0]
        base_mid_off_reserve_buy_size = \
            (huobi_market.account_available(self.mid_cur, self.get_market_name(self.base_cur, self.mid_cur)) -
             self.base_mid_mid_reserve) / \
            self.market_price_tick["{0}_{1}".format(self.base_cur, self.mid_cur)].get("asks")[0][0]
        logger.info("计算数量：{0}，{1}，{2}，{3}，{4}".format(market_sell_size, base_mid_buy_size,
                    base_quote_off_reserve_sell_size, quote_mid_off_reserve_sell_size, base_mid_off_reserve_buy_size))
        return math.floor(min(market_sell_size, base_mid_buy_size, base_quote_off_reserve_sell_size,
                          quote_mid_off_reserve_sell_size, base_mid_off_reserve_buy_size) * 10000) / 10000

    '''
        正循环套利
        正循环套利的顺序如下：
        先去LTC/BTC吃单买入LTC，卖出BTC，然后根据LTC/BTC的成交量，使用多线程，
        同时在LTC/usdt和BTC/usdt市场进行对冲。LTC/usdt市场吃单卖出LTC，BTC/usdt市场吃单买入BTC。

    '''
    def buy_enter(self, huobi_market, market_buy_size):
        logger.info("多单开仓 size:{0}".format(market_buy_size))
        # return
        order_result = huobi_market.buy(cur_market_name=self.get_market_name(self.base_cur, self.quote_cur),
                                        price=self.market_price_tick["{0}_{1}".format(self.base_cur, self.quote_cur)]
                                        .get("asks")[0][0], amount=market_buy_size)
        logger.info("买入结果：{0}".format(order_result))
        time.sleep(0.2)
        if not huobi_market.order_normal(order_result,
                                         cur_market_name=self.get_market_name(self.base_cur, self.quote_cur)):
            # 交易失败
            logger.info("buy交易失败，退出 {0}".format(order_result))
            return
        # 获取真正成交量
        retry, already_close_amount = 0, 0.0
        while retry < 3:   # 循环3次检查是否交易成功
            if retry == 2:
                # 取消剩余未成交的
                huobi_market.cancel_order(order_result, self.get_market_name(self.base_cur, self.quote_cur))

                self.wait_for_cancel(huobi_market, order_result, self.get_market_name(self.base_cur, self.quote_cur))
            field_amount = float(huobi_market.get_order_processed_amount(
                order_result, cur_market_name=self.get_market_name(self.base_cur, self.quote_cur)))
            logger.info("field-amount:{0}_{1}".format(field_amount,already_close_amount))

            if field_amount-already_close_amount < self.min_trade_unit:
                logger.info("没有新的成功交易或者新成交数量太少")
                retry += 1
                continue
#            # TODO:开始对冲
#            logger.info("开始对冲，数量：{0}".format(field_amount - already_close_amount))
#            p1 = multiprocessing.Process(target=self.close_sell_cur_pair,
#                                         args=(field_amount-already_close_amount,huobi_market,
#                                               self.get_market_name(self.base_cur, self.mid_cur)))
#            p1.start()
#
#            # TODO: 这里最好直接从order_result里面获取成交的quote_cur金额，然后对冲该金额
#            quote_to_be_close = downRound((field_amount-already_close_amount)
#                                 * self.market_price_tick["{0}_{1}".format(self.base_cur, self.quote_cur)].
#                                 get("asks")[0][0], 2)
#            p2 = multiprocessing.Process(target=self.close_buy_cur_pair,
#                                         args=(quote_to_be_close, huobi_market,
#                                               self.get_market_name(self.quote_cur, self.mid_cur)))
#            p2.start()
#            p1.join()
#            p2.join()
#            already_close_amount = field_amount
#            if field_amount >= market_buy_size:  # 已经完成指定目标数量的套利
#                break
#            retry += 1
            time.sleep(0.2)
        logger.info("完成多单开仓")

    '''
        逆循环套利
        逆循环套利的顺序如下：
        先去LTC/BTC吃单卖出LTC，买入BTC，然后根据LTC/BTC的成交量，使用多线程，
        同时在LTC/usdt和BTC/usdt市场进行对冲。
        LTC/usdt市场吃单买入LTC，BTC/usdt市场吃单卖出BTC。

    '''
    def sell_enter(self, huobi_market, market_sell_size):
        logger.info("开始空单入场")
        # return
        order_result = huobi_market.sell(cur_market_name=self.get_market_name(self.base_cur, self.quote_cur),
                                         price=self.market_price_tick["{0}_{1}".format(self.base_cur, self.quote_cur)].
                                         get("bids")[0][0], amount=market_sell_size)
        if not huobi_market.order_normal(order_result,
                                         cur_market_name=self.get_market_name(self.base_cur, self.quote_cur)):
            # 交易失败
            logger.info("sell交易失败，退出 {0}".format(order_result))
            return
        time.sleep(0.2)
        # 获取真正成交量
        retry, already_close_amount = 0, 0.0
        while retry < 3:  # 循环3次检查是否交易成功
            if retry == 2:
                # 取消剩余未成交的
                huobi_market.cancel_order(order_result, self.get_market_name(self.base_cur, self.quote_cur))

                self.wait_for_cancel(huobi_market, order_result, self.get_market_name(self.base_cur, self.quote_cur))

            field_amount = float(huobi_market.get_order_processed_amount(
                    order_result, cur_market_name=self.get_market_name(self.base_cur, self.quote_cur)))
            logger.info("field_amount:{0}_{1}".format(field_amount, already_close_amount))

            if field_amount - already_close_amount < self.min_trade_unit:
                logger.info("没有新的成功交易或者新成交数量太少")
                retry += 1
                continue
            time.sleep(0.2)
        logger.info("完成空单开仓")

    def close_buy_cur_pair(self, buy_size, huobi_market, cur_pair):
        """
        对冲买入货币对
        :param buy_size: 买入数量
        :param huobi_market: 火币市场实例
        :param cur_pair: 货币对名称
        :return:
        """
        logger.info("开始买入{0}".format(cur_pair))
        try:
            order_result = huobi_market.buy(cur_market_name=cur_pair,
                                            price=self.market_price_tick["{0}".format(cur_pair)].
                                            get("asks")[0][0], amount=downRound(buy_size, 2))
            close_amount = 0.0
            time.sleep(0.2)
            logger.info("买入结果：{0}".format(order_result))
            if huobi_market.order_normal(order_result,
                                         cur_market_name=cur_pair):
                huobi_market.cancel_order(order_result, cur_pair)  # 取消未成交的order

                self.wait_for_cancel(huobi_market, order_result, cur_pair)
                close_amount = float(huobi_market.get_order_processed_amount(
                    order_result, cur_market_name=cur_pair))
            else:
                # 交易失败
                logger.info("买入{0} 交易失败 {1}".format(cur_pair, order_result))
            if buy_size > close_amount:
                # 对未成交的进行市价交易
                buy_amount = self.market_price_tick["{0}".format(cur_pair)].get("asks")[4][0] \
                             * (buy_size - close_amount)  # 市价的amount按5档最差情况预估
                buy_amount = max(HUOBI_BTC_MIN_ORDER_CASH, buy_amount)
                market_order_result = huobi_market.buy_market(cur_market_name=cur_pair, amount=downRound(buy_amount, 2))
                logger.info(market_order_result)
        except:
            logger.error(traceback.format_exc())
        logger.info("结束买入{0}".format(cur_pair))

    def close_sell_cur_pair(self, sell_size, huobi_market, cur_pair):
        """
        对冲卖出货币对
        :param sell_size: 卖出头寸
        :param huobi_market: 火币市场实例
        :param cur_pair: 货币对名称
        :return:
        """
        logger.info("开始卖出{0}".format(cur_pair))
        try:
            order_result = huobi_market.sell(cur_market_name=cur_pair,
                                             price=self.market_price_tick["{0}".format(cur_pair)].get("bids")[0][0],
                                             amount=sell_size)
            close_amount = 0.0
            time.sleep(0.2)
            logger.info("卖出结果：{0}".format(order_result))
            if huobi_market.order_normal(order_result,
                                         cur_market_name=cur_pair):
                huobi_market.cancel_order(order_result, cur_pair)
                self.wait_for_cancel(huobi_market, order_result, cur_pair)

                close_amount = float(huobi_market.get_order_processed_amount(order_result, cur_market_name=cur_pair))
            else:
                # 交易失败
                logger.info("卖出{0} 交易失败  {1}".format(cur_pair, order_result))

            if sell_size > close_amount:
                # 对未成交的进行市价交易
                sell_qty = sell_size - close_amount
                ccy_to_sell = cur_pair.split("_")[0]
                if ccy_to_sell == "btc":
                    sell_qty = max(HUOBI_BTC_MIN_ORDER_QTY, sell_qty)
                elif ccy_to_sell == "ltc":
                    sell_qty = max(HUOBI_LTC_MIN_ORDER_QTY, sell_qty)
                elif ccy_to_sell == "eth":
                    sell_qty = max(BITEX_ETH_MIN_ORDER_QTY, sell_qty)
                else:
                    sell_qty = max(BITEX_ETH_MIN_ORDER_QTY, sell_qty)

                market_order_result = huobi_market.sell_market(
                    cur_market_name=cur_pair,
                    amount=downRound(sell_qty, 3))
                logger.info(market_order_result)
        except:
            logger.error(traceback.format_exc())
        logger.info("结束卖出{0}".format(cur_pair))

    @staticmethod
    def wait_for_cancel(huobi_market, order_result, market_name):
        """
        等待order  cancel完成
        :param huobi_market: 火币市场实例
        :param order_result: 订单号
        :param market_name: 货币对市场名称
        :return:
        """
        while huobi_market.get_order_status(order_result, market_name) \
                not in [2, 3, 6, "partial-canceled", "filled", "canceled"]:    # 订单完成或者取消或者部分取消
            time.sleep(0.1)
# =============================================================================
#   getLots
# =============================================================================
    def get_currency_available(self,market,curPara):
        cur_lots=market.account_available(curPara)
        return cur_lots


if __name__ == "__main__":
    matradesys = ClassMa('tnb','btc')
#    while True:
    matradesys.strategy()
    time.sleep(matradesys.interval)
