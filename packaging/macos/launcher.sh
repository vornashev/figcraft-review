#!/bin/sh
# FigCraft Review.app's executable: the bundled Python runs the app (sidecar/app.py) from Resources.
here="$(cd "$(dirname "$0")/../Resources" && pwd)"
export PYTHONDONTWRITEBYTECODE=1  # the bundle is signed: bytecode was compiled when it was built
exec "$here/python/bin/python3" "$here/app/sidecar/app.py" "$@"
