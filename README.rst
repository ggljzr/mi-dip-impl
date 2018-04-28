mi-dip-impl
===========

Implementation part of my `thesis <https://github.com/ggljzr/mi-dip>`__ (in Czech).

Installation
============

Requires Python 3. Other packages are collected via pip. For sending SMS notifications, you'll need to install and configure `Gammu SMSD <https://wammu.eu/smsd/>`__.

Create virtual environment (optional):

::
    
    $ python3 -m venv env
    $ . env/bin/activate

Install package:

::

    $ (env) python setup.py install

Running
=======

::

    $ (env) garage_system
    # or
    $ (env) python run.py

Note that this will run embedded Flask server in debug mode, which is suitable for debug/developement purposes only. For deployment (on Raspberry Pi) see deployment `readme <https://github.com/ggljzr/mi-dip-impl/tree/master/deployment>`__.

Tests
=====

You can run tests with:

::
    
    $ (env) python setup.py test

This should collect `pytest <https://docs.pytest.org/en/latest/contents.html>`__ framework used for testing. Or if you already have pytest:

::

    $ (env) python -m pytest tests