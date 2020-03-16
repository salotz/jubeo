Quick Start
===========

Install jubeo from the git repo:

.. code:: bash

   pip install git+https://github.com/salotz/jubeo.git

Because jubeo isn't really a library and doesn't have plugins it is
compatible with installing via ``pipx`` or similar tool:

.. code:: bash

   pipx install git+https://github.com/salotz/jubeo.git

You should be able to run the help message from the command line tool:

.. code:: bash

   jubeo --help

Then you can either manually create the config folder and file (at
``$XDG_CONFIG_HOME/jubeo``) for the command line tool or use the init
config CLI target:

.. code:: bash

   jubeo init-config

Then choose some project you want to install ``jubeo`` metaproject
tooling to e.g. ``$HOME/scratch/test_proj``:

.. code:: bash

   mkdir -p $HOME/scratch/test_proj
   jubeo init --force $HOME/scratch/test_proj
   cd $HOME/scratch/test_proj
   pip install -r .jubeo/requirements.txt
   inv -l
   inv custom.hello
   jubeo update .
