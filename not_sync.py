import time

from tasks import not_async


result = not_async.apply_async(args=(2, ))

i = 0
while i < 10:
    print(f"{i}s: {result.status}")
    i += 1
    time.sleep(1)

print(result.get())
