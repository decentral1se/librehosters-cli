*****
Usage
*****

Getting help
------------

``librehosters-cli`` is a good command line citizen:

.. code-block:: bash

    $ libreh --help

Schema management
-----------------

The latest standardised schema is hosted `here`_. 

View the latest standardised schema:

.. code-block:: bash

    $ libreh schema -S 

Validate a local schema with the latest standardised schema:

.. code-block:: bash

    $ libreh schema -s myschema.json

Validate a hosted schema with the latest standardised schema:

.. code-block:: bash

    $ libreh schema -lh nixnet 

Validate all network member schemas with the latest standardised schema:

.. code-block:: bash

    $ libreh schema --validate-all 

Validate a hosted schema via URL:

.. code-block:: bash

    $ libreh schema -u https://mycollective.org 

Assuming that a ``/librehost.json`` is exposed from this domain.

.. note::

    ``librehosters-cli schema`` ensures matching schema version and keys. Since
    there is not yet multiple versions of the standardised schema, only the
    latest is compaired. No functionality to compare different versions of the
    standardised schema is yet available.

.. _here: https://lab.libreho.st/librehosters/librehost-api/raw/master/librehost.json

Exploring the network
---------------------

The latest network registry is hosted `over here`_. 

List the current members of the network:

.. code-block:: bash

    $ libreh whois -S

List a member's schema information:

.. code-block:: bash

    $ libreh whois -lh weho.st

.. _over here: https://libreho.st/directory.json
