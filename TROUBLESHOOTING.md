When running backend if you get below error:

```
in check_consistent_history
    raise InconsistentMigrationHistory(
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency authx.0001_initial on database 'default'.
```

Read this post on stackoverflow: https://stackoverflow.com/questions/44651760/django-db-migrations-exceptions-inconsistentmigrationhistory



```
The above exception (insert or update on table "django_admin_log" violates foreign key constraint "django_admin_log_user_id_c564eba6_fk_auth_user_id" DETAIL: Key (user_id)=(1) is not present in table "auth_user". ) was the direct cause of the following exception:
```

Read this post on stackoverflow: https://stackoverflow.com/questions/70274885/insert-or-update-on-table-django-admin-log-violates-foreign-key-constraint