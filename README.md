# simple-proxy-pool

原定写个简单代理池，但目前 simple_pp 实际是个异步并发IP代理验证工具，速度很快，一千个代理半分钟左右可完成。

### 安装

```pip install -U simple-proxy-pool```

或下载 repo (e.g., ```git clone https://github.com/ffreemt/simple-proxy-pool.git``` 换到 simple-proxy-pool目录执行 ```
python setup.py develop```

### 原理

经过IP代理访问 www.baidu.com, 能成功获取百度返回的头则代理有效。再检查头里面时候含'via', 不含'via'即为匿名代理。参考 aio_headers.py。

### 用法

#### 命令行

```python -m simple_pp``` 贴入需验证的IP代理（格式 ip:端口, 以空格、回车非数字字母或中文隔开）。或：

```python -m simple_pp file1 file2 ...``` 文件内含以上格式的IP代理

也可以用pipe，例如
```
curl "https://www.freeip.top/?page=1" | python -m simple_pp
```

#### python 程序内调用
```
from simple_pp import simple_pp
from pprint import pprint

ip_list = [ip1, ip2, ...]
res = simple_pp(ip_list)
pprint(res)
```

输出 res 里格式为: res[0] = ip_list[0] + （是否有效，是否匿名，响应时间秒）

可参看tests 里面的文件。有疑问或反馈可发 Issues。

例如
```
import asyncio
import httpx
from simple_pp import simple_pp

simple_pp(['113.53.230.167:80', '36.25.243.51:80'])
#-> [('113.53.230.167:80', True, False, 0.31),
# ('36.25.243.51:80', True, True, 0.51)]
# 第一个代理为透明代理，第二个代理为匿名代理

```
也可以直接将网页结果送给 simple_pp, 例如
```
import re
import asyncio
import httpx
from pprint import pprint
from simple_pp import simple_pp

arun = lambda x: asyncio.get_event_loop().run_until_complete(x)
_ = [elm for elm in simple_pp([':'.join(elm) if elm[1] else elm[0] for elm in re.findall(r'(?:https?://)?(\d{1,3}(?:\.\d{1,3}){3})(?:[\s\t:\'",]+(\d{1,4}))?', arun(httpx.get('https://www.freeip.top/?page=1')).text)]) if elm[-3] is True]
pprint(_)
# 可能拿到将近 10 个代理
# 或
_ = [elm for elm in simple_pp(arun(httpx.get('https://www.freeip.top/?page=1')).text) if elm[-3] is True]
pprint(_)
# ditto

```

### Acknowledgments

* 含 jhao 的 proxypool 项目里的几个文件， 但并未使用，可能将来会用。先感谢jhao开源。
