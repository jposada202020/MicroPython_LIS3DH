⛔️ DEPRECATED
===============

This repository is no longer supported, please consider using alternatives.

.. image:: http://unmaintained.tech/badge.svg
  :target: http://unmaintained.tech
  :alt: No Maintenance Intended
LIS3DH MicroPython Driver. Work is based in:
    * https://github.com/adafruit/Adafruit_CircuitPython_LIS3DH/
    * https://github.com/adafruit/Adafruit_CircuitPython_Register


Installing with mip
====================

To install using mpremote

.. code-block:: shell

    mpremote mip install github:jposada202020/MicroPython_LIS3DH

To install directly using a WIFI capable board

.. code-block:: shell

    mip.install("github:jposada202020/MicroPython_LIS3DH")


Installing Library Examples
============================

If you want to install library examples:

.. code-block:: shell

    mpremote mip install github:jposada202020/MicroPython_LIS3DH/examples.json

To install directly using a WIFI capable board

.. code-block:: shell

    mip.install("github:jposada202020/MicroPython_LIS3DH/examples.json")



Installation
=============

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/micropython-lis3dh/>`_.
To install for current user:

.. code-block:: shell

    pip3 install micropython-lis3dh

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install micropython-lis3dh

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install micropython-lis3dh
