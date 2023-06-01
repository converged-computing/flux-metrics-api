# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

# This is an example of a custom metrics file you can provide on the command line, e.g,
# flux-metrics-api start --custom-metrics ./custom-metrics.py

# The default format for a custom metric is the following:


def my_custom_metric_name(handle):
    """
    All custom metrics will be passed the active flux handle.

    - The name of the function is the name of the metric.
    - You'll need to import what you need.
    """
    # You'll need to import what you need again from Flux
    # or other places.
    import flux.resource

    rpc = flux.resource.list.resource_list(handle)
    listing = rpc.get()
    return listing.free.ncores
