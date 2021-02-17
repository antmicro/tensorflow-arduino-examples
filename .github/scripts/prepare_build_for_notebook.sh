#!/bin/sh

set -e

echo "git clone https://github.com/antmicro/tensorflow-arduino-examples.git \n$(cat build.sh)" > build.sh
sed -i 's/^/!/' build.sh