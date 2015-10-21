## profiler_online

### 介绍
用来解析查找python程序存在的各方面性能或者奇葩问题的工具.

### 用法
这边已经封装好了，你需要做的只是把性能分析模块引入到你的应用里面.
```
from profiler_online import run_profiler
run_profiler()
```

### 测试

```
python test.py
curl "127.0.0.1:8080" | profiler_online/tools/flamegraph.pl > flame.svg
```
