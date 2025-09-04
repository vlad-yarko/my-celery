import time
import asyncio

from celery import Celery
from celery.signals import task_prerun, task_postrun, task_failure, worker_ready

from asgiref.sync import async_to_sync


BROKER_URL = "redis://localhost:6379/0"
BACKEND_URL = "redis://localhost:6379/1"


app = Celery(
    "my-celery",
    broker=BROKER_URL,
    backend=BACKEND_URL
)

app.conf.result_expires = 3600 # one hour
app.conf.broker_connection_retry_on_startup = True


@app.task(bind=True, max_retries=3, default_retry_delay=5, queue="reverse")
def reverse(self, text):
    try:
        time.sleep(5)
        return text[::-1]
    except Exception as e:
        raise self.retry(exc=e)
    
    
@app.task(bind=True)
def say_hello(self):
    print("YEP")
    
    
async def square(number: int) -> int:
    return number ** 2
    
    
@app.task(bind=True, queue="async")
def not_async(self, number: int):
    try:
        async_to_sync(asyncio.sleep)(4)
        result = async_to_sync(square)(number)
        return result
    except Exception as e:
        raise self.retry(exc=e)


app.conf.beat_schedule = {
    "hello-every-10-seconds" : {
        "task": "tasks.say_hello", # <module_name>.<function>
        "schedule": 10.0 # Every 10 seconds
    }
}


@task_prerun.connect
def before_task(task_id, task, args, kwargs, **_):
    print(f"Starting task {task.name} ({task_id}) with args={args}")

@task_postrun.connect
def after_task(task_id, task, args, kwargs, retval, **_):
    print(f"Finished task {task.name}, result={retval}")

@task_failure.connect
def task_failed(task_id, exception, args, kwargs, traceback, einfo, **_):
    print(f"Task {task_id} failed with {exception}")

@worker_ready.connect
def worker_started(sender, **kwargs):
    print("Worker is ready!")
