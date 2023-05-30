# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

import collections

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


def update_queue_metrics():
    """
    Update metrics for counts of jobs in the queue
    """
    jobs = flux.job.job_list(handle)
    listing = jobs.get()

    # Organize based on states
    states = [x["state"] for x in listing["jobs"]]
    print(states)
    counter = collections.Counter(states)

    # This is how to get states
    # TODO make an endpoint for each, if this works at all :/
    for stateint, _ in counter.items():
        flux.job.info.statetostr(stateint)


# Organize metrics by name so we can eventually support export of custom set (if needed)
metrics = {
    "node_cores_free_count": node_core_free_count,
    "node_cores_up_count": node_core_up_count,
    "node_free_count": node_free_count,
    "node_up_count": node_up_count,
    # TODO add shared function to get queue stats
}
