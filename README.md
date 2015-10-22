## 项目名

`profiler_online`

### 介绍:
用来解析查找python程序可能存在的各方面性能或者奇葩问题的工具,通过web访问访问可以直接拿到火焰吐.

Add Future:

* 加入内存的相关信息
* 查询时间范围

### 用法:

这边已经封装好了，你需要做的只是把性能分析模块引入到你的应用里面.

```
from profiler_online import run_profiler
run_profiler()
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


