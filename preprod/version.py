"""
This module defines the version information for the preprod package.
It includes the semantic version string, the exact datetime of the version,
and the date component of the version datetime.
"""
from datetime import datetime
__version__="1.4.0"
__versiondatetime__= datetime(2026, 2, 26, 8, 15, 0)
__versiondate__=__versiondatetime__.date()
