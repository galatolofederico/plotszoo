import wandb
import pandas as pd
import hashlib
import json
import os
api = wandb.Api()

from plotszoo.data import DataCollection

class WandbData(DataCollection):
    def __init__(self, username, project, query, cache=True, cache_dir="./.plotszoo-wandb-cache", force_update=False):
        super(WandbData, self).__init__()
        try:
            self.query = json.dumps(query)
        except:
            raise Exception("The query '%s' must be a valid JSON" % (query))
        
        self.username = username
        self.project = project
        self.cache = cache
        self.cache_dir = cache_dir
        self.force_update = force_update

        self.id = hashlib.sha256(("%s/%s/%s" % (self.username, self.project, self.query)).encode()).hexdigest()
        self.cache_file = os.path.join(self.cache_dir, self.id+".json")
        
    def pull_scalars(self, state="finished"):
        assert len(self.data_types) == 0, "You can pull the data once for each data object"

        self.runs = None
        if self.cache and os.path.exists(self.cache_file) and not self.force_update:
            print("[!] Using cache file %s" % (self.cache_file, ))
            self.runs = json.load(open(self.cache_file, "r"))
        else:
            print("[!] Pulling data from wandb")
            wandb_runs = api.runs("%s/%s" % (self.username, self.project), json.loads(self.query))
            self.runs = []
            for wandb_run in wandb_runs:
                if state is None or wandb_run.state == state:
                    runs.append(dict(
                        id=wandb_run.id,
                        name=wandb_run.name,
                        config=dict(wandb_run.config),
                        summary=wandb_run.summary._json_dict
                    ))

            if self.cache:
                if not os.path.isdir(self.cache_dir): os.mkdir(self.cache_dir)
                if not os.path.isfile(self.cache_file) or self.force_update:
                    print("[!] Saving cache file %s" % (self.cache_file, ))
                    json.dump(self.runs, open(self.cache_file, "w"))

        one_level_runs = []
        internal_keys = ["config", "summary"]
        keep_keys = ["id", "name"]
        for run in self.runs:
            one_level_run = dict()
            for internal_key in internal_keys:
                for key, value in run[internal_key].items():
                    one_level_run["%s/%s" % (internal_key, key)] = value
            for keep_key in keep_keys:
                one_level_run[keep_key] = run[keep_key]
            one_level_runs.append(one_level_run)

        self.data_types.append("scalars")
        self.scalars = pd.DataFrame(one_level_runs)


    def pull_series(self):
        assert len(self.data_types) == 1 and self.data_types[0] == "scalars", "You have to pull_scalars() before pulling the series"

        self.series = {}
        for index, run in self.scalars.iterrows():
            cache_file = os.path.join(self.cache_dir, run["id"]+".csv")
            series_df = None
            if self.cache and os.path.exists(cache_file) and not self.force_update:
                print("[!] Using cache file %s" % (cache_file, ))
                series_df = pd.read_csv(cache_file)
            else:
                print("[!] Pulling data from wandb for run_id=%s" % (run["id"], ))
                wandb_run = api.run("%s/%s/%s" % (self.username, self.project, run["id"]))
                series_df = wandb_run.history()
                if self.cache:
                    print("[!] Writing cache file %s" % (cache_file, ))
                    series_df.to_csv(cache_file)
            self.series[index] = series_df
        
        self.data_types.append("series")