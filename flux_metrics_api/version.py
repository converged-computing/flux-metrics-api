# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

__version__ = "0.0.11"
AUTHOR = "Vanessa Sochat"
EMAIL = "vsoch@users.noreply.github.com"
NAME = "flux-metrics-api"
PACKAGE_URL = "https://github.com/converged-computing/flux-metrics-api"
KEYWORDS = "cloud, flux, flux-framework, monitoring"
DESCRIPTION = "Custom metrics exporter for Flux in Kubernetes"
LICENSE = "LICENSE"

################################################################################
# Global requirements

INSTALL_REQUIRES = (
    ("uvicorn", {"min_version": None}),
    ("starlette", {"min_version": None}),
    ("starlette-apispec", {"min_version": None}),
)

TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)

################################################################################
# Submodule Requirements (versions that include database)

INSTALL_REQUIRES_ALL = INSTALL_REQUIRES
