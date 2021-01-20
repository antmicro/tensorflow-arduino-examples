curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
bin/arduino-cli core install arduino:mbed
git clone --quiet https://github.com/antmicro/tensorflow-arduino-examples.git && mkdir -p $HOME/Arduino/libraries && cp -r tensorflow-arduino-examples/tensorflow $HOME/Arduino/libraries
sed -i'' '/#define DEBUG_SERIAL_OBJECT/s/(Serial)/(Serial1)/' $HOME/Arduino/libraries/tensorflow/src/tensorflow/lite/micro/arduino/debug_log.cpp
bin/arduino-cli compile -b arduino:mbed:nano33ble --output-dir binaries/micro_speech $HOME/Arduino/libraries/tensorflow/examples/micro_speech