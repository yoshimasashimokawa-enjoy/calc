# -*- coding: utf-8 -*-
import json
import os
import re

from fastapi import FastAPI, render_template, redirect, request, session

application = FastAPI(__name__)
application.secret_key = 'secret'

DATA_FILE = 'clacdata.json'

# 計算機能
def calc_data(formula, button):
    """式を演算する
    :param formula:　これまで入力された演算式
    :type formula: str
    :param button: 押しされたボタン
    :type button: str
    :return: None
    """

    SYMBOL = ["*","+","-","/","%","."]
    ans = ""

    if button == '=':
        if formula[-1:] in SYMBOL: # 記号の場合、記号より前で計算
            formula = formula[:-1]

        if re.findall(r"/0", formula) != []:
            zero1 =  len(re.findall(r"/0", formula))
            zero2 = len(re.findall(r"/0.\d+", formula))
            if zero1 != zero2:
                ans = "ERROR"
            else:
                ans = '= ' + str(eval(formula))
        else:
            ans = '= ' + str(eval(formula))
    elif button == 'AC': #クリアの場合
        formula = ''
    elif button == '+/-': # 正負符号の場合
        formula = str(eval(formula)) + "*(-1)"
    elif button in SYMBOL: # 記号の場合
        if formula[-1:] not in SYMBOL and formula[-1:] != '':
            formula += button
        elif formula[-1:] in SYMBOL: # 記号の場合入れ替える
            formula = formula[:-1] + button
    else: #数字などの場合
        formula += button

    res = [formula,ans]

    return res
