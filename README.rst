Introduction
============


.. image:: https://readthedocs.org/projects/lis3dh/badge/?version=latest
    :target: https://lis3dh.readthedocs.io/
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/micropython-lis3dh.svg
    :alt: latest version on PyPI
    :target: https://pypi.python.org/pypi/micropython-lis3dh

.. image:: https://static.pepy.tech/personalized-badge/micropython-lis3dh?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Pypi%20Downloads
    :alt: Total PyPI downloads
    :target: https://pepy.tech/project/micropython-lis3dh


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

LIS3DH MicroPython Driver. Work is based in:
    * https://github.com/adafruit/Adafruit_CircuitPython_LIS3DH/
    * https://github.com/adafruit/Adafruit_CircuitPython_Register

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
