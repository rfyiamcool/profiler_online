#coding:utf-8
import collections
import signal
import time
import gevent
import threading
import subprocess
from werkzeug.serving import BaseWSGIServer, WSGIRequestHandler
from werkzeug.wrappers import Request, Response
from profiler_online.log import init_logger
import os

logger = init_logger('debug.log')

class Sampler(object):
    def __init__(self, interval=0.005):
        self.interval = interval
        self._started = None
        self._stack_counts = collections.defaultdict(int)

    def start(self):
        self._started = time.time()
        try:
            signal.signal(signal.SIGVTALRM, self._sample)
        except ValueError:
            raise ValueError('Can only sample on the main thread')

        signal.setitimer(signal.ITIMER_VIRTUAL, self.interval, 0)

    def _sample(self, signum, frame):
        stack = []
        while frame is not None:
            stack.append(self._format_frame(frame))
            frame = frame.f_back

        stack = ';'.join(reversed(stack))
        self._stack_counts[stack] += 1
        signal.setitimer(signal.ITIMER_VIRTUAL, self.interval, 0)

    def _format_frame(self, frame):
        return '{}({})'.format(frame.f_code.co_name,
                               frame.f_globals.get('__name__'))

    def output_stats(self):
        if self._started is None:
            return ''
        elapsed = time.time() - self._started
        lines = ['elapsed {}'.format(elapsed),
                 'granularity {}'.format(self.interval)]
        ordered_stacks = sorted(self._stack_counts.items(),
                                key=lambda kv: kv[1], reverse=True)
        lines.extend(['{} {}'.format(frame, count)
                      for frame, count in ordered_stacks])
        return '\n'.join(lines) + '\n'

    def reset(self):
        self._started = time.time()
        self._stack_counts = collections.defaultdict(int)


class Emitter(object):
    def __init__(self, sampler, host, port, tmp_path):
        self.sampler = sampler
        self.host = host
        self.port = port
        self.tmp_path = tmp_path

    def handle_request(self, environ, start_response):
        stats = self.sampler.output_stats()
        request = Request(environ)
        if request.args.get('reset') in ('1', 'true'):
            self.sampler.reset()
        with open('debug.out','w') as f:
            f.write(stats)
        
        cmdstr = 'cat %s/debug.out | profiler_online/tools/flamegraph.pl'%self.tmp_path
        p = subprocess.Popen(cmdstr, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        stats = p.stdout.read()
        response = Response(stats,mimetype='text/html')
        return response(environ, start_response)

    def run(self):
        server = BaseWSGIServer(self.host, self.port, self.handle_request,
                                _QuietHandler)
        logger.info('Serving profiles on port {}'.format(self.port))
        server.serve_forever()


class _QuietHandler(WSGIRequestHandler):
    def log_request(self, *args, **kwargs):
        """Suppress request logging so as not to pollute application logs."""
        pass

def run_profiler(host='0.0.0.0', port=8080, tmp_path=os.getcwd()):
    try:
        gevent.spawn(run_worker,host,port,tmp_path)
    except e:
        t = threading.Thread(target=run_worker,args=(host,port,tmp_path))
        t.start()

def run_worker(host,port,tmp_path):
    sampler = Sampler()
    sampler.start()
    e = Emitter(sampler, host, port, tmp_path)
    e.run()

