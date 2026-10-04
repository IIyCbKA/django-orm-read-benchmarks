import os
import statistics
import sys
import time

import django
django.setup()

from core.models import Booking

from django.db import connection
connection.ensure_connection()

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '25'))
LIMIT = int(os.environ.get('LIMIT', '1000'))


def select_iteration() -> int:
  start = time.perf_counter_ns()

  bookings = list(Booking.objects.order_by('pk')[:LIMIT])

  end = time.perf_counter_ns()

  if len(bookings) != LIMIT:
    raise AssertionError(f'Expected {LIMIT} rows, got {len(bookings)}')

  return end - start


def main() -> None:
  elapsed_results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      elapsed_ns = select_iteration()
      elapsed_results.append(elapsed_ns)
  except Exception as e:
    print(f'[ERROR] Test 4 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)

  print(
    f'Test 4. Retrieval of 1,000 rows as model instances\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
