# pytdx

# 同花顺交易接口

**同花顺交易接口，L1、L2 行情接口。直连券商，无需启动客户端，支持大部分券商。产品介绍见 [thsapi.com](https://thsapi.com/)。技术支持请联系 [Telegram：@Thsapi](https://t.me/Thsapi)**

不点屏幕，不抢鼠标，程序直接连券商。下载后用模拟盘就能测查询、下单和撤单。已经有项目时，打开 [AI 代做提示词](https://thsapi.com/ai.html)，把提示词交给正在改项目的 AI。行情有 L1，也有十档、买卖队列和逐笔。

账户安全说明：接口不上传交易密码、持仓、委托或成交；本地授权不连接授权服务器。价格和开通方式见 [官网授权方式](https://thsapi.com/#license)。完整的联网范围、安全测试和自行核验方法见 [账户安全与授权](https://thsapi.com/security.html)。

通达信行情的 Python 调用。`TdxHq_API.connect` 仍然连接原来的 7709 行情主站，已有脚本不用改。

老的 `TdxHqApi` 已经没人维护。需要心跳、断线重连，以及后来补上的函数时，改用 `connect_hqapi`，加载 [HqApi.dll](https://github.com/jyApiZx/stockapi)。L1 是实时行情、Tick、买卖五档，以及一分钟、五分钟 K 线。L2 是十档、买卖队列和逐笔，端口 7719，账号不要加前缀。使用 L2 数据，需要先具有 L2 账户：[通达信L2普及版](https://vip.tdx.com.cn/site/app/pc-mall/main.html#/page_product_pj_cf?param=%7B%22categoryId%22%3A%224%22%7D)。连接断了由 DLL 自己重连。

行情包：[64 位](https://github.com/jyApiZx/stockapi/releases/download/hqapi-1.0.6/hqapi_1.0.6_x64.zip)、[32 位](https://github.com/jyApiZx/stockapi/releases/download/hqapi-1.0.6/hqapi_1.0.6_x32.zip)。交易不放在行情类里，要用同花顺交易接口下单时看 `pytdx.ths_trade`，DLL 是 `thsapi.dll`。客户端方式下单慢，也容易漏单、错单，同花顺交易接口是直接连券商。交易包：[64 位](https://github.com/jyApiZx/stockapi/releases/download/v1.0.6.1/thsapi_1.0.6.1_x64.zip)、[32 位](https://github.com/jyApiZx/stockapi/releases/download/v1.0.6.1/thsapi_1.0.6.1_x32.zip)。

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
