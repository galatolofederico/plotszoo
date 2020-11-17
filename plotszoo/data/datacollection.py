import pandas as pd

class DataCollection:
    r"""
    Base class for data collection

    Attributes:
        :scalars: :class:`DataFrame` cointaning the scalars
        :series: :class:`dict` cointaining the time series
    
    """
    def __init__(self):
        self.data_types = []

    def set_scalars(self, data):
        r"""
        Set the scalars

        Args:
            :data: The :class:`DataFrame` cointaning the scalars
        
        """
        assert not self.is_scalars(), "You can set_scalars() only once per DataCollection"
        assert not self.is_series(), "If you want to have both scalars and series you have to first set_scalars()"
        assert type(data) is pd.DataFrame, "The scalars must be in a DataFrame"
        
        self.scalars = data.copy()
        self.data_types.append("scalars")
    
    def set_series(self, series):
        r"""
        Set the series

        Args:
            :series: The :class`dict` cointaning the time series
        
        ``series`` must be set after ``scalars``

        the ``series`` :class:`dict` must have a key for each index of the ``scalars``
        """
        assert type(series) is dict, "Series must be passed as dict"
        if self.is_scalars():
            for index, row in self.scalars.iterrows():
                if not index in series:
                    raise Exception("Index %s not present in series but present in scalars" % (index, ))

        self.series = series.copy()
        self.data_types.append("series")

    def create_scalar_from_series(self, scalar_name, agg_fn):
        r"""
        Create a new column of scalars using the corresponding time series

        Args:
            :scalar_name: The name of the new scalar
            :agg_fn: Function to be called to the corresponding time series to create the scalar

        Example::

            >>> data.create_scalar_from_series("start_time", lambda s: s["timestamp"].min())

        """
        assert self.is_both(), "To create a scalar from series the DataCollection must have both scalars and series"
        newscalars = []
        for index, scalars in self.scalars.iterrows():
            series = self.series[index]
            newscalars.append(agg_fn(series))

        self.scalars[scalar_name] = newscalars

    def dropna(self, columns):
        r"""
        Discard ``NaN`` values from the scalars and also discard the corresponding time series

        Args:
            :columns: Columns to check for ``NaN``
        
        """
        assert self.is_scalars(), "You must have scalars to drop"
        null_indices = self.scalars.index[pd.isnull(self.scalars[columns]).any(1)].tolist()
        
        self.scalars = self.scalars.drop(null_indices)
        if self.is_series():
            for null_index in null_indices:
                del self.series[null_index]
    
    def align_series(self, to="longest", fill=float("NaN")):
        r"""
        Algin series to the longest or shortest one.

        Args:
            :to: alignment strategy (one of ``longest`` or ``shortest``) (Default: ``longest``)
            :fill: filling value to use (Default: ``NaN``)
        """
        assert not self.are_series_aligned(), "Series have to be unaligned"
        assert self.is_series(), "DataCollection must have series"
        assert to in ["longest", "shortest"], "to must be 'longest' or 'shortest'"

        new_index = None
        for key, series in self.series.items():
            if (
                new_index is None
                or (to == "longest" and len(series.index) > len(new_index))
                or (to == "shortest" and len(series.index) < len(new_index))
            ):
                new_index = series.index
        
        for key, series in self.series.items():
            self.series[key] = series.reindex(new_index, fill_value=fill)
        
        assert self.are_series_aligned()

    def are_series_aligned(self):
        r"""
        Returns ``True`` if all series share the same indices
        """
        assert self.is_series(), "You must have series to check for alignment"
        index = None
        for k, s in self.series.items():
            if index is None: index = s.index
            if len(s.index) != len(index) or not (s.index == index).all():
                return False
        return True


    def is_scalars(self):
        r"""
        Returns ``True`` if the :class:`DataCollection` contains scalars
        
        """
        return "scalars" in self.data_types
    
    def is_series(self):
        r"""
        Returns ``True`` if the :class:`DataCollection` contains time series
        
        """
        return "series" in self.data_types
    
    def is_both(self):
        r"""
        Returns ``True`` if the :class:`DataCollection` contains both scalars and time series
        
        """
        return self.is_scalars() and self.is_series()
    
    def is_empty(self):
        r"""
        Returns ``True`` if the :class:`DataCollection` is empty
        
        """
        return len(self.data_types) == 0
