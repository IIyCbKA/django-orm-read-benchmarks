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

  booking = Booking.objects.first()

  end = time.perf_counter_ns()

  if booking is None:
    raise AssertionError('Expected booking, got None')

  return end - start


def main() -> None:
  elapsed_results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      elapsed_ns = select_iteration()
      elapsed_results.append(elapsed_ns)
  except Exception as e:
    print(f'[ERROR] Test 1 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)

  print(
    f'Test 1. Single-row retrieval as a model instance\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
