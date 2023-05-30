# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

import flux_metrics_api.defaults as defaults


def new_identifier(name: str, selector: dict = None):
    """
    Get a new metric identifier.
    """
    metric = {"name": name}
    if selector is not None:
        metric["selector"] = selector
    return metric


def new_metric(metric, value, time="", windowSeconds=0):
    """
    Get the metric value for an object.

    The metric should be the data structure above, and it's corresponding value (value).
    The time is an optional timestamp with the metric, windowSeconds is the window over
    which the metric was calculated (0 for instantaneous, which is what we are making).
    describedObject is the object the metric was collected from.
    """
    # Our custom metrics API always comes from a service
    describedObject = {
        "kind": "Service",
        "namespace": defaults.NAMESPACE,
        "name": defaults.SERVICE_NAME,
        "apiVersion": defaults.API_VERSION(),
    }
    return {
        "metricName": metric,
        "value": value,
        "timestamp": time,
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
