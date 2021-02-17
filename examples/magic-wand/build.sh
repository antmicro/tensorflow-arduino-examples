curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
bin/arduino-cli core install arduino:mbed
bin/arduino-cli lib install Arduino_LSM9DS1@1.1.0
mkdir -p $HOME/Arduino/libraries && cp -r $TENSORFLOW_PATH $HOME/Arduino/libraries
sed -i'' '/#define DEBUG_SERIAL_OBJECT/s/(Serial)/(Serial1)/' $HOME/Arduino/libraries/tensorflow/src/tensorflow/lite/micro/arduino/system_setup.cpp
bin/arduino-cli compile -b arduino:mbed:nano33ble --output-dir binaries/magic_wand $HOME/Arduino/libraries/tensorflow/examples/magic_wand