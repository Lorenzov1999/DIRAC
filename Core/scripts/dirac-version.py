#!/usr/bin/env python
########################################################################
# File :   dirac-version
# Author : Ricardo Graciani
########################################################################
"""
Print version of current DIRAC installation

Usage::

  dirac-version [option]

Example::

  $ dirac-version

"""
from __future__ import print_function

__RCSID__ = "$Id$"

import sys
import getopt

cmdOpt = ('h', 'help', 'help doc string')

optList, args = getopt.getopt(sys.argv[1:], cmdOpt[0], cmdOpt[1])
for opt, value in optList:
  if opt in ('-h', '--help'):
    print(__doc__)
    print('Options::\n\n')
    print("  %s %s : %s" % (cmdOpt[0].ljust(3), cmdOpt[1].ljust(20), cmdOpt[2]))
    sys.exit(0)

import DIRAC
print(DIRAC.version)
