#!/usr/bin/env bash

#
# usage:
#   ./built_apk.sh
# or:
#   ./built_apk.sh --verbose
#

set -e

# Generate passwd/group file, e.g.: doesn't exist on travis ;)

TEMP=$(python -c "import tempfile;print(tempfile.gettempdir())")

TEMP_PASSWD=${TEMP}/passwd
TEMP_GROUP=${TEMP}/group

DOCKER_UID=$(id -u)
DOCKER_UGID=$(id -g)
DOCKER_USER=${USER}

echo "${DOCKER_USER}:x:${DOCKER_UID}:${DOCKER_UGID}:${DOCKER_USER},,,:/buildozer/:/bin/bash">${TEMP_PASSWD}
echo "${DOCKER_USER}:x:${DOCKER_UGID}:">${TEMP_GROUP}

CHANGE_USER="-v ${TEMP_GROUP}:/etc/group:ro -v ${TEMP_PASSWD}:/etc/passwd:ro -u=$UID:$(id -g $USER)"

set -x

docker pull jedie/buildozer

(
    cd runcalculator

    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer python --version
    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer pip freeze
    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer cython --version
    docker run --tty --volume ${PWD}:/buildozer/ jedie/buildozer buildozer --version

    docker run --tty --volume ${PWD}:/buildozer/ ${CHANGE_USER} jedie/buildozer id
    docker run --tty --volume ${PWD}:/buildozer/ ${CHANGE_USER} jedie/buildozer pwd
    docker run --tty --volume ${PWD}:/buildozer/ ${CHANGE_USER} jedie/buildozer ls -la

    docker run --tty --volume ${PWD}:/buildozer/ ${CHANGE_USER} jedie/buildozer buildozer ${1} android debug
    docker run --tty --volume ${PWD}:/buildozer/ ${CHANGE_USER} jedie/buildozer buildozer ${1} android release
)

ls -la runcalculator/bin/
