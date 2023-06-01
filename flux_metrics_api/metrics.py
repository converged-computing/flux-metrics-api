# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

import collections
import importlib.util
import inspect
import os
import shutil
import sys

import flux_metrics_api.utils as utils
from flux_metrics_api.logger import logger

try:
    import flux
    import flux.job
    import flux.resource
except ImportError:
    logger.exit(
        "Cannot import flux. Please ensure that flux Python bindings are on the PYTHONPATH."
    )


# Keep a global handle so we make it just once
handle = flux.Flux()


def node_core_free_count():
    """
    Function to use the flux handle to get node cores free
    """
    rpc = flux.resource.list.resource_list(handle)
    listing = rpc.get()
    return listing.free.ncores


def node_core_up_count():
    """
    Function to use the flux handle to get node cores up
    """
    rpc = flux.resource.list.resource_list(handle)
    listing = rpc.get()
    return listing.up.ncores


def node_up_count():
    """
    Function to use the flux handle to get nodes up
    """
    rpc = flux.resource.list.resource_list(handle)
    listing = rpc.get()
    return len(listing.up.nodelist)


def node_free_count():
    """
    Function to use the flux handle to get nodes free
    """
    rpc = flux.resource.list.resource_list(handle)
    listing = rpc.get()
    return len(listing.free.nodelist)


def get_queue_metrics():
    """
    Update metrics for counts of jobs in the queue

    See https://github.com/flux-framework/flux-core/blob/master/src/common/libjob/job.h#L45-L53
    for identifiers.
    """
    jobs = flux.job.job_list(handle)
    listing = jobs.get()

    # Organize based on states
    states = [x["state"] for x in listing["jobs"]]
    counter = collections.Counter(states)

    # Lookup of state name to integer
    lookup = {
        "new": 1,
        "depend": 2,
        "priority": 4,
        "sched": 8,
        "run": 16,
        "cleanup": 32,
        "inactive": 64,
    }

    # This is how to get states
    counts = {}
    for stateint, count in counter.items():
        state = flux.job.info.statetostr(stateint)
        counts[state] = count
    for state in lookup:
        if state not in counts:
            counts[state] = 0
    return counts


# Queue states


def job_queue_state_new_count():
    return get_queue_metrics()["new"]


def job_queue_state_depend_count():
    return get_queue_metrics()["depend"]


def job_queue_state_priority_count():
    return get_queue_metrics()["priority"]


def job_queue_state_sched_count():
    return get_queue_metrics()["sched"]


def job_queue_state_run_count():
    return get_queue_metrics()["run"]


def job_queue_state_cleanup_count():
    return get_queue_metrics()["cleanup"]


def job_queue_state_inactive_count():
    return get_queue_metrics()["inactive"]


def add_custom_metrics(metric_file):
    """
    Add custom metrics to the server
    """
    global metrics
    tmpdir = utils.get_tmpdir()

    # Copy our metrics file there and do relative import
    custom_metrics_file = os.path.join(tmpdir, "custom_metrics.py")
    shutil.copyfile(metric_file, custom_metrics_file)
    spec = importlib.util.spec_from_file_location("custom_metrics", custom_metrics_file)
    cm = importlib.util.module_from_spec(spec)
    sys.modules["cm"] = cm
    spec.loader.exec_module(cm)

    # Discover the names, and add the functions!
    for contender in dir(cm):
        if contender.startswith("_"):
            continue
        func = getattr(cm, contender)

        # We only care about functions
        if func.__class__.__name__ == "function":
            args = inspect.signature(func)

            # Must have at least one argument (the handle)
            # We could be more strict here, but this is probably OK
            if len(args.parameters) == 0:
                sys.exit(f"{contender} is not a valid function - has no arguments")
            print(f"Adding custom function {contender} to metrics.")
            custom_metrics[contender] = func

    # Cleanup
    shutil.rmtree(tmpdir)


# Organize metrics by name
metrics = {
    # Node resources
    "node_cores_free_count": node_core_free_count,
    "node_cores_up_count": node_core_up_count,
    "node_free_count": node_free_count,
    "node_up_count": node_up_count,
    # Queue states
    "job_queue_state_new_count": job_queue_state_new_count,
    "job_queue_state_depend_count": job_queue_state_depend_count,
    "job_queue_state_priority_count": job_queue_state_priority_count,
    "job_queue_state_sched_count": job_queue_state_sched_count,
    "job_queue_state_run_count": job_queue_state_run_count,
    "job_queue_state_cleanup_count": job_queue_state_cleanup_count,
    "job_queue_state_inactive_count": job_queue_state_inactive_count,
}

# Custom metrics defined by the user (have the handle provided)
custom_metrics = {}
