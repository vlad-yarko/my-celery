import time

from tasks import reverse


result = reverse.delay("hello")

print(result.status)

i = 0
# while i < 120:
#     print(f"{i}s: {result.status}")
#     i += 1
#     time.sleep(1)

print(result.get())
