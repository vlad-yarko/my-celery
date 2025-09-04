from tasks import app


app.worker_main(argv=[
    "worker",
    "-Q", "reverse",
    "-P", "gevent",
    "--concurrency=50",
    "--autoscale=200,50",
    '--loglevel=INFO',
    '-n', "reverseWorker"
])
