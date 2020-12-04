import pandas as pd
import os
import hashlib

from plotszoo.data import DataCollection

class OptunaData(DataCollection):
    r"""
    Retrive scalars and time series from an `optuna <https://optuna.org/>`_. storage

    Args:
        :storage: ``optuna`` storage (example: ``sqlite:///example.db``)
        :study_name: ``optuna`` study name
        :cache: Cache retrived data (Default: ``True``)
        :cache_dir: Directory to cache the data to (Default: ``./.plotszoo-optuna-cache``)
        :verbose: Be verbose about pulling and caching (Default: ``True``)
    """
    def __init__(self, storage, study_name, cache=True, cache_dir="./.plotszoo-optuna-cache", verbose=True):
        try:
            import optuna
        except:
            raise Exception("You must install 'optuna' to use this class")
        
        super(OptunaData, self).__init__()
        
        self.storage = storage
        self.study_name = study_name
        self.cache = cache
        self.cache_dir = cache_dir
        self.verbose = verbose

        self.id = hashlib.sha256(("%s_%s" % (self.storage, self.study_name)).encode()).hexdigest()
        self.cache_file = os.path.join(self.cache_dir, self.id+".csv")
    
    def pull_scalars(self, force_update=False):
        r"""
        Pull scalars from the ``optuna`` storage

        Args:
            :force_update: Force cache update (Default: ``False``)
        """
        import optuna
        if self.cache and os.path.exists(self.cache_file) and not force_update:
            if self.verbose: print("[!] Using cache file %s" % (self.cache_file, ))
            self.scalars = pd.read_csv(self.cache_file)
        else:
            study = optuna.load_study(study_name=self.study_name, storage=self.storage)
            self.scalars = study.trials_dataframe()
            if self.cache:
                if not os.path.isdir(self.cache_dir): os.mkdir(self.cache_dir)
                if not os.path.isfile(self.cache_file) or force_update:
                    if self.verbose: print("[!] Saving cache file %s" % (self.cache_file, ))
                    self.scalars.to_csv(self.cache_file)


    def pull_series(self):
        raise Exception("Optuna does not store series")