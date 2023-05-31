# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

import json
import os
import subprocess

import flux_metrics_api.utils as utils


def get_api_group_list():
    """
    Get the API group list, assuming we are inside a pod.
    """
    return get_kubernetes_endpoint("apis")


def get_kubernetes_endpoint(endpoint):
    """
    Get an endpoint from the cluster.
    """
    # Point to the internal API server hostname
    api_server = "https://kubernetes.default.svc"

    # Path to ServiceAccount directory
    sa_account_dir = "/var/run/secrets/kubernetes.io/serviceaccount"
    namespace_file = os.path.join(sa_account_dir, "namespace")
    cert_file = os.path.join(sa_account_dir, "ca.crt")
    token_file = os.path.join(sa_account_dir, "token")

    # Cut out early if we aren't running in the pod
    if not all(
        map(os.path.exists, [sa_account_dir, namespace_file, token_file, cert_file])
    ):
        return {}

    # Get the token to do the request
    token = utils.read_file(token_file)

    # Using subprocess to not add extra dependency - yes requires curl
    # res = requests.get(f"{api_server}/apis", headers=headers, verify=cert_file)
    # Kids don't do this at home
    output = subprocess.check_output(
        f'curl --cacert {cert_file} --header "Authorization: Bearer {token}" -X GET {api_server}/{endpoint}',
        shell=True,
    )
    try:
        output = json.loadss(output)
    except Exception:
        return {}
    return output
