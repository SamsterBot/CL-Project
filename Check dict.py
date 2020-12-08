import h5py
import numpy as np
import pickle
from function_lib import *
from plot_results import *
from specify_cells import*
from neuron import h


morph_filename = 'EB2-late-bifurcation.swc'
mech_filename = 'updated dict'
soma = cell.soma[0]  # This will be an SNode2 object, which contains the hoc section as an attribute: soma.sec
# This can also work:
# soma = cell.tree.root

#Using QuickSim object
stim=h.IClamp(soma.sec(0.5))
stim.amp=0.5
stim.dur=400
stim.delay=500

# You also have to record the timestamps!
t = h.Vector().record(h._ref_t)
dv = h.Vector().record(soma.sec(0.5)._ref_v)

del stim
del t
del dv

sim = QuickSim(1000., cvode=0, dt=0.025)
sim.append_rec(cell, cell.tree.root, description='soma', loc=0.5)
sim.append_stim(cell, cell.tree.root, description='step', loc=0.5, amp=0.5, dur=400., delay=500.)

sim.run()
sim.plot()

# You can also access the underlying vectors in python by converting them to numpy arrays:
t_array = np.array(sim.tvec)
dv_array = np.array(sim.get_rec('soma')['vec'])

# And manually plot them:
plt.plot(t_array, dv_array)
plt.show()

# You can also modify the parameters of the current injection:
sim.modify_stim(0, amp=0.2, delay=250., dur=200.)
sim.run()
sim.plot()



'''
Synapse param plotting
'''
#mech_filename = '043016 Type A - km2_NMDA_KIN5_Pr'

cell = CA1_Pyr(morph_filename, mech_filename)

excitatory_stochastic = 1
syn_types = ['Wghkampa']
apical = cell.apical[0] 
cell.insert_spines_in_subset('apical')

# placing synapses in every spine
for sec_type in ['apical']:
    for node in cell.get_nodes_of_subtype(sec_type):
        for spine in node.spines:
            syn = Synapse(cell, spine, syn_types, stochastic=excitatory_stochastic)

cell.init_synaptic_mechanisms()

AMPAR_Perm = 6.3e-7 
plot_synaptic_param_distribution(cell, 'Wghkampa', 'Pmax', scale_factor=1.*AMPAR_Perm, yunits='µS', param_label='Synaptic AMPAR gradient')
plot_mech_param_distribution(cell, 'cat', 'gcatbar')

