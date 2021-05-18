import ray

ray.init()

# get keys to assign to each worker nodes
keys = []
for n in ray.nodes():
    keys.extend(n["Resources"])
keys = set(k for k in keys if k.startswith("node"))
print(len(keys))


@ray.remote
def bench():
    import subprocess, shlex

    # NOTE: replca the url with elb if benchmarking via load balancer.
    return subprocess.check_output(
        shlex.split("wrk -c 50 -t 2 http://localhost:8000/predict/")
    )


outs = [bench.options(resources={k: 0.01}, num_cpus=0).remote() for k in keys]
results = ray.get(outs)


def parse(text):
    return float(text.decode().split("\n")[-3].split()[-1])


print([parse(r) for r in results])
print(sum([parse(r) for r in results]))