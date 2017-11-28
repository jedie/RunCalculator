#!/usr/bin/env bash

#
# usage:
#   ./built_apk.sh
# or:
#   ./built_apk.sh --verbose
#

CHANGE_USER=-v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro -u=$UID:$(id -g $USER)

set -e
set -x

docker pull jedie/buildozer

(
    cd runcalculator

    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer python --version
    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer pip freeze
    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer cython --version
    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer buildozer --version

    docker run --tty --volume ${PWD}:/buildozer/ ${CHANGE_USER} jedie/buildozer buildozer ${1} android debug
    docker run --tty --volume ${PWD}:/buildozer/ ${CHANGE_USER} jedie/buildozer buildozer ${1} android release
)

ls -la runcalculator/bin/
