# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

from apispec import APISpec
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette_apispec import APISpecSchemaGenerator

import flux_metrics_api.defaults as defaults
import flux_metrics_api.types as types
import flux_metrics_api.version as version
from flux_metrics_api.metrics import custom_metrics, handle, metrics

schemas = APISpecSchemaGenerator(
    APISpec(
        title="Flux Metrics API",
        version=version.__version__,
        openapi_version="3.0.0",
        info={"description": "Export Flux custom metrics."},
    )
)

not_found_response = JSONResponse(
    {"detail": "The metric server is not running in a Kubernetes pod."},
    status_code=404,
)


class Root(HTTPEndpoint):
    """
    Root of the API

    This needs to return 200 for a health check. I later discovered it also needs
    to return the listing of available metrics!
    """

    async def get(self, request):
        return JSONResponse(types.new_resource_list())


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
    if metric_name not in metrics and metric_name not in custom_metrics:
        print(f"Unknown metric requested {metric_name}")
        return JSONResponse(
            {"detail": "This metric is not known to the server."}, status_code=404
        )

    # Prepare the metric
    metric = types.new_identifier(metric_name)

    # Get the value from Flux, assemble into listing
    if metric_name in custom_metrics:
        value = custom_metrics[metric_name](handle)
    else:
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


class APIGroupList(HTTPEndpoint):
    """
    Service a faux resource list just for our custom metrics endpoint.
    """

    async def get(self, request):
        listing = types.new_group_list()
        if not listing:
            return not_found_response
        return JSONResponse(listing)


class OpenAPI(HTTPEndpoint):
    """
    Forward the cluster openapi endpoint
    """

    async def get(self, request):
        version = request.path_params["version"]
        openapi = types.get_cluster_schema(version)
        if not openapi:
            return not_found_response
        return JSONResponse(openapi)


def openapi_schema(request):
    """
    Get the openapi spec from the endpoints
    """
    return JSONResponse(schemas.get_schema(routes=routes))


routes = [
    Route(defaults.API_ROOT, Root),
    # This is a faux route so we can get the preferred resource version
    Route("/apis", APIGroupList),
    Route("/openapi/{version}", OpenAPI),
    Route(defaults.API_ROOT + "/namespaces/{namespace}/metrics/{metric_name}", Metric),
    Route(defaults.API_ROOT + "/{resource}/{name}/{metric_name}", Metric),
    Route(
        defaults.API_ROOT + "/namespaces/{namespace}/{resource}/{name}/{metric_name}",
        Metric,
    ),
    # These are for our endpoints
    Route("/schema", openapi_schema, include_in_schema=False),
    Route(f"{defaults.API_ROOT}/openapi/v2", openapi_schema, include_in_schema=False),
]
