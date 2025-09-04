import time

from tasks import reverse


result = reverse.apply_async(args=("hello", ), kwargs={})

i = 0
while i < 20:
    print(f"{i}s: {result.status}")
    i += 1
    time.sleep(1)

print(result.get())
