#!/usr/bin/env bash
# Alias — use bootstrap-gluon-zombie.sh for full hatch.
exec "$(cd "$(dirname "$0")" && pwd)/bootstrap-gluon-zombie.sh" "$@"
