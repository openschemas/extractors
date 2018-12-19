#!/usr/bin/env python

import json
import os
import sys


# Called by entrypoint.sh, handles input parsing
# We would normally not want to have this hard coded, but rely on entrypoint.sh
# to ensure arguments are provided.

dockerfile = sys.argv[1]
output_format = sys.argv[2]
contact_name = sys.argv[3]

output_format = output_format.lower()

################################################################################
# Helper Functions
################################################################################

def recursive_find(base, pattern=None):
    '''recursively find files that match a pattern, in this case, we will use
       to find Dockerfiles

       Paramters
       =========
       base: the root directory to start the seartch
       pattern: the pattern to search for using fnmatch
    '''
    if pattern is None:
        pattern = "*"

    for root, dirnames, filenames in os.walk(base):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)


# These extractors are used across a subset

from Organization.extract import extract as org_extract
from ImageDefinition.extract import extract

# Don't define an output html, the user can pipe to one if desired
result = extract(dockerfile, contact_name)
print(result)
