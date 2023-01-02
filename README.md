Inels-mqtt
========
A Python library that handles communication with inels over mqtt
[iNels](https://www.inels.com/) by ElkoEP company.

Requirements
============
For smooth using you need to have Python 3.9 or higher.

Install
=======
Use PyPI repository
```
pip install inels-mqtt-dev
```

Testing
=======
I use [tox](https://tox.readthedocs.io) for testing.

```
$ pip install tox

```

Development status
==================

Supported bus devices
    - SA3-01B (100)
    - DA3-22M (101)
    - GRT3-50 (102)
    - GSB3-90Sx (103)
    - SA3-04M (106)
    - SA3-012M (108)
    - WSB3-20H (124)
    - GSB3-60S (139)
    - IDRT3-1 (160)

Bus devices in development
    - IM3-80B (117)
    - IM3-140M (121)
    - Virtual controller (166)
    - Virtual heat regulator (167)
    - Virtual cool regulator (168)
