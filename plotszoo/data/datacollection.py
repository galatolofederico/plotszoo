import pandas as pd

class DataCollection:
    def __init__(self):
        self.data_types = []

    def create_scalar_from_series(self, scalar_name, agg_fn):
        assert self.is_both(), "To create a scalar from series the DataCollection must have both scalars and series"
        newscalars = []
        for index, scalars in self.scalars.iterrows():
            series = self.series[index]
            newscalars.append(agg_fn(series))

        self.scalars[scalar_name] = newscalars

    def dropna(self, columns):
        assert self.is_scalars(), "You must have scalars to drop"
        null_indices = self.scalars.index[pd.isnull(self.scalars[columns]).any(1)].tolist()
        
        self.scalars = self.scalars.drop(null_indices)
        if self.is_series():
            for null_index in null_indices:
                del self.series[null_index]

    def is_scalars(self):
        return "scalars" in self.data_types
    
    def is_series(self):
        return "series" in self.data_types
    
    def is_both(self):
        return self.is_scalars() and self.is_series()
