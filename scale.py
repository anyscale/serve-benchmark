from ray import serve
import os

num_replicas = os.environ.get("NUM_REPLICAS", "1")
serve.get_deployment("rl").options(num_replicas=int(num_replicas)).deploy()