# -*- coding: utf-8 -*-

import json

def ops_renderJSON( code = 200,msg = "操作成功~~",data = {} ):
    resp = { "code":code,"msg":msg,"data":data }
    result = json.dumps(resp, ensure_ascii=False)
    return result

def ops_renderErrJSON( msg = "系统繁忙，请稍后再试~~",data = {} ):
    return ops_renderJSON( code = -1,msg = msg,data = data )
