# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

from datetime import datetime

import flux_metrics_api.apis as apis
import flux_metrics_api.defaults as defaults
from flux_metrics_api.metrics import metrics


def new_group_list():
    """
    Return a faux group list to get the version of the custom metrics API
    """
    return apis.get_kubernetes_endpoint("apis")


def get_cluster_schema(version="v2"):
    """
    Get the API group list, assuming we are inside a pod.
    """
    return apis.get_kubernetes_endpoint(f"openapi/{version}")


def new_resource_list():
    """
    The root of the server returns the api list with available metrics.
    """
    listing = {
        "kind": "APIResourceList",
        "apiVersion": defaults.API_VERSION(),
        "groupVersion": defaults.API_ENDPOINT,
        "resources": [],
    }

    for metric_name in metrics:
        listing["resources"].append(
            {
                "name": metric_name,
                "singularName": metric_name,
                "namespaced": True,
                "kind": "MetricValueList",
                "verbs": ["get"],
            }
        )
    return listing


def new_identifier(name: str, selector: dict = None):
    """
    Get a new metric identifier.
    """
    metric = {"name": name}

    # A selector would be a label on a metric (we don't have any currently)
    if selector is not None:
        metric["selector"] = selector
    return metric


def new_metric(metric, value, timestamp="", windowSeconds=0):
    """
    Get the metric value for an object.

    The metric should be the data structure above, and it's corresponding value (value).
    The time is an optional timestamp with the metric, windowSeconds is the window over
    which the metric was calculated (0 for instantaneous, which is what we are making).
    describedObject is the object the metric was collected from.
    """
    # This probably needs work - I just fudged it for now
    timestamp = timestamp or datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")

    # Our custom metrics API always comes from a service
    describedObject = {
        "kind": "Service",
        "namespace": defaults.NAMESPACE,
        "name": defaults.SERVICE_NAME,
        "apiVersion": defaults.API_VERSION(),
    }
    return {
        "metric": metric,
        "value": value,
        "timestamp": timestamp,
        "windowSeconds": windowSeconds,
        "describedObject": describedObject,
    }


def new_metric_list(metrics, metadata=None):
    """
    Put list of metrics into proper list format
    """
    listing = {
        "items": metrics,
        "apiVersion": defaults.API_ENDPOINT,
        "kind": "MetricValueList",
    }
    if metadata is not None:
        listing["metadata"] = metadata
    return listing
