# %% [markdown]
"""
![Renode](https://dl.antmicro.com/projects/renode/renode.png)
<table align="left">
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/antmicro/tensorflow-arduino-examples/blob/master/examples/hello-world/$NOTEBOOK.ipynb"><img src="https://raw.githubusercontent.com/antmicro/tensorflow-arduino-examples/master/examples/.static/view-in-colab.png" />Run in Google Colab</a>
  </td>
  <td>
    <a target="_blank" href="https://github.com/antmicro/tensorflow-arduino-examples/blob/master/examples/hello-world/$NOTEBOOK.ipynb"><img src="https://raw.githubusercontent.com/antmicro/tensorflow-arduino-examples/master/examples/.static/view-ipynb.png" />View ipynb on GitHub</a>
  </td>
  <td>
    <a target="_blank" href="https://github.com/antmicro/tensorflow-arduino-examples/blob/master/examples/hello-world/hello_world.py"><img src="https://raw.githubusercontent.com/antmicro/tensorflow-arduino-examples/master/examples/.static/view-source.png" />View Python source on GitHub</a>
  </td>
</table>
"""

# %% [markdown]
"""
## Install requirements
"""

# %%
!pip install -q git+https://github.com/antmicro/pyrenode.git git+https://github.com/antmicro/renode-colab-tools.git
!mkdir -p renode && cd renode && wget https://dl.antmicro.com/projects/renode/builds/renode-latest.linux-portable.tar.gz && tar -xzf renode-latest.linux-portable.tar.gz --strip 1
!pip install -q -r renode/tests/requirements.txt

import os
from renode_colab_tools import metrics
os.environ['PATH'] = os.getcwd()+"/renode:"+os.environ['PATH']
os.environ['TENSORFLOW_PATH'] = os.getcwd()+"/tensorflow-arduino-examples/tensorflow"

# %%
!mkdir -p binaries/hello_world && cd binaries/hello_world && wget https://github.com/antmicro/tensorflow-arduino-examples-binaries/raw/master/hello_world/hello_world.ino.elf # fetch prebuilt binaries

# %% [markdown]
"""## Run the hello-world example in Renode"""

# %%
import time
from pyrenode import *
shutdown_renode()
connect_renode() # this sets up a log file, and clears the simulation (just in case)
tell_renode('using sysbus')
tell_renode('mach create')
tell_renode('machine LoadPlatformDescription @platforms/boards/arduino_nano_33_ble.repl')
tell_renode('sysbus LoadELF @binaries/hello_world/hello_world.ino.elf')

tell_renode('uart0 CreateFileBackend @uart.dump true')
tell_renode('logLevel 3')
tell_renode('machine EnableProfiler @metrics.dump')
tell_renode('s')
while not os.path.exists('renode/uart.dump'):
  time.sleep(1) #waits for creating uart.dump
!timeout 60 tail -c+2 -f renode/uart.dump | sed '/^1$/ q'
tell_renode('q')
expect_cli('Renode is quitting')
time.sleep(1) #wait not to kill Renode forcefully
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
metrics.show_exceptions(parser)

# %%
metrics.configure_plotly_browser_state()
metrics.show_peripheral_access(parser)
