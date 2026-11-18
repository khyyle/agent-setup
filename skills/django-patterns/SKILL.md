---
name: django-patterns
description: Work on Django ORM queries, transactions, DRF endpoints and their database-backed tests.
metadata:
  origin: Adapted from the locally installed ECC Django patterns, security and TDD skills.
---

Start in the owning Django app. Trace the URL through its view, serializer, queryset and model. Change the layer that owns the contract.

- Scope object lookups and list querysets to the current caller where access depends on ownership. Test a second user through the real view. Serializer validation gives useful feedback, and a database constraint protects a rule that concurrent writers must also obey.
- Evaluate related data the view actually reads. Use `select_related` for a single-valued relation and `prefetch_related` for collections. For a query-count regression, exercise the endpoint with several related records and count queries around evaluation.
- Group dependent writes in `transaction.atomic()`. Schedule work that requires a committed row using `transaction.on_commit()`. Include retries or database uniqueness in the check where duplicate requests matter.
- Exercise a DRF route through the project's API test client. Assert the response and a fresh database read when persistence is part of the promise. In a test wrapped in a rollback transaction, capture and execute commit callbacks when their scheduling is the question. Use a transactional test when real commits, rollback or locks are the behavior under test.
