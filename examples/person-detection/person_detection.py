# %% [markdown]
"""
![Renode](https://dl.antmicro.com/projects/renode/renode.png)
<table align="left">
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/antmicro/tensorflow-arduino-examples/blob/master/examples/person-detection/$NOTEBOOK.ipynb"><img src="https://raw.githubusercontent.com/antmicro/tensorflow-arduino-examples/master/examples/.static/view-in-colab.png" />Run in Google Colab</a>
  </td>
  <td>
    <a target="_blank" href="https://github.com/antmicro/tensorflow-arduino-examples/blob/master/examples/person-detection/$NOTEBOOK.ipynb"><img src="https://raw.githubusercontent.com/antmicro/tensorflow-arduino-examples/master/examples/.static/view-ipynb.png" />View ipynb on GitHub</a>
  </td>
  <td>
    <a target="_blank" href="https://github.com/antmicro/tensorflow-arduino-examples/blob/master/examples/person-detection/person_detection.py"><img src="https://raw.githubusercontent.com/antmicro/tensorflow-arduino-examples/master/examples/.static/view-source.png" />View Python source on GitHub</a>
  </td>
</table>
"""

# %% [markdown]
"""
## Install requirements
"""

# %%
!pip install -q git+https://github.com/antmicro/pyrenode.git git+https://github.com/antmicro/renode-colab-tools.git Pillow
!mkdir -p renode && cd renode && wget https://dl.antmicro.com/projects/renode/builds/renode-latest.linux-portable.tar.gz && tar -xzf renode-latest.linux-portable.tar.gz --strip 1
!pip install -q -r renode/tests/requirements.txt
!wget -O default.jpg https://dl.antmicro.com/projects/renode/images/person_image_0.jpg-s_3853-7f2125e28423fa117a1079d84785b17c9b70f62d #download default photo

import os
from renode_colab_tools import image, metrics
os.environ['PATH'] = os.getcwd()+"/renode:"+os.environ['PATH']
os.environ['TENSORFLOW_PATH'] = os.getcwd()+"/tensorflow-arduino-examples/tensorflow"

# %%
!mkdir -p binaries/person_detection && cd binaries/person_detection && wget https://github.com/antmicro/tensorflow-arduino-examples-binaries/raw/master/person_detection/person_detection.ino.elf # fetch prebuilt binaries

# %% [markdown]
"""
## Take a photo
To change the selected option, rerun the cell
"""

# %%
image.image_options()
# %% [markdown]
"""## Convert the photo, required size < 4096 bytes"""

# %%
from PIL import Image as pil
from IPython.display import Image, display
photo = pil.open('photo.jpg')
photo.thumbnail((120, 120))
photo.save('photo.jpg')
display(Image('photo.jpg'))

# %% [markdown]
"""## Run a person-detection example with a captured photo in Renode"""

# %%
import time
from pyrenode import *
shutdown_renode()
connect_renode() # this sets up a log file, and clears the simulation (just in case)
tell_renode('using sysbus')
tell_renode('mach create')
tell_renode('machine LoadPlatformDescription @platforms/boards/arduino_nano_33_ble.repl')
tell_renode('sysbus LoadELF @binaries/person_detection/person_detection.ino.elf')

tell_renode('uart0 CreateFileBackend @uart.dump true')
tell_renode('logLevel 3')
tell_renode('spi2.camera ImageSource @photo.jpg')
tell_renode('machine EnableProfiler "metrics.dump"')
tell_renode('s')
time.sleep(5) #waits for creating uart.dump
!timeout 120 tail -c+2 -f renode/uart.dump | sed '/^Person score: .*$/ q'
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
