*** Settings ***
Suite Setup                   Setup
Suite Teardown                Teardown
Test Setup                    Reset Emulation
Test Teardown                 Test Teardown
Resource                      ${RENODEKEYWORDS}

*** Variables ***
${UART}                       sysbus.uart0
${URI}                        @https://dl.antmicro.com/projects/renode

*** Keywords ***
Create Machine
    Execute Command          mach create
    Execute Command          machine LoadPlatformDescription @platforms/boards/arduino_nano_33_ble.repl

    Execute Command          sysbus LoadELF @${CURDIR}/binaries/micro_speech/micro_speech.ino.elf

*** Test Cases ***
Should Detect Yes Pattern
    Create Machine
    Execute Command           sysbus.pdm SetInputFile ${URI}/audio_yes_1s.s16le.pcm-s_32000-b69f5518615516f80ae0082fe9b5a5d29ffebce8

    Create Terminal Tester    ${UART}
    Execute Command           machine EnableProfiler @${CURDIR}/micro_speech.dump
    Start Emulation

    Wait For Line On Uart     Heard yes