# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

API_ENDPOINT = "custom.metrics.k8s.io/v1beta2"
API_ROOT = "/apis/custom.metrics.k8s.io/v1beta2"
NAMESPACE = "flux-operator"
SERVICE_NAME = "custom-metrics-apiserver"
USE_CACHE = True


def API_VERSION():
    """
    Derive the api version from the endpoint
    """
    global API_ENDPOINT
    return API_ENDPOINT.rstrip("/").rsplit("/")[-1]
