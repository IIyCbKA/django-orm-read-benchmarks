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


def select_iteration() -> int:
  start = time.perf_counter_ns()

  booking = Booking.objects.values().first()

  end = time.perf_counter_ns()

  if not isinstance(booking, dict):
    raise AssertionError(f'Expected dict, got {type(booking).__name__}')

  return end - start


def main() -> None:
  elapsed_results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      elapsed_ns = select_iteration()
      elapsed_results.append(elapsed_ns)
  except Exception as e:
    print(f'[ERROR] Test 2 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)

  print(
    f'Test 2. Single-row retrieval as a key-value dictionary\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
