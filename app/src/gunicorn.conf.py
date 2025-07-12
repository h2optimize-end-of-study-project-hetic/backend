# https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

import multiprocessing

bind = "0.0.0.0:80"

# backlog - The number of pending connections
backlog = 2048

# workers - The number of worker processes that this server should keep alive for handling requests.
workers = multiprocessing.cpu_count() * 2 + 1

# worker_class - The type of workers to use.
worker_class = "uvicorn.workers.UvicornWorker"

# worker_connections - For the eventlet and gevent worker classes this limits the maximum number of simultaneous clients that  a single process can handle.
worker_connections = 1000

# timeout - If a worker does not notify the master process in this number of seconds it is killed and a new worker is spawned to replace it.
timeout = 30

# keepalive - The number of seconds to wait for the next request on a Keep-Alive HTTP connection.
keepalive = 2

# daemon - Detach the main Gunicorn process from the controlling terminal with a standard fork/fork sequence.
daemon = False

errorlog = '-'

# loglevel - The granularity of log output :  A string of "debug", "info", "warning", "error", "critical"
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

preload_app = True

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    ## get traceback info
    import threading, sys, traceback
    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))

def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
