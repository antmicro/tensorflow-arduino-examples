# %% [markdown]
"""
![Renode](https://antmicro.com/OpenSource/assets/images/projects/renode.png)
"""

# %% [markdown]
"""
## Install requirements
"""

# %%
!pip install -q git+https://github.com/antmicro/pyrenode.git git+https://github.com/antmicro/renode-colab-tools.git
!mkdir -p renode && cd renode && wget http://dl.antmicro.com/projects/renode/builds/renode-1.11+colab.linux-portable.tar.gz &&  tar -xzf renode-1.11+colab.linux-portable.tar.gz --strip 1
!pip install -q -r renode/tests/requirements.txt
!git clone --quiet https://github.com/antmicro/tensorflow-arduino-examples.git

import os
from renode_colab_tools import *
os.environ['PATH'] = os.getcwd()+"/renode:"+os.environ['PATH']

# %%
!mkdir -p binaries/magic_wand && cd binaries/magic_wand && wget https://github.com/antmicro/tensorflow-arduino-examples-binaries/raw/master/magic_wand/magic_wand.ino.elf # fetch prebuilt binaries

# %% [markdown]
"""## Run a magic-wand example in Renode"""

# %%
import time
from pyrenode import *
shutdown_renode()
connect_renode() # this sets up a log file, and clears the simulation (just in case)
tell_renode('using sysbus')
tell_renode('mach create')
tell_renode('machine LoadPlatformDescription @/content/renode/platforms/boards/arduino_nano_33_ble.repl')
tell_renode('sysbus LoadELF @/content/binaries/magic_wand/magic_wand.ino.elf')

tell_renode('uart0 CreateFileBackend @uart.dump true')
tell_renode('logLevel 3')
tell_renode('machine EnableProfiler "metrics.dump"')
tell_renode('sysbus.twi0.lsm9ds1_imu FeedAccelerationSample @/content/tensorflow-arduino-examples/examples/magic-wand/angle_rotated.data')
tell_renode('s')
time.sleep(5) #waits for creating uart.dump
!timeout 60 tail -c+2 -f renode/uart.dump | sed '/\* \* \* \* \* \* \* \*/ q'
tell_renode('q')
expect_cli('Renode is quitting')
shutdown_renode()

# %% [markdown]
"""## Renode metrics analysis"""

# %%
from renode.tools.metrics_analyzer.metrics_parser import MetricsParser
init_notebook_mode(connected=False)
parser = MetricsParser('renode/metrics.dump')

# %%
configure_plotly_browser_state()
show_executed_instructions(parser)

# %%
configure_plotly_browser_state()
show_memory_access(parser)

# %%
configure_plotly_browser_state()
show_exceptions(parser)

# %%
configure_plotly_browser_state()
show_peripheral_access(parser)