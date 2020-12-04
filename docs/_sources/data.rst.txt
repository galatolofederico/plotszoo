Data loading
============

In ``plotszoo`` data is organized in a :class:`plotszoo.data.DataCollection`.

:class:`plotszoo.data.DataCollection` collect two data types:
    
* ``scalars``: organized in a pandas :class:`DataFrame`
* ``series``: organized in a python :class:`dict` having as keys the indices of the ``scalars`` and as values time series :class:`DataFrame`

Classes to pull data from common services are also provided such as :class:`plotszoo.data.WandbData`

.. autoclass:: plotszoo.data.DataCollection
    :members:
.. autoclass:: plotszoo.data.WandbData
    :members:
.. autoclass:: plotszoo.data.OptunaData
    :members: