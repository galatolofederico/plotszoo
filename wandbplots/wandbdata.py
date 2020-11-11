import wandb
import pandas as pd
import hashlib
import json
import os
api = wandb.Api()


class WandbData:
    def __init__(self, username, project, query, cache=True, cache_dir="./wandb-plots.cache", force_update=False):
        try:
            self.query = json.dumps(query)
        except:
            raise Exception("The query '%s' must be a valid JSON" % (query))
        
        self.id = hashlib.sha256(("%s/%s/%s" % (username, project, self.query)).encode()).hexdigest()
        self.cache_file = os.path.join(cache_dir, self.id+".json")
        runs = None

        if cache and os.path.exists(self.cache_file) and not force_update:
            print("[!] Using cache file %s" % (self.cache_file, ))
            runs = json.load(open(self.cache_file, "r"))
        else:
            print("[!] Pulling data from wandb")
            wandb_runs = api.runs("%s/%s" % (username, project), json.loads(self.query))
            runs = []
            for wandb_run in wandb_runs: 
                runs.append(dict(
                    id=wandb_run.id,
                    name=wandb_run.name,
                    config=dict(wandb_run.config),
                    summary=wandb_run.summary._json_dict
                ))

            if cache:
                if not os.path.isdir(cache_dir): os.mkdir(cache_dir)
                if not os.path.isfile(self.cache_file) or force_update:
                    print("[!] Saving cache file %s" % (self.cache_file, ))
                    json.dump(runs, open(self.cache_file, "w"))

        one_level_runs = []
        internal_keys = ["config", "summary"]
        keep_keys = ["id", "name"]
        for run in runs:
            one_level_run = dict()
            for internal_key in internal_keys:
                for key, value in run[internal_key].items():
                    one_level_run["%s/%s" % (internal_key, key)] = value
            for keep_key in keep_keys:
                one_level_run[keep_key] = run[keep_key]
            one_level_runs.append(one_level_run)

        self.runs = pd.DataFrame(one_level_runs)

