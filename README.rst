Introduction
============

Django ORM manager for Postgresql
Came from Rock@luojilab

Replace ``update_or_create``
Without transaction, when using ``update_or_create`` may raise ``IntegrityError``
Because thread 1 execute update affect 0 row
and at the same time, thread 2 insert it
then thread 1 do insert will trigger UniqueKey conflict.

This method will use ``INSERT ON CONFLICT`` feature to fix this.

Requirements
============

  * Python >= 2.6
  * Django >= 1.7
  * PostgreSQL >= 9.2

Installation
============

Running following command::

  $ python setup.py install

Or using pip::

  $ pip install -U django-postgres-ioc

Usage
=====

Python code::

    from django.db import models
    from ioc import IOCManager

    class Test(models.Model):
        code = models.CharField(max_length=50, unique=True))
        name = models.CharField(max_length=100

        objects = IOCManager()

    Test.objects.create_or_update(
        conflict="code",
        code="luojilab",
        defaults={
            "name": "LuojiLab",
        },
    )
