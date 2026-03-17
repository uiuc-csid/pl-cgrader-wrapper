#!/bin/bash

# This bundles the grader wrapper with the tests you specifically provide for
# the current question so that the grading Docker can be built on Coursera.

set -eu

SCRIPT_FILENAME="$(basename "$0")"
if [ ! -f "$SCRIPT_FILENAME" ] ; then
    echo "Error: Please run this script (\"./$SCRIPT_FILENAME\") from the same directory where it is located." >&2
    exit 1
fi

GRADER_ZIP="$(basename "$PWD")-grader-build.zip"

zip -r "$GRADER_ZIP" tests Dockerfile postprocess.py wrapper-entrypoint.sh .dockerignore
