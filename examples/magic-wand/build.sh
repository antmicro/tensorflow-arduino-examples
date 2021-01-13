curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
bin/arduino-cli lib install Arduino_LSM9DS1@1.1.0
git clone --quiet https://github.com/antmicro/tensorflow-arduino-examples.git && cp -r tensorflow-arduino-examples/tensorflow $HOME/Arduino/libraries
sed -i'' '/#define DEBUG_SERIAL_OBJECT/s/(Serial)/(Serial1)/' $HOME/Arduino/libraries/tensorflow/src/tensorflow/lite/micro/arduino/debug_log.cpp
bin/arduino-cli compile -b arduino:mbed:nano33ble --output-dir binaries/magic_wand $HOME/Arduino/libraries/tensorflow/examples/magic_wand