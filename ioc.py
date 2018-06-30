from django.conf import settings
from django.core import exceptions
from django.db import models, connections


LOOKUP_SEP = '__'


class IOCManager(models.Manager):
    """
    Django ORM manager for Postgresql
    Came from Rock@luojilab
    """

    def create_or_update(self, conflict, defaults=None, **kwargs):
        """
        Replace update_or_create
        Without transaction, when using update_or_create may raise IntegrityError
        Because thread 1 execute update affect 0 row
        and at the same time, thread 2 insert it
        then thread 1 do insert will trigger UniqueKey conflict.

        This method will use INSERT ON CONFLICT feature to fix this.

        :param conflict:
        :param defaults:
        :param kwargs:
        :return:
        """
        postgres_engines = ("postgis", "postgresql", "django_postgrespool")
        engine = settings.DATABASES[self.db]["ENGINE"].split(".")[-1]
        is_postgres = engine.startswith(postgres_engines)

        if not is_postgres:
            # if not postgres, return update_or_create using Django origin
            return super(IOCManager, self).update_or_create(defaults, **kwargs)

        defaults = defaults or {}
        lookup, params = self._extract_model_params(defaults, **kwargs)
        params = {k: v() if callable(v) else v for k, v in params.items()}
        
        field_names = ",".join(params.keys())
        field_values = []
        field_updates = []
        for k, v in params.items():
            field_values.append("%%(%s)s" % k)
            field_updates.append("%s = %%(%s)s" % (k, k))

        sql = "INSERT INTO %s(%s) VALUES(%s) ON CONFLICT (%s) DO " \
              "UPDATE SET %s RETURNING id" % \
              (
                  self.model._meta.db_table,
                  field_names,
                  ",".join(field_values),
                  conflict,
                  ",".join(field_updates),
              )
        cursor = connections[self.db].cursor()
        return cursor.execute(sql, params=params)

    def _extract_model_params(self, defaults, **kwargs):
        """
        Prepares `lookup` (kwargs that are valid model attributes), `params`
        (for creating a model instance) based on given kwargs; for use by
        get_or_create and update_or_create.
        """
        defaults = defaults or {}
        lookup = kwargs.copy()
        for f in self.model._meta.fields:
            if f.attname in lookup:
                lookup[f.name] = lookup.pop(f.attname)
        params = {k: v for k, v in kwargs.items() if LOOKUP_SEP not in k}
        params.update(defaults)
        property_names = self.model._meta._property_names
        invalid_params = []
        for param in params:
            try:
                self.model._meta.get_field(param)
            except exceptions.FieldDoesNotExist:
                # It's okay to use a model's property if it has a setter.
                if not (param in property_names and getattr(self.model, param).fset):
                    invalid_params.append(param)
        if invalid_params:
            raise exceptions.FieldError(
                "Invalid field name(s) for model %s: '%s'." % (
                    self.model._meta.object_name,
                    "', '".join(sorted(invalid_params)),
                ))
        return lookup, params
