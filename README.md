# pytdx

通达信行情的 Python 调用。`TdxHq_API.connect` 仍然连接原来的 7709 行情主站，已有脚本不用改。

老的 `TdxHqApi` 已经没人维护。需要心跳、断线重连，以及后来补上的函数时，改用 `connect_hqapi`，加载 [HqApi.dll](https://github.com/jyApiZx/stockapi)。公开这一版是 L1：实时行情、Tick、买卖五档，以及一分钟、五分钟 K 线。连接断了由 DLL 自己重连。

行情包：[64 位](https://github.com/jyApiZx/stockapi/releases/download/v1.1.0/HqApi-x64.zip)、[32 位](https://github.com/jyApiZx/stockapi/releases/download/v1.1.0/HqApi-x32.zip)。交易不放在行情类里，要用纯协议下单时看 `pytdx.ths_trade`，DLL 是 `thsapi.dll`。客户端方式下单慢，也容易漏单、错单，纯协议是直接连券商。交易包：[64 位](https://github.com/jyApiZx/stockapi/releases/download/v1.0.2/thsapi_1.0.2_x64.zip)、[32 位](https://github.com/jyApiZx/stockapi/releases/download/v1.0.2/thsapi_1.0.2_x32.zip)。

## 原来的行情

```python
from pytdx.hq import TdxHq_API

api = TdxHq_API()
api.connect("101.227.73.20", 7709)
api.get_security_bars(9, 0, "000001", 0, 10)
api.disconnect()
```

## HqApi

```python
from pytdx.hq import TdxHq_API

api = TdxHq_API()
api.connect_hqapi("101.227.73.20", 7709, account="L1*YOUR_ACCOUNT", password="YOUR_PASSWORD")
api.get_security_bars(9, 0, "000001", 0, 10)
api.disconnect()
```

账号写成 `L1*账号`，密码自己生成一串非空字符。程序位数要和 `HqApi.dll` 一致。

扩展行情 `TdxExHq_API` 仍走原来的端口，不要拿 A 股的 HqApi 连接号去调它。
