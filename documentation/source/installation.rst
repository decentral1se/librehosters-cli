************
Installation
************

``librehosters-cli`` is only available from `test.pypi.org`_ right now.

.. _test.pypi.org: https://test.pypi.org/

.. code-block:: bash

    $ pip install \
      --index-url https://test.pypi.org/simple \
      --extra-index-url https://pypi.org/simple \
      librehosters-cli

.. warning::

    This tool is only supported on Python >= 3.5.

.. warning::

    It is highly recommended to use a `virtual environment`_ when installing
    Python packages. You should also consider upgrading your `setuptools`_
    installation with ``pip install -U setuptools``.

    .. _virtual environment: https://docs.python.org/3/tutorial/venv.html
    .. _setuptools: http://setuptools.readthedocs.io/
