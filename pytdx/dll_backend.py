# coding=utf-8
"""HqApi.dll backend. Public TdxHq_* only."""

import os
from ctypes import (
    WinDLL, c_int, c_ushort, c_short, c_byte, c_char_p, c_bool, POINTER,
    create_string_buffer, byref,
)

_DLL = None


def load_dll(path=None):
    global _DLL
    if _DLL is not None:
        return _DLL
    path = path or os.environ.get("HQAPI_DLL", "HqApi.dll")
    _DLL = WinDLL(path)
    return _DLL


def gbk(text):
    if text is None:
        text = ""
    if isinstance(text, bytes):
        return text
    return str(text).encode("gbk", errors="replace")


def decode(buf):
    raw = buf.raw.split(b"\x00", 1)[0]
    return raw.decode("gbk", errors="replace")


def parse_tsv(text):
    text = (text or "").strip()
    if not text:
        return []
    lines = [line for line in text.split("\n") if line != ""]
    if not lines:
        return []
    if "\t" not in lines[0]:
        return [{"text": text}]
    header = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        cols = line.split("\t")
        rows.append({header[i] if i < len(header) else str(i): cols[i] if i < len(cols) else "" for i in range(max(len(header), len(cols)))})
    return rows


def kline_category(category):
    category = int(category)
    if category == 8:
        return 7
    if category == 9:
        return 4
    return category


class HqDll(object):
    def __init__(self, path=None):
        self.dll = load_dll(path)
        self.cid = -1
        self._bind()

    def _bind(self):
        d = self.dll
        self.connect_fn = d.TdxHq_Connect
        self.connect_fn.argtypes = [c_char_p, c_ushort, c_char_p, c_char_p, c_char_p, c_char_p]
        self.connect_fn.restype = c_int
        self.disconnect_fn = d.TdxHq_Disconnect
        self.disconnect_fn.argtypes = [c_int]
        self.disconnect_fn.restype = None
        self.count_fn = d.TdxHq_GetSecurityCount
        self.count_fn.argtypes = [c_int, c_byte, POINTER(c_ushort), c_char_p]
        self.count_fn.restype = c_bool
        self.list_fn = d.TdxHq_GetSecurityList
        self.list_fn.argtypes = [c_int, c_byte, c_ushort, POINTER(c_ushort), c_char_p, c_char_p]
        self.list_fn.restype = c_bool
        self.bars_fn = d.TdxHq_GetSecurityBars
        self.bars_fn.argtypes = [c_int, c_byte, c_byte, c_char_p, c_ushort, POINTER(c_ushort), c_char_p, c_char_p]
        self.bars_fn.restype = c_bool
        self.index_fn = d.TdxHq_GetIndexBars
        self.index_fn.argtypes = [c_int, c_byte, c_byte, c_char_p, c_ushort, POINTER(c_ushort), c_char_p, c_char_p]
        self.index_fn.restype = c_bool
        self.minute_fn = d.TdxHq_GetMinuteTimeData
        self.minute_fn.argtypes = [c_int, c_byte, c_char_p, c_char_p, c_char_p]
        self.minute_fn.restype = c_bool
        self.hminute_fn = d.TdxHq_GetHistoryMinuteTimeData
        self.hminute_fn.argtypes = [c_int, c_byte, c_char_p, c_int, c_char_p, c_char_p]
        self.hminute_fn.restype = c_bool
        self.tick_fn = d.TdxHq_GetTransactionData
        self.tick_fn.argtypes = [c_int, c_byte, c_char_p, c_ushort, POINTER(c_ushort), c_char_p, c_char_p]
        self.tick_fn.restype = c_bool
        self.htick_fn = d.TdxHq_GetHistoryTransactionData
        self.htick_fn.argtypes = [c_int, c_byte, c_char_p, c_ushort, POINTER(c_ushort), c_int, c_char_p, c_char_p]
        self.htick_fn.restype = c_bool
        self.quotes_fn = d.TdxHq_GetSecurityQuotes
        self.quotes_fn.argtypes = [c_int, POINTER(c_byte), POINTER(c_char_p), POINTER(c_ushort), c_char_p, c_char_p]
        self.quotes_fn.restype = c_bool
        self.quotes10_fn = d.TdxHq_GetSecurityQuotes10
        self.quotes10_fn.argtypes = [c_int, POINTER(c_byte), POINTER(c_char_p), POINTER(c_ushort), c_char_p, c_char_p]
        self.quotes10_fn.restype = c_bool
        self.detail_fn = d.TdxHq_GetDetailTransactionData
        self.detail_fn.argtypes = [c_int, c_byte, c_char_p, c_int, POINTER(c_ushort), c_char_p, c_char_p]
        self.detail_fn.restype = c_bool
        self.order_fn = d.TdxHq_GetDetailOrderData
        self.order_fn.argtypes = [c_int, c_byte, c_char_p, c_int, POINTER(c_ushort), c_char_p, c_char_p]
        self.order_fn.restype = c_bool
        self.company_fn = d.TdxHq_GetCompanyInfoCategory
        self.company_fn.argtypes = [c_int, c_byte, c_char_p, c_char_p, c_char_p]
        self.company_fn.restype = c_bool
        self.content_fn = d.TdxHq_GetCompanyInfoContent
        self.content_fn.argtypes = [c_int, c_byte, c_char_p, c_char_p, c_int, c_int, c_char_p, c_char_p]
        self.content_fn.restype = c_bool
        self.xdxr_fn = d.TdxHq_GetXDXRInfo
        self.xdxr_fn.argtypes = [c_int, POINTER(c_byte), POINTER(c_char_p), c_int, c_char_p, c_char_p]
        self.xdxr_fn.restype = c_bool
        self.finance_fn = d.TdxHq_GetFinanceInfo
        self.finance_fn.argtypes = [c_int, POINTER(c_byte), POINTER(c_char_p), c_int, c_char_p, c_char_p]
        self.finance_fn.restype = c_bool
        self.block_fn = d.TdxHq_GetBlockInfo
        self.block_fn.argtypes = [c_int, c_char_p, c_char_p, c_char_p]
        self.block_fn.restype = c_bool

    def buffers(self):
        return create_string_buffer(1024 * 1024), create_string_buffer(256)

    def connect(self, ip, port, account, password):
        result, err = self.buffers()
        self.cid = self.connect_fn(gbk(ip), int(port), gbk(account), gbk(password), result, err)
        self.last_error = decode(err)
        return self.cid

    def disconnect(self):
        if self.cid >= 0:
            self.disconnect_fn(self.cid)
            self.cid = -1

    def _rows(self, ok, result, err):
        if not ok:
            raise RuntimeError(decode(err) or "Api.dll call failed")
        return parse_tsv(decode(result))

    def security_count(self, market):
        err = create_string_buffer(256)
        count = c_ushort(0)
        ok = self.count_fn(self.cid, int(market), byref(count), err)
        if not ok:
            raise RuntimeError(decode(err) or "GetSecurityCount failed")
        return int(count.value)

    def security_list(self, market, start, count=1000):
        result, err = self.buffers()
        n = c_ushort(int(count))
        ok = self.list_fn(self.cid, int(market), int(start), byref(n), result, err)
        return self._rows(ok, result, err)

    def bars(self, category, market, code, start, count, index=False):
        result, err = self.buffers()
        n = c_ushort(int(count))
        fn = self.index_fn if index else self.bars_fn
        ok = fn(self.cid, kline_category(category), int(market), gbk(code), int(start), byref(n), result, err)
        return self._rows(ok, result, err)

    def minute(self, market, code, date=None):
        result, err = self.buffers()
        if date:
            ok = self.hminute_fn(self.cid, int(market), gbk(code), int(date), result, err)
        else:
            ok = self.minute_fn(self.cid, int(market), gbk(code), result, err)
        return self._rows(ok, result, err)

    def ticks(self, market, code, start, count, date=None):
        result, err = self.buffers()
        n = c_ushort(int(count))
        if date:
            ok = self.htick_fn(self.cid, int(market), gbk(code), int(start), byref(n), int(date), result, err)
        else:
            ok = self.tick_fn(self.cid, int(market), gbk(code), int(start), byref(n), result, err)
        return self._rows(ok, result, err)

    def quotes(self, pairs, level2=False):
        result, err = self.buffers()
        n = len(pairs)
        markets = (c_byte * n)(*[int(m) for m, _ in pairs])
        codes = (c_char_p * n)(*[gbk(c) for _, c in pairs])
        count = c_ushort(n)
        fn = self.quotes10_fn if level2 else self.quotes_fn
        ok = fn(self.cid, markets, codes, byref(count), result, err)
        return self._rows(ok, result, err)

    def detail(self, market, code, start, count, orders=False):
        result, err = self.buffers()
        n = c_ushort(int(count))
        fn = self.order_fn if orders else self.detail_fn
        ok = fn(self.cid, int(market), gbk(code), int(start), byref(n), result, err)
        return self._rows(ok, result, err)

    def company(self, market, code):
        result, err = self.buffers()
        ok = self.company_fn(self.cid, int(market), gbk(code), result, err)
        return self._rows(ok, result, err)

    def company_content(self, market, code, filename, start, length):
        result, err = self.buffers()
        ok = self.content_fn(self.cid, int(market), gbk(code), gbk(filename), int(start), int(length), result, err)
        if not ok:
            raise RuntimeError(decode(err) or "GetCompanyInfoContent failed")
        return decode(result)

    def xdxr(self, market, code):
        result, err = self.buffers()
        markets = (c_byte * 1)(int(market))
        codes = (c_char_p * 1)(gbk(code))
        ok = self.xdxr_fn(self.cid, markets, codes, 1, result, err)
        return self._rows(ok, result, err)

    def finance(self, market, code):
        result, err = self.buffers()
        markets = (c_byte * 1)(int(market))
        codes = (c_char_p * 1)(gbk(code))
        ok = self.finance_fn(self.cid, markets, codes, 1, result, err)
        return self._rows(ok, result, err)

    def block(self, blockfile):
        result, err = self.buffers()
        ok = self.block_fn(self.cid, gbk(blockfile or ""), result, err)
        return self._rows(ok, result, err)


class ExHqDll(object):
    def __init__(self, path=None):
        self.dll = load_dll(path)
        self.cid = -1
        d = self.dll
        self.connect_fn = d.TdxExHq_Connect
        self.connect_fn.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_char_p]
        self.connect_fn.restype = c_int
        self.disconnect_fn = d.TdxExHq_Disconnect
        self.disconnect_fn.argtypes = [c_int]
        self.disconnect_fn.restype = None
        self.markets_fn = d.TdxExHq_GetMarkets
        self.markets_fn.argtypes = [c_int, c_char_p, c_char_p]
        self.markets_fn.restype = c_bool
        self.count_fn = d.TdxExHq_GetInstrumentCount
        self.count_fn.argtypes = [c_int, POINTER(c_int), c_char_p]
        self.count_fn.restype = c_bool
        self.info_fn = d.TdxExHq_GetInstrumentInfo
        self.info_fn.argtypes = [c_int, c_int, c_short, c_char_p, c_char_p]
        self.info_fn.restype = c_bool
        self.bars_fn = d.TdxExHq_GetInstrumentBars
        self.bars_fn.argtypes = [c_int, c_byte, c_byte, c_char_p, c_int, POINTER(c_short), c_char_p, c_char_p]
        self.bars_fn.restype = c_bool
        self.minute_fn = d.TdxExHq_GetMinuteTimeData
        self.minute_fn.argtypes = [c_int, c_byte, c_char_p, c_char_p, c_char_p]
        self.minute_fn.restype = c_bool
        self.hminute_fn = d.TdxExHq_GetHistoryMinuteTimeData
        self.hminute_fn.argtypes = [c_int, c_byte, c_char_p, c_int, c_char_p, c_char_p]
        self.hminute_fn.restype = c_bool
        self.tick_fn = d.TdxExHq_GetTransactionData
        self.tick_fn.argtypes = [c_int, c_byte, c_char_p, c_int, POINTER(c_short), c_char_p, c_char_p]
        self.tick_fn.restype = c_bool
        self.htick_fn = d.TdxExHq_GetHistoryTransactionData
        self.htick_fn.argtypes = [c_int, c_byte, c_char_p, c_int, c_int, POINTER(c_short), c_char_p, c_char_p]
        self.htick_fn.restype = c_bool
        self.quote_fn = d.TdxExHq_GetInstrumentQuote
        self.quote_fn.argtypes = [c_int, c_byte, c_char_p, c_char_p, c_char_p]
        self.quote_fn.restype = c_bool

    def buffers(self):
        return create_string_buffer(1024 * 1024), create_string_buffer(256)

    def connect(self, ip, port, account, password):
        result, err = self.buffers()
        self.cid = self.connect_fn(gbk(ip), int(port), gbk(account), gbk(password), result, err)
        self.last_error = decode(err)
        return self.cid

    def disconnect(self):
        if self.cid >= 0:
            self.disconnect_fn(self.cid)
            self.cid = -1

    def _rows(self, ok, result, err):
        if not ok:
            raise RuntimeError(decode(err) or "Api.dll call failed")
        return parse_tsv(decode(result))

    def markets(self):
        result, err = self.buffers()
        return self._rows(self.markets_fn(self.cid, result, err), result, err)

    def instrument_count(self):
        err = create_string_buffer(256)
        n = c_int(0)
        ok = self.count_fn(self.cid, byref(n), err)
        if not ok:
            raise RuntimeError(decode(err) or "GetInstrumentCount failed")
        return int(n.value)

    def instrument_info(self, start, count):
        result, err = self.buffers()
        return self._rows(self.info_fn(self.cid, int(start), int(count), result, err), result, err)

    def bars(self, category, market, code, start, count):
        result, err = self.buffers()
        n = c_short(int(count))
        ok = self.bars_fn(self.cid, kline_category(category), int(market), gbk(code), int(start), byref(n), result, err)
        return self._rows(ok, result, err)

    def minute(self, market, code, date=None):
        result, err = self.buffers()
        if date:
            ok = self.hminute_fn(self.cid, int(market), gbk(code), int(date), result, err)
        else:
            ok = self.minute_fn(self.cid, int(market), gbk(code), result, err)
        return self._rows(ok, result, err)

    def ticks(self, market, code, start, count, date=None):
        result, err = self.buffers()
        n = c_short(int(count))
        if date:
            ok = self.htick_fn(self.cid, int(market), gbk(code), int(date), int(start), byref(n), result, err)
        else:
            ok = self.tick_fn(self.cid, int(market), gbk(code), int(start), byref(n), result, err)
        return self._rows(ok, result, err)

    def quote(self, market, code):
        result, err = self.buffers()
        return self._rows(self.quote_fn(self.cid, int(market), gbk(code), result, err), result, err)
