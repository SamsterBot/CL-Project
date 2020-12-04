import h5py
import numpy as np
import pickle
from function_lib import *
import builtins
import sys
from plot_results import *
from specify_cells import*
from neuron import h
from neuron import gui

morph_filename = 'EB2-late-bifurcation.swc'
mech_filename = 'updated dict'
dicts = {'soma': [], 'axon': [], 'basal': [], 'trunk': [], 'apical': [], 'tuft': [], 'spine': []}
cells=HocCell(morph_filename, mech_filename)
cells.make_section('soma')
cells.init_synaptic_mechanisms()

soma=h.Section()
stim=h.IClamp(soma(0.5))
stim.amp=0.5
stim.dur=400
stim.delay=500
dv = h.Vector().record(soma(0.5)._ref_v)
plt.plot(dv)
plt.savefig('output/kkk')
print(dv)
dv.printf()


