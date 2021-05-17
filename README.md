## Serve Scalability Benchmark for RLlib Models

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
