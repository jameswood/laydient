# laydient
Swap filaments throughout am FDM 3D print to create a vertical gradient effect

## usage
from a command prompt, use ```laydient.py /path/to/source.gcode```

Or place ```/path/to/laydient.py``` in the Post-processing scripts section in PrusaSlicer or maybe other slicers

## how it works
it searches for ```LAYER_CHANGE``` in the input gcode, counts them, then generates a gradient with that number of steps. Then it searches again and inserts toolchanges into the gcode at the appropriate layers. Finally, it outputs the code as ```input-filename_gradient.gcode``` into the source directory.
