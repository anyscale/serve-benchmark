from ray import serve
import os
import ray

ray.init(address="auto", namespace="serve")
num_replicas = os.environ.get("NUM_REPLICAS", "1")
serve.get_deployment("rl").options(num_replicas=int(num_replicas)).deploy()
