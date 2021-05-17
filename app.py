import os

import numpy as np
import ray
from gym.spaces import Box, Discrete
from ray import serve
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


@serve.deployment(route_prefix="/predict")
class Backend:
    def __init__(self, checkpoint_bytes, checkpoint_tune_meta_bytes):
        replica_tag = serve.get_replica_context().replica_tag

        # Cache the checkpoint file locally.
        checkpoint_path = f"checkpoint-{replica_tag}"
        checkpoint_tune_meta_path = f"checkpoint-{replica_tag}.tune_metadata"
        with open(checkpoint_path, "wb") as f:
            f.write(checkpoint_bytes)
        with open(checkpoint_tune_meta_path, "wb") as f:
            f.write(checkpoint_tune_meta_bytes)

        # Restore the trainer.
        self.agent = restore_trainer(checkpoint_path)

    def __call__(self, request):
        return {"status": "ok"}


if __name__ == "__main__":
    ray.init(address="auto")
    serve.start(
        detached=True, http_options={"host": "0.0.0.0", "location": "EveryNode"}
    )

    with open("./checkpoint", "rb") as f1, open(
        "./checkpoint.tune_metadata", "rb"
    ) as f2:
        Backend.deploy(f1.read(), f2.read())
