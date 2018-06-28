from setuptools import setup


setup(
    name = "django-postgres-ioc",
    version = "0.0.1",
    author = "mrgaolei",
    author_email = "gaolei@luojilab.com",
    description = ("A Django model manager providing insert on conflict "
                   "for PostgreSQL database tables."),
    long_description = open("README.rst").read(),
    url = "http://github.com/luojilab/django-postgres-ioc",
    zip_safe = False,
    py_modules=["ioc",],
    install_requires = [
        "django >= 1.7",
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ]
)
