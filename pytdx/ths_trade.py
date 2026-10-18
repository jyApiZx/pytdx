# coding=utf-8
"""Optional trade client. Loads thsapi.dll only when this module is used."""

import os
from ctypes import WinDLL, c_int, c_short, c_float, c_char_p, create_string_buffer


def _gbk(text):
    if text is None:
        text = ""
    if isinstance(text, bytes):
        return text
    return str(text).encode("gbk", errors="replace")


def _decode(buf):
    return buf.raw.split(b"\x00", 1)[0].decode("gbk", errors="replace")


class ThsTrade(object):
    def __init__(self, path=None):
        self.dll = WinDLL(path or os.environ.get("THSAPI_DLL", "thsapi.dll"))
        self.client_id = -1
        self.dll.Init.argtypes = []
        self.dll.Init()
        self.logon = self.dll.Logon
        self.logon.argtypes = [c_char_p, c_short, c_char_p, c_short, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p]
        self.logon.restype = c_int
        self.query = self.dll.QueryData
        self.query.argtypes = [c_int, c_int, c_char_p, c_char_p]
        self.query.restype = c_int
        self.send = self.dll.SendOrder
        self.send.argtypes = [c_int, c_int, c_int, c_char_p, c_char_p, c_float, c_int, c_char_p, c_char_p]
        self.cancel = self.dll.CancelOrder
        self.cancel.argtypes = [c_int, c_char_p, c_char_p, c_char_p, c_char_p]

    def login(self, ip, port, account, password, config='{"qs_id":356,"account_type":0}', yyb=48):
        err = create_string_buffer(256)
        self.client_id = self.logon(_gbk(ip), int(port), _gbk(config), int(yyb), _gbk(account), _gbk(account), _gbk(password), _gbk(""), err)
        if self.client_id < 0:
            raise RuntimeError(_decode(err) or "Logon failed")
        return self.client_id

    def query_data(self, category):
        result = create_string_buffer(1024 * 1024)
        err = create_string_buffer(256)
        code = self.query(self.client_id, int(category), result, err)
        if code != 0:
            raise RuntimeError(_decode(err) or "QueryData failed")
        return _decode(result)

    def order(self, category, price, amount, shareholder="", code="", price_type=0):
        result = create_string_buffer(1024 * 1024)
        err = create_string_buffer(256)
        self.send(self.client_id, int(category), int(price_type), _gbk(shareholder), _gbk(code), float(price), int(amount), result, err)
        message = _decode(err).strip()
        if message:
            raise RuntimeError(message)
        return _decode(result)

    def cancel_order(self, exchange_id, order_id):
        result = create_string_buffer(1024 * 1024)
        err = create_string_buffer(256)
        self.cancel(self.client_id, _gbk(exchange_id), _gbk(order_id), result, err)
        message = _decode(err).strip()
        if message:
            raise RuntimeError(message)
        return _decode(result)
