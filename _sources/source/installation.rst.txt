Installation
============

To install from pip (which may be out of date):

.. code:: bash

   pip install jubeo[all]

There are some optional features you can install as well using the
"extras" spec in pip. Currently, these are:

all
   installs all extras

Check the setup.py file under ``extras_requirements`` for the full
listing.

You can always install from git as well for the latest:

.. code:: bash

   pip install git+https://github.com/salotz/jubeo

If installation went alright this command should succeed:

.. code:: bash

   python -c "import jubeo"
