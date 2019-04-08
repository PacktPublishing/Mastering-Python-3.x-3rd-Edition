#!/bin/bash
python3.7 -m zipapp app --python="/usr/bin/env python3.7" --main=oware.client.__main__:main --output=client.pyz
