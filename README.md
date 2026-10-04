Django ORM read performance bench ![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/Python-3.14-blue) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue)
==============

A reproducible benchmark of Django ORM read operations on PostgreSQL.

The database schema is based on the demonstration schema provided by
Postgres Professional: https://postgrespro.ru/education/demodb.
Each run is initialized from a trimmed three-month dump derived from
`demo-20250901-3m.sql.gz` (original dump available at
https://edu.postgrespro.ru/demo-20250901-3m.sql.gz). The trimmed dump contains
only two tables, **Bookings** and **Tickets**, and is restored immediately
before testing. After restoration, `VACUUM (ANALYZE)` is run for both tables
to refresh planner statistics and the visibility map, so every run starts from
the same database state.

For convenience, the trimmed dump is built into the database image published
on Docker Hub: https://hub.docker.com/r/denistred/sql-orm-bench-db.

---
### Server specifications

**Minimum:**
- 2 × 3.3 GHz CPUs
- 4 GB RAM

**Recommended:**
- 2 × 3.5 GHz CPUs
- 8 GB RAM

---

### Running

Create a `.env` file in the project root with the required values
(`POSTGRES_*`, `SELECT_REPEATS`, `LIMIT`), then run the ready-made script:

```bash
# from repo root
# run ten benchmark cycles
./runner.sh 10
```

Each cycle starts from a fresh runtime copy of the golden database. After the
cycle, its containers, networks and runtime volumes are removed. All tests are
read-only, so the data is identical for every cycle.

Each test is repeated `SELECT_REPEATS` times (default 25) and prints the median
wall-clock time of the ORM call as `elapsed_ns`. The output is shown in the
terminal and saved to `logs.txt` next to `runner.sh`. The file is cleared
before the first cycle, and every cycle is marked with an `iteration <k>` line.

**IMPORTANT NOTE:** Run only the ready-made `runner.sh`. It checks that the
golden volume exists (and restores the dump into it if necessary), recreates the
runtime volume for every cycle and passes the required arguments to Docker
Compose.

---

### Tests

1. Single-row retrieval as a model instance
2. Single-row retrieval as a key-value dictionary
3. Single-row retrieval as a tuple of field values
4. Retrieval of `LIMIT` rows as model instances
5. Retrieval of `LIMIT` rows as key-value dictionaries
6. Retrieval of `LIMIT` rows as tuples of field values

Tests 1-3 use `.first()` on the plain, `values()` and `values_list()`
querysets. Tests 4-6 use `order_by('pk')[:LIMIT]` (default `LIMIT=1000`) and
evaluate the queryset with `list()`, so the query is executed inside the
measured interval.

---

- Stack: Python 3.14, PostgreSQL 18, Django 5.2.8, Psycopg 3.3.2.
- Authors: student research team.
- License: MIT.