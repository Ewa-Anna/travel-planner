When running backend if you get below error:

```
in check_consistent_history
    raise InconsistentMigrationHistory(
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency authx.0001_initial on database 'default'.
```

Read this post on stackoverflow: https://stackoverflow.com/questions/44651760/django-db-migrations-exceptions-inconsistentmigrationhistory