import os

from flask import Flask
import numpy as np

import ray
from gym.spaces import Box, Discrete
from ray import serve
from ray.rllib.agents.marwil import MARWILTrainer
from ray.rllib.examples.env.random_env import RandomEnv


app = Flask(__name__)

def restore_trainer(checkpoint_path):
    env_config = {
        "action_space": Discrete(12),
        "observation_space": Box(-1000.0, 1000.0, (47,), np.float32),
    }
    config = {"explore": False, "env_config": env_config}
    _trainer = MARWILTrainer(config=config, env=RandomEnv)
    _trainer.restore(checkpoint_path)
    return _trainer



ray.init()
agent = restore_trainer("./checkpoint")

@app.route("/")
def compute_action():
    arr = [1 for _ in range(47)]
    actions = agent.compute_action(arr).astype(float).tolist()
    return {"result": actions}

