# Copyright 2023 Lawrence Livermore National Security, LLC and other
# HPCIC DevTools Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (MIT)


def read_file(path):
    """
    Read content from a file
    """
    with open(path, "r") as fd:
        content = fd.read()
    return content
