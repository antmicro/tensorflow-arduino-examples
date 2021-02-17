# %% [markdown]
"""
![Renode](https://antmicro.com/OpenSource/assets/images/projects/renode.png)
"""

# %% [markdown]
"""
## Install requirements
"""
# %%
!pip install -q ffmpeg-python pyaudioconvert git+https://github.com/antmicro/pyrenode.git git+https://github.com/antmicro/renode-colab-tools.git
!apt install -q xxd sox
!mkdir -p renode && cd renode && wget https://dl.antmicro.com/projects/renode/builds/renode-latest.linux-portable.tar.gz && tar -xzf renode-latest.linux-portable.tar.gz --strip 1
!pip install -q -r renode/tests/requirements.txt
!wget -O binary_yes https://dl.antmicro.com/projects/renode/audio_yes_1s.s16le.pcm-s_32000-b69f5518615516f80ae0082fe9b5a5d29ffebce8
!wget -O binary_no https://dl.antmicro.com/projects/renode/audio_no_1s.s16le.pcm-s_32000-f36b60d425c9d5414a38658dbd096313d82d28c5

import os
from renode_colab_tools import audio, metrics
os.environ['PATH'] = os.getcwd()+"/renode:"+os.environ['PATH']
os.environ['TENSORFLOW_PATH'] = os.getcwd()+"/tensorflow-arduino-examples/tensorflow"

# %%
!mkdir -p binaries/micro_speech && cd binaries/micro_speech && wget https://github.com/antmicro/tensorflow-arduino-examples-binaries/raw/master/micro_speech/micro_speech.ino.elf # fetch prebuilt binaries
# %% [markdown]
"""
## Get audio
"""
# %%
audio.audio_options()

# %% [markdown]
"""
## Run a micro-speech example in Renode
The command may not be recognized correctly due to https://github.com/tensorflow/tensorflow/pull/45878
"""
# %%
import time
from pyrenode import *
shutdown_renode()
connect_renode() # this sets up a log file, and clears the simulation (just in case)

tell_renode('using sysbus')
tell_renode('mach create')
tell_renode('machine LoadPlatformDescription @platforms/boards/arduino_nano_33_ble.repl')
tell_renode('sysbus LoadELF @binaries/micro_speech/micro_speech.ino.elf')

tell_renode('logLevel 3')
tell_renode('pdm SetInputFile @audio_bin')
tell_renode('uart0 CreateFileBackend @uart.dump true')
tell_renode('machine EnableProfiler @metrics.dump')
tell_renode('s')
while not os.path.exists('renode/uart.dump'):
  time.sleep(1) #waits for creating uart.dump
!timeout 60 tail -f renode/uart.dump | sed '/^.*Heard .*$/ q' | cut -c 2-
tell_renode('q')
expect_cli('Renode is quitting')
shutdown_renode()

# %% [markdown]
"""## Renode metrics analysis"""

# %%
from renode.tools.metrics_analyzer.metrics_parser import MetricsParser
metrics.init_notebook_mode(connected=False)
parser = MetricsParser('renode/metrics.dump')

# %%
metrics.configure_plotly_browser_state()
metrics.show_executed_instructions(parser)

# %%
metrics.configure_plotly_browser_state()
metrics.show_memory_access(parser)

# %%
metrics.configure_plotly_browser_state()
metrics.show_peripheral_access(parser)

# %%
metrics.configure_plotly_browser_state()
metrics.show_exceptions(parser)