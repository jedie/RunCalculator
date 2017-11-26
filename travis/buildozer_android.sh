#!/usr/bin/env bash

set -e
set -x

cd runcalculator

buildozer --verbose android debug
buildozer --verbose android release
