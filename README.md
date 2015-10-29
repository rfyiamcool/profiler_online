## 项目名

`profiler_online`  

更多profiler_online相关信息，转到这个链接 [xiaorui.cc](http://xiaorui.cc/2015/10/22/%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE%E4%B9%8B%E8%B0%83%E8%AF%95python%E5%BA%94%E7%94%A8%E7%94%9F%E6%88%90%E6%80%A7%E8%83%BDcpu%E7%81%AB%E7%84%B0%E5%9B%BE/)

### 介绍:
用来解析查找python程序可能存在的各方面性能或者奇葩问题的工具,通过web访问访问可以直接拿到火焰图.

本项目是基于FlameGraph封装的,他本身是perl开发的,我就地封了一层调用,外加了web展现.这样对于python工程师来说，可以方便的把调试功能加入应用里面.

*Gregg开发的FlameGraph源码*

[https://github.com/brendangregg/FlameGraph](https://github.com/brendangregg/FlameGraph)

*Python systemTap参考文档*

[https://github.com/nylas/nylas-perftools](https://github.com/nylas/nylas-perftools)

Will Add Future:

* 加入更完善的信号控制
* 加入内存的相关信息
* 查询时间范围

### 安装:

**pypi**

```
pip install profiler_online
```

**源码安装**

```
git clone https://github.com/rfyiamcool/profiler_online.git
cd profiler_online
python setup.py install
```

### 用法:

这边已经封装好了，你需要做的只是把性能分析模块引入到你的应用里面.

```
from profiler_online import run_profiler
run_profiler()
```

run_profiler支持三个参数:
```
debug_config = {
    'host': '127.0.0.1',
    'port': 8080,
    'tmp_path: '/tmp/debug'
}
run_profiler(**debug_config)
```

### 测试:

打开浏览器 http://127.0.0.1:8080  这样就可以显示正在运行服务的性能火焰图了.

![image](https://github.com/rfyiamcool/profiler_online/raw/master/img/demo.png)

### 问题:

下面是以前创建火焰图的方法.

```
python test.py
curl "127.0.0.1:8080" | profiler_online/tools/flamegraph.pl > flame.html
```

改进的方法:
```
直接浏览器打开,地址栏 --> 127.0.0.1:8080
```

在开发过程中,遇到了python系统调用时不能正常捕获输出. 现在已经改为临时文件的方式.
```
cmdstr = './profiler_online/tools/flamegraph.pl'
p = subprocess.Popen(cmdstr, stdin = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
p.stdin.write(stats)
p.stdin.flush()
try:
    if p.stderr:
        stats = p.stderr.read()
        p.stderr.flush()
    if p.stdout:
        stats = p.stdout.read()
except Exception, e:
    print e,Exception
```


