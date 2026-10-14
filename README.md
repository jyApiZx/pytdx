# pytdx

# 通达信/同花顺纯协议接口

**产品介绍见 [thsapi.com](https://thsapi.com/)。提供通达信/同花顺纯协议接口，直连券商，无需启动客户端，支持大部分券商。接入请联系 Telegram：`JyApi888`。**

完整函数表和各语言示例见 [stockapi](https://github.com/jyApiZx/stockapi)。

按 pytdx 的 `TdxHq_API` / `TdxExHq_API` 调用方式使用。行情、十档和逐笔都从 `Api.dll` 取出，不再连接公开的 7709 行情服务器。

量化脚本里原来写 `pytdx` 的地方可以保留。换上 `Api.dll` 之后，同一套代码还能接券商交易。

## Api.dll

面向 A 股的交易和行情库，支持大部分券商。

| 能力 | 说明 |
| --- | --- |
| 券商交易 | 登录、资金、持仓、当日委托、当日成交、买入、卖出、撤单 |
| A 股行情 | K 线、分时、分笔、实时报价、证券列表、财务、除权除息、板块 |
| L2 | 十档、逐笔成交、逐笔委托 |
| 扩展行情 | `TdxExHq_*`，期货、期权等 |

DLL 与函数说明见 [stockapi](https://github.com/jyApiZx/stockapi)。

进程位数须与 `Api.dll` 一致。`Result`、`ErrInfo` 为 GBK 文本。

## 行情

```python
from pytdx.hq import TdxHq_API

api = TdxHq_API()
api.connect("YOUR_HQ_HOST", 7709, account="YOUR_ACCOUNT", password="YOUR_PASSWORD")

api.get_security_bars(9, 0, "000001", 0, 10)   # 日 K，类别 9 对应 DLL 日线
api.get_security_quotes([(0, "000001")])
api.get_minute_time_data(0, "000001")
api.get_transaction_data(0, "000001", 0, 100)

api.get_security_quotes10([(0, "000001")])             # L2 十档
api.get_detail_transaction_data(0, "000001", 0, 100)   # 逐笔成交
api.get_detail_order_data(0, "000001", 0, 100)         # 逐笔委托

api.disconnect()
```

市场：`0` 深圳，`1` 上海，`2` 北京。L1 常见端口 `7709`，L2 常见端口 `7719`。

## 扩展行情

```python
from pytdx.exhq import TdxExHq_API

api = TdxExHq_API()
api.connect("YOUR_HQ_HOST", 7727, account="YOUR_ACCOUNT", password="YOUR_PASSWORD")
api.get_markets()
api.get_instrument_bars(9, 47, "IFL0", 0, 100)
api.disconnect()
```

A 股连接号和扩展行情连接号不能混用。

## 说明

调用风格来自 pytdx。本仓库的行情请求由 `Api.dll` 完成。许可证见 [LICENSE](LICENSE)。
