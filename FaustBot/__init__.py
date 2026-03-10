import logging
import os
import sys

loglevel = os.getenv("LOGLEVEL", "INFO").upper()  # Default to "INFO" if not set


class PackagePathFilter(logging.Filter):
    def filter(self, record):
        pathname = record.pathname
        record.relativepath = None
        abs_sys_paths = map(os.path.abspath, sys.path)
        for path in sorted(abs_sys_paths, key=len, reverse=True):  # longer paths first
            if not path.endswith(os.sep):
                path += os.sep
            if pathname.startswith(path):
                record.relativepath = os.path.relpath(pathname, path)
                break
        return True


logging.basicConfig(
    level=loglevel,
    format="%(asctime)s - %(name)s - %(levelname)s - %(relativepath)s:%(lineno)d %(funcName)s - %(message)s",
)

logger = logging.getLogger(__name__)
logger.addFilter(PackagePathFilter())
