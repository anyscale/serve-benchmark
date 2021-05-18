## Serve Scalability Benchmark for RLlib Models

### Microbenchmark for batching

Run `batch_size_benchmark.py`. `linear_scaling_us` is the hypothetical number for `single_query_latency * batch_size`.

| batch_size | latency_us |     std | linear_scaling_us |
| ---------: | ---------: | ------: | ----------------: |
|          1 |    537.452 | 5.75518 |           537.452 |
|          2 |    556.276 | 4.80701 |            1074.9 |
|          4 |    600.416 | 2.89832 |           2149.81 |
|          8 |     664.37 | 7.94813 |           4299.62 |
|         16 |    781.605 | 3.67411 |           8599.23 |
|         32 |    1108.92 | 10.6627 |           17198.5 |
|         64 |    1536.36 | 3.94714 |           34396.9 |
|         96 |    1931.03 | 8.81434 |           51595.4 |
|        128 |    2290.48 | 7.23508 |           68793.9 |

### Scalability Benchmark

- Use `app_config.json` to configure the runtime environment. Note that we use `wrk` for HTTP benchmark.
- Use `compute_config.json` to configure nodes. Make sure to change the cloud id.
- Use `app.py` to deploy initial app.
- Use `NUM_REPLICAS=<int> python scale.py` to dynamically scale the deployment.
- Use `benchmark_client.py` to benchmark each http proxy to see the individual and aggregated throughput.
- For deployment scenario, you will need to add a load balancer in front. See `register_elb.sh` for the shell command to register all instances within an anyscale session to load balancer. You can also use the `benchmark_client.py`, but make sure to point it to the load balancer address.

### Latency Benchmark

- Ray Serve deployment at `app.py`: `ray start --head; python app.py`
  - Use `wrk --latency localhost:8000/predict/` to benchmark
- Flask deployment at `flask_app.py`: `FLASK_APP=flask_app:app flask run`
  - Use `wrk --latency localhost:5000/predict/` to benchmark
