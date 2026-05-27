"""Allow running cali with python -m cali."""

from __future__ import annotations

import sys

from cali.cli import main

if __name__ == '__main__':
    sys.exit(main())
