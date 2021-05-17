import os
import time
import json

os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np
import ray
from gym.spaces import Box, Discrete
from ray.rllib.agents.marwil import MARWILTrainer
from ray.rllib.examples.env.random_env import RandomEnv


def restore_trainer(checkpoint_path):
    env_config = {
        "action_space": Discrete(12),
        "observation_space": Box(-1000.0, 1000.0, (47,), np.float32),
    }
    config = {"explore": False, "env_config": env_config}
    _trainer = MARWILTrainer(config=config, env=RandomEnv)
    _trainer.restore(checkpoint_path)
    return _trainer


def timeit(func):
    arr = []
    for _ in range(7):
        start = time.time()
        [func() for _ in range(1000)]
        end = time.time()
        arr.append((end - start) * 1e6)
    arr = np.array(arr) / 1000
    return {"mean": np.mean(arr), "std": np.std(arr)}


if __name__ == "__main__":
    ray.init()
    trainer = restore_trainer("./checkpoint")
    bs = [1, 2, 4, 8, 16, 32, 64, 96, 128]
    timing = {}
    for i in bs:
        batch = {_: [1 for _ in range(47)] for _ in range(i)}
        result = timeit(lambda: trainer.compute_actions(batch))
        timing[i] = result
    print(json.dumps(timing, indent=2))
