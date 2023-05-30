#!/usr/bin/env python3

# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)

import argparse
import os
import sys

import uvicorn
from starlette.applications import Starlette

import flux_metrics_api
import flux_metrics_api.defaults as defaults
from flux_metrics_api.logger import setup_logger
from flux_metrics_api.routes import routes


def get_parser():
    parser = argparse.ArgumentParser(
        description="Flux Metrics API",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Global Variables
    parser.add_argument(
        "--debug",
        help="use verbose logging to debug.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--quiet",
        help="Silence most output and logging.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--version",
        dest="version",
        help="show software version.",
        default=False,
        action="store_true",
    )

    subparsers = parser.add_subparsers(
        help="flux_metrics_api actions",
        title="actions",
        description="actions",
        dest="command",
    )

    # print version and exit
    subparsers.add_parser("version", description="show software version")

    # Local shell with client loaded
    start = subparsers.add_parser(
        "start",
        description="Start the running server.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    start.add_argument(
        "--port",
        help="Port to run application",
        default=8080,
        type=int,
    )
    start.add_argument(
        "--namespace", help="Scope to running in these namespace(s)", action="append"
    )
    start.add_argument(
        "--api-path",
        dest="api_path",
        help="Custom API path (defaults to /apis/custom.metrics.k8s.io/v1beta2)",
        default=None,
    )

    start.add_argument(
        "--host",
        help="Host address to run application",
        default="0.0.0.0",
    )
    start.add_argument(
        "--verbose",
        help="add verbose metrics about server usage and garbage collection (not related to Flux).",
        default=False,
        action="store_true",
    )
    return parser


def start(args):
    """
    Start the server with uvicorn
    """
    app = Starlette(debug=args.debug, routes=routes)
    uvicorn.run(app, host=args.host, port=args.port)


def main():
    parser = get_parser()

    def help(return_code=0):
        version = flux_metrics_api.__version__

        print("\nFlux Prometheus v%s" % version)
        parser.print_help()
        sys.exit(return_code)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, _ = parser.parse_known_args()
    if args.debug is True:
        os.environ["MESSAGELEVEL"] = "DEBUG"

    # Show the version and exit
    if args.command == "version" or args.version:
        print(flux_metrics_api.__version__)
        sys.exit(0)

    setup_logger(
        quiet=args.quiet,
        debug=args.debug,
    )

    # Setup the registry - non verbose is default
    print(f"API endpoint is at {defaults.API_ROOT}")
    if args.api_path is not None:
        print(f"Setting API endpoint to {args.api_path}")
        defaults.API_ROOT = args.api_path

    # Limit to specific namespaces?
    if args.namespace:
        defaults.NAMESPACES = args.namespace

    # Does the user want a shell?
    if args.command == "start":
        return start(args)

    sys.exit(f"{args.command} is not a known command.")


if __name__ == "__main__":
    main()
