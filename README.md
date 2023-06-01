# Flux Metrics API

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![PyPI](https://img.shields.io/pypi/v/flux-metrics-api)](https://pypi.org/project/flux-metrics-api/)

This is an experiment to create a metrics API for Kubernetes that can be run directly from the Flux
leader broker pod. We made this after creating [prometheus-flux](https://github.com/converged-computing/prometheus-flux)
and wanting a more minimalist design. I'm not even sure it will work, but it's worth a try!

## Usage

### Install

You can install from pypi or from source:

```bash
$ python -m venv env
$ source env/bin/activate
$ pip install flux-metrics-api

# or

$ git clone https://github.com/converged-computing/flux-metrics-api
$ cd flux-metrics-api
$ pip install .
# you can also do "pip install -e ."
```

This will install the executable to your path, which might be your local user bin:

```bash
$ which flux-metric-api
/home/vscode/.local/bin/flux-metrics-api
```

Note that the provided [.devcontainer](.devcontainer) includes an environment for VSCode where you have Flux
and can install this and use ready to go!

### Start

You'll want to be running in a Flux instance, as we need to connect to the broker handle.

```bash
$ flux start --test-size=4
```

And then start the server. This will use a default port and host (0.0.0.0:8443) that you can customize
if desired.

```bash
$ flux-metrics-api start

# customize the port or host
$ flux-metrics-api start --port 9000 --host 127.0.0.1
```

#### SSL

If you want ssl (port 443) you can provide the path to a certificate and keyfile:

```bash
$ flux-metrics-api start --ssl-certfile /etc/certs/tls.crt --ssl-keyfile /etc/certs/tls.key
```

An example of a full command we might run from within a pod:

```bash
$ flux-metrics-api start --port 8443 --ssl-certfile /etc/certs/tls.crt --ssl-keyfile /etc/certs/tls.key --namespace flux-operator --service-name custom-metrics-apiserver
```

#### On the fly custom metrics!

If you want to provide custom metrics, you can write a function in an external file that we will read it and add to the server.
As a general rule:

 - The name of the function will be the name of the custom metric
 - You can expect the only argument to be the flux handle
 - You'll need to do imports within your function to get them in scope

This likely can be improved upon, but is a start for now! We provide an [example file](example/custom-metrics.py). As an example:

```bash
$ flux-metrics-api start --custom-metric ./example/custom-metrics.py
```

And then test it:

```bash
$ curl -s http://localhost:8443/apis/custom.metrics.k8s.io/v1beta2/namespaces/flux-operator/metrics/my_custom_metric_name | jq
```
```console
{
  "items": [
    {
      "metric": {
        "name": "my_custom_metric_name"
      },
      "value": 4,
      "timestamp": "2023-06-01T01:39:08+00:00",
      "windowSeconds": 0,
      "describedObject": {
        "kind": "Service",
        "namespace": "flux-operator",
        "name": "custom-metrics-apiserver",
        "apiVersion": "v1beta2"
      }
    }
  ],
  "apiVersion": "custom.metrics.k8s.io/v1beta2",
  "kind": "MetricValueList",
  "metadata": {
    "selfLink": "/apis/custom.metrics.k8s.io/v1beta2"
  }
}
```

See `--help` to see other options available.

### Endpoints

#### Metric

**GET /apis/custom.metrics.k8s.io/v1beta2/namespaces/<namespace>/metrics/<metric_name>**

Here is an example to get the "node_up_count" metric:

```bash
 curl -s http://localhost:8443/apis/custom.metrics.k8s.io/v1beta2/namespaces/flux-operator/metrics/node_up_count | jq
```
```console
{
  "items": [
    {
      "metric": {
        "name": "node_up_count"
      },
      "value": 2,
      "timestamp": "2023-05-31T04:44:57+00:00",
      "windowSeconds": 0,
      "describedObject": {
        "kind": "Service",
        "namespace": "flux-operator",
        "name": "custom-metrics-apiserver",
        "apiVersion": "v1beta2"
      }
    }
  ],
  "apiVersion": "custom.metrics.k8s.io/v1beta2",
  "kind": "MetricValueList",
  "metadata": {
    "selfLink": "/apis/custom.metrics.k8s.io/v1beta2"
  }
}
```

The following metrics are supported:

 - **node_up_count**: number of nodes up in the MiniCluster
 - **node_free_count**: number of nodes free in the MiniCluster
 - **node_cores_free_count**: number of node cores free in the MiniCluster
 - **node_cores_up_count**: number of node cores up in the MiniCluster
 - **job_queue_state_new_count**: number of new jobs in the queue
 - **job_queue_state_depend_count**: number of jobs in the queue in state "depend"
 - **job_queue_state_priority_count**: number of jobs in the queue in state "priority"
 - **job_queue_state_sched_count**: number of jobs in the queue in state "sched"
 - **job_queue_state_run_count**: number of jobs in the queue in state "run"
 - **job_queue_state_cleanup_count**: number of jobs in the queue in state "cleanup"
 - **job_queue_state_inactive_count**: number of jobs in the queue in state "inactive"


### Docker

We have a docker container, which you can customize for your use case, but it's more intended to
be a demo. You can either build it yourself, or use our build.

```bash
$ docker build -t flux_metrics_api .
$ docker run -it -p 8443:8443 flux_metrics_api
```
or

```bash
$ docker run -it -p 8443:8443 ghcr.io/converged-computing/flux-metrics-api
```

### Development

Note that this is implemented in Python, but (I found this after) we could [also use Go](https://github.com/kubernetes-sigs/custom-metrics-apiserver).
Specifically, I found this repository useful to see the [spec format](https://github.com/kubernetes-sigs/custom-metrics-apiserver/blob/master/pkg/generated/openapi/custommetrics/zz_generated.openapi.go).

You can then open up the browser at [http://localhost:8443/metrics/](http://localhost:8443/metrics) to see
the metrics!

## 😁️ Contributors 😁️

We use the [all-contributors](https://github.com/all-contributors/all-contributors)
tool to generate a contributors graphic below.

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://vsoch.github.io"><img src="https://avatars.githubusercontent.com/u/814322?v=4?s=100" width="100px;" alt="Vanessasaurus"/><br /><sub><b>Vanessasaurus</b></sub></a><br /><a href="https://github.com/converged-computing/flux-metrics-api/commits?author=vsoch" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

HPCIC DevTools is distributed under the terms of the MIT license.
All new contributions must be made under this license.

See [LICENSE](https://github.com/converged-computing/flux-metrics-api/blob/main/LICENSE),
[COPYRIGHT](https://github.com/converged-computing/flux-metrics-api/blob/main/COPYRIGHT), and
[NOTICE](https://github.com/converged-computing/flux-metrics-api/blob/main/NOTICE) for details.

SPDX-License-Identifier: (MIT)

LLNL-CODE- 842614
