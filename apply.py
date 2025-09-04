import time

from tasks import reverse


result = reverse.apply(args=("hello", ), kwargs={})

print(result.status)

print(result.get())
