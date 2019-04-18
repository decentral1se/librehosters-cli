*************
Get Involved
*************

We use `tox`_ as the development interface. This means that as a contributor
you do not have to manage a virtual environment or dependencies. You can safely
run `pip install --user tox` as a standard `user package install`_ and then use
the following commands below to perform day-to-day development tasks.

An alternative installation method is provided below however.

.. _tox: http://tox.readthedocs.io/
.. _user package install: https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site

Run tests
---------

.. code-block:: bash

    tox -e test

Lint source
-----------

.. code-block:: bash

    tox -e lint

Format source
-------------

.. code-block:: bash

    tox -e format

Type check source
-----------------

.. code-block:: bash

    tox -e type

Development install
-------------------

The following command can be used to install the development package without
the use of Tox. This is not required for doing development work but is provided
for the convenience of those who wish to avoid using Tox for some personal
preference.

.. code-block:: bash

    $ pip install -e .'[test,lint,format,type,docs,pkg]'

.. warning::

    If you see an error message such as:

        No matching distribution found for black

    Then you should try passing the `--pre` option to `pip install`. The
    `black`_ formatting tool is still in the `beta development`_ phase.

    .. _black: https://black.readthedocs.io/en/stable/
    .. _beta development: https://github.com/ambv/black#note-this-is-a-beta-product

Add a new dependency
--------------------

You add to the `install_requires`_ entry in the `setup.cfg`_.

.. _install_requires: https://setuptools.readthedocs.io/en/latest/setuptools.html#options
.. _setup.cfg: ./setup.cfg

Release Process
---------------

.. code-block:: bash

    $ git tag x.x.x
    $ git push --tags

Test release
============

.. code-block:: bash

    $ tox -e metadata-release
    $ tox -e test-release

Validate that you can install the package:

.. code-block:: bash

    $ pip install -i https://test.pypi.org/simple/ librehosters-cli
    $ pip show librehosters-cli

Production release
==================

.. code-block:: bash

    $ tox -e metadata-release
    $ tox -e prod-release

Validate that you can install the package:

.. code-block:: bash

    $ pip install librehosters-cli
    $ pip show librehosters-cli
