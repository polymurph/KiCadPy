### DEFAULT STARTUP FILE FOR KiCad Python Shell
# Enter any Python code you would like to execute when the PCBNEW python shell first runs.

# For example, uncomment the following lines to import the current board

# import pcbnew
# import eeschema
# board = pcbnew.GetBoard()
# sch = eeschema.GetSchematic()
import sys
kicadpy_dir = '/home/key/git/kicadpy_test/'
sys.path.append(kicadpy_dir)
import kicadpy as kp
sys.path.append(kp.getProjectPath())
