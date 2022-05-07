#!/bin/bash
set -e

nfc_status=${python -m nfc}

if [["$nfc_status" =~ "port100"]] then
  modprobe -r port100
fi

exec "$@"
