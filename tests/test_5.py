import os
import statistics
import sys
import time

import django
django.setup()

from core.models import Booking

from django.db import connection
connection.ensure_connection()

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))
LIMIT = int(os.environ.get('LIMIT', '2500'))


def select_iteration() -> int:
  start = time.perf_counter_ns()

  rows = list(Booking.objects.order_by('pk').values()[:LIMIT])

  end = time.perf_counter_ns()

  if len(rows) != LIMIT or not isinstance(rows[0], dict):
    raise AssertionError('Expected a list of dicts of length LIMIT')

  return end - start


def main() -> None:
  elapsed_results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      elapsed_ns = select_iteration()
      elapsed_results.append(elapsed_ns)
  except Exception as e:
    print(f'[ERROR] Test 5 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)

  print(
    f'Test 5. Retrieval of 2,500 rows as key-value dictionaries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
