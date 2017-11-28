#!/usr/bin/env bash

#
# usage:
#   ./built_apk.sh
# or:
#   ./built_apk.sh --verbose
#

set -e
set -x

docker pull jedie/buildozer

(
    cd runcalculator

    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer python --version
    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer pip freeze
    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer cython --version
    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer buildozer --version

    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer buildozer ${1} android debug
    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer buildozer ${1} android release
)

ls -la runcalculator/bin/
