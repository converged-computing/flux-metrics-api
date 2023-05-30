# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.schemas import SchemaGenerator

import flux_metrics_api.defaults as defaults
import flux_metrics_api.types as types
import flux_metrics_api.version as version
from flux_metrics_api.metrics import metrics

schemas = SchemaGenerator(
    {
        "openapi": "3.0.0",
        "info": {"title": "Flux Metrics API", "version": version.__version__},
    }
)


class Root(HTTPEndpoint):
    """
    Root of the API

    This needs to return 200 for a health check. I later discovered it also needs
    to return the listing of available metrics!
    """

    async def get(self, request):
        return JSONResponse(types.new_api_resource_list())


def get_metric(request):
    """
    Shared function to get and return a metric response

    We could do some checks / validation of namespace here, but since
    we are just running inside a single namespace we don't care.
    """
    metric_name = request.path_params["metric_name"]
    namespace = request.path_params.get("namespace")
    print(f"Requested metric {metric_name} in  namespace {namespace}")

    # TODO we don't do anything with namespace currently, we assume we won't
    # be able to hit this if running in the wrong one
    # Unknown metric
    if metric_name not in metrics:
        print(f"Unknown metric requested {metric_name}")
        return JSONResponse(
            {"detail": "This metric is not known to the server."}, status_code=404
        )

    # Prepare the metric
    metric = types.new_identifier(metric_name)

    # Get the value from Flux, assemble into listing
    value = metrics[metric_name]()
    metric_value = types.new_metric(metric, value=value)

    # Give the endpoint for the service as metadata
    metadata = {"selfLink": defaults.API_ROOT}
    listing = types.new_metric_list([metric_value], metadata=metadata)
    return JSONResponse(listing)


class Metric(HTTPEndpoint):
    """
    Get a metric for a namespace.

    Since this api server will be running in a namespace, we assume
    we are getting the metric for where it is running (and don't care)
    """

    async def get(self, request):
        return get_metric(request)


def openapi_schema(request):
    """
    Get the openapi spec from the endpoints

    TODO: debug why paths empty
    """
    return JSONResponse(schemas.get_schema(routes=routes))


# STOPPED HERE - make open api spec s we can see endpoints and query
routes = [
    Route(defaults.API_ROOT, Root),
    # Optional for openapi, we could add if needed
    Route(defaults.API_ROOT + "/namespaces/{namespace}/metrics/{metric_name}", Metric),
    Route(defaults.API_ROOT + "/{resource}/{name}/{metric_name}", Metric),
    Route(
        defaults.API_ROOT + "/namespaces/{namespace}/{resource}/{name}/{metric_name}",
        Metric,
    ),
    Route(f"{defaults.API_ROOT}/openapi/v2", openapi_schema, include_in_schema=False),
]
