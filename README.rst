Django Filebrowser cleanup
===============================

This Django app makes it to cleanup unused file uploads which are uploaded by Filebrowser.
It scans all registered models in a project and determines where the FileBrowseField is used.
With that data available it queries all used data against the upload filesystem and deletes files which are no longer used.

.. warning::

    Use this package at your own risk.
    The app is based on the 3.0 version of the `No-Grapelli version of Django Filebrowser <https://github.com/wardi/django-filebrowser-no-grappelli>`_.
    I am not able to detect the exact version because the package doesn't have a appropriate version specification.
    

Installation
------------

* Add ``filebrowser_cleanup`` to your ``settings.INSTALLED_APPS``.


How-to
------------

* Run the following command: ``./manage.py filebrowser_cleanup``

Changelog
------------

v0.1 (development)
~~~~~~~~~~~~~~~~~~

* Initial release.