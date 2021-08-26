set -e

MAIN_DIR=$(pwd)

function print_available_examples {
    echo "Available examples:"
    for x in $(ls ${MAIN_DIR}/examples |grep -v '\.md'); do
        echo "    ${x}"
    done
}

if [ -z ${1} ]; then
    echo "Please pass example name as argument!"
    print_available_examples && exit 1
fi

EXAMPLE_DIR=examples/${1}
if [ ! -d ${EXAMPLE_DIR} ]; then
    echo "Example \"${1}\" not found."
    print_available_examples && exit 1
fi
cd ${EXAMPLE_DIR}
../../bin/arduino-cli compile -b arduino:mbed:nano33ble --output-dir binaries/${1} ${HOME}/Arduino/libraries/tflite-micro/examples/${1}

cd ${MAIN_DIR}
