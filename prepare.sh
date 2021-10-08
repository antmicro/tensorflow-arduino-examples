set -x
git submodule update --init
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
bin/arduino-cli core install arduino:mbed
# Required by magic_wand example
bin/arduino-cli lib install Arduino_LSM9DS1@1.1.0
# Required by person_detection example
bin/arduino-cli lib install JPEGDecoder@1.8.0
git clone --quiet https://github.com/ArduCAM/Arduino.git
# Make sure no hardware platform is selected
sed --in-place --regexp-extended 's|^(#define OV[0-9]+_MINI_[0-9]MP_[A-Z_]*)|//\1|g' Arduino/ArduCAM/memorysaver.h && \
# Select the platform specified in `arduino_image_provider.cpp`
sed --in-place 's|//#define OV2640_MINI_2MP_PLUS|#define OV2640_MINI_2MP_PLUS|' Arduino/ArduCAM/memorysaver.h
cp --recursive Arduino/ArduCAM $HOME/Arduino/libraries/ArduCAM
 > $HOME/Arduino/libraries/JPEGDecoder/src/User_Config.h
rm --recursive --force Arduino

sed --in-place '/#define DEBUG_SERIAL_OBJECT/s/(Serial)/(Serial1)/' tflite-micro/src/tensorflow/lite/micro/system_setup.cpp
mkdir -p $HOME/Arduino/libraries && cp -r $TENSORFLOW_PATH $HOME/Arduino/libraries

