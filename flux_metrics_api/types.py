# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

from datetime import datetime

import flux_metrics_api.defaults as defaults
from flux_metrics_api.metrics import metrics


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


def new_group_list():
    """
    Return a faux group list to get the version of the custom metrics API
    """
    return {
        "kind": "APIGroupList",
        "apiVersion": "v1",
        "groups": [
            {
                "name": "apiregistration.k8s.io",
                "versions": [
                    {"groupVersion": "apiregistration.k8s.io/v1", "version": "v1"}
                ],
                "preferredVersion": {
                    "groupVersion": "apiregistration.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "apps",
                "versions": [{"groupVersion": "apps/v1", "version": "v1"}],
                "preferredVersion": {"groupVersion": "apps/v1", "version": "v1"},
            },
            {
                "name": "events.k8s.io",
                "versions": [{"groupVersion": "events.k8s.io/v1", "version": "v1"}],
                "preferredVersion": {
                    "groupVersion": "events.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "authentication.k8s.io",
                "versions": [
                    {"groupVersion": "authentication.k8s.io/v1", "version": "v1"}
                ],
                "preferredVersion": {
                    "groupVersion": "authentication.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "authorization.k8s.io",
                "versions": [
                    {"groupVersion": "authorization.k8s.io/v1", "version": "v1"}
                ],
                "preferredVersion": {
                    "groupVersion": "authorization.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "autoscaling",
                "versions": [
                    {"groupVersion": "autoscaling/v2", "version": "v2"},
                    {"groupVersion": "autoscaling/v1", "version": "v1"},
                ],
                "preferredVersion": {"groupVersion": "autoscaling/v2", "version": "v2"},
            },
            {
                "name": "batch",
                "versions": [{"groupVersion": "batch/v1", "version": "v1"}],
                "preferredVersion": {"groupVersion": "batch/v1", "version": "v1"},
            },
            {
                "name": "certificates.k8s.io",
                "versions": [
                    {"groupVersion": "certificates.k8s.io/v1", "version": "v1"}
                ],
                "preferredVersion": {
                    "groupVersion": "certificates.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "networking.k8s.io",
                "versions": [{"groupVersion": "networking.k8s.io/v1", "version": "v1"}],
                "preferredVersion": {
                    "groupVersion": "networking.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "policy",
                "versions": [{"groupVersion": "policy/v1", "version": "v1"}],
                "preferredVersion": {"groupVersion": "policy/v1", "version": "v1"},
            },
            {
                "name": "rbac.authorization.k8s.io",
                "versions": [
                    {"groupVersion": "rbac.authorization.k8s.io/v1", "version": "v1"}
                ],
                "preferredVersion": {
                    "groupVersion": "rbac.authorization.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "storage.k8s.io",
                "versions": [{"groupVersion": "storage.k8s.io/v1", "version": "v1"}],
                "preferredVersion": {
                    "groupVersion": "storage.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "admissionregistration.k8s.io",
                "versions": [
                    {"groupVersion": "admissionregistration.k8s.io/v1", "version": "v1"}
                ],
                "preferredVersion": {
                    "groupVersion": "admissionregistration.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "apiextensions.k8s.io",
                "versions": [
                    {"groupVersion": "apiextensions.k8s.io/v1", "version": "v1"}
                ],
                "preferredVersion": {
                    "groupVersion": "apiextensions.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "scheduling.k8s.io",
                "versions": [{"groupVersion": "scheduling.k8s.io/v1", "version": "v1"}],
                "preferredVersion": {
                    "groupVersion": "scheduling.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "coordination.k8s.io",
                "versions": [
                    {"groupVersion": "coordination.k8s.io/v1", "version": "v1"}
                ],
                "preferredVersion": {
                    "groupVersion": "coordination.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "node.k8s.io",
                "versions": [{"groupVersion": "node.k8s.io/v1", "version": "v1"}],
                "preferredVersion": {"groupVersion": "node.k8s.io/v1", "version": "v1"},
            },
            {
                "name": "discovery.k8s.io",
                "versions": [{"groupVersion": "discovery.k8s.io/v1", "version": "v1"}],
                "preferredVersion": {
                    "groupVersion": "discovery.k8s.io/v1",
                    "version": "v1",
                },
            },
            {
                "name": "flowcontrol.apiserver.k8s.io",
                "versions": [
                    {
                        "groupVersion": "flowcontrol.apiserver.k8s.io/v1beta3",
                        "version": "v1beta3",
                    },
                    {
                        "groupVersion": "flowcontrol.apiserver.k8s.io/v1beta2",
                        "version": "v1beta2",
                    },
                ],
                "preferredVersion": {
                    "groupVersion": "flowcontrol.apiserver.k8s.io/v1beta3",
                    "version": "v1beta3",
                },
            },
            {
                "name": "flux-framework.org",
                "versions": [
                    {
                        "groupVersion": "flux-framework.org/v1alpha1",
                        "version": "v1alpha1",
                    }
                ],
                "preferredVersion": {
                    "groupVersion": "flux-framework.org/v1alpha1",
                    "version": "v1alpha1",
                },
            },
        ],
    }

    #
    return {
        "kind": "APIGroupList",
        "apiVersion": "v1",
        "groups": [
            {
                "name": "custom.metrics.k8s.io",
                "versions": [
                    {
                        "groupVersion": defaults.API_ENDPOINT,
                        "version": defaults.API_VERSION(),
                    }
                ],
                "preferredVersion": {
                    "groupVersion": defaults.API_ENDPOINT,
                    "version": defaults.API_VERSION(),
                },
            }
        ],
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
