"""Generate a set of 512^3 density grids with a linear LCDM power spectrum

The bigfiles produced by this script can be used for testing various bskit
routines.
"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import argparse
import h5py
import time

import nbodykit.lab as nbk
from nbodykit.source.catalog.file import Gadget1Catalog,HDFCatalog
from nbodykit import CurrentMPIComm

# Routine to print script status to command line, with elapsed time
def print_status(comm,start_time,message):
    if comm.rank == 0:
        elapsed_time = time.time() - start_time
        print('%d\ts: %s' % (elapsed_time,message))

# Prefix and suffix for files to store grids
out_file_prefix = '%stest_grid_512_' % os.environ['BSKIT_GRID_DIR']
out_file_suffix = '.bigfile'

# Box and grid info
Lbox = 1000.
Nmesh = 512
z = 0
seeds = [1,2]

# Set start time, and print first status message
comm = CurrentMPIComm.get()
start_time = time.time()
print_status(comm,start_time,'Starting grid generation')

# Grab linear power spectrum from nbodykit
cosmo = nbk.cosmology.Planck15
Plin = nbk.cosmology.LinearPower(cosmo, z, transfer='EisensteinHu')

# Set up dict to store power spectra measured from grids
Pk_meas = {}
dk = 2*np.pi/Lbox
kmin = 0.5*dk

# Loop over 2 random seeds
for s in seeds:
    print_status(comm,start_time,'Making Gaussian realization with seed %d' % s)
    
    # Make mesh with Gaussian realization of linear power spectrum
    mesh = nbk.LinearMesh(Plin, Nmesh=Nmesh, BoxSize=Lbox, seed=s)
    
    # Measure power spectrum from mesh and add to dict
    r = nbk.FFTPower(mesh, mode='1d', dk=dk, kmin=kmin)
    Pk = r.power
    Pk_meas[s] = Pk
    
    # Save mesh to disk
    filename = out_file_prefix + str(s) + out_file_suffix
    mesh.save(filename, dataset='Field', mode='real')
    print_status(comm,start_time,'Wrote %s' % filename)
    
# Plot input and measured power spectra
plot_filename = '%spk_comparison.pdf' % os.environ['BSKIT_GRID_DIR']
if comm.rank == 0:
    k_for_plot = np.logspace(-2,1,100)
    plt.loglog(k_for_plot,Plin(k_for_plot),'-',label='Input power spectrum')
    for s in seeds:
        plt.loglog(Pk_meas[s]['k'], np.real(Pk_meas[s]['power']), '-', label='Grid %d' % s)
    plt.legend()
    plt.title('Input power spectra and grid measurements')
    plt.xlabel('k [h Mpc^-1]')
    plt.ylabel('P(k) [h^-3 Mpc^3]')
    plt.savefig(plot_filename)

print_status(comm,start_time,'Wrote plot of power spectra to %s' % plot_filename)
