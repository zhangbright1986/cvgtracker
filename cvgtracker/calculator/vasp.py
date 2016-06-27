import numpy as np
import os, sys, time
from cvgtracker.helpers import randomstring
import shutil


class Vasp:
    def __init__(self, controller, cutoff=400, path='./'):
        '''
        :param controller: controller object
        :param cutoff: Kinetic energy cutoff
        :param path: path the calculations will be performed, also is the path to check input files
        '''
        self.energy = None
        self.force = None
        self.controller = controller
        self.cutoff = cutoff
        self.path = os.path.abspath(path)
        self.type = 'VASP'

        #print self.path
        if not self.check_file():
            print "Input files are not ready"
            sys.exit(1)

    def check_file(self):
        status = False
        if os.path.isdir(self.path):
            status = True
            for file in ('INCAR', 'KPOINTS', 'POTCAR', 'POSCAR'):
                # print os.path.join(self.path,file)
                status = status and os.path.isfile(os.path.join(self.path, file))
        return status

    def prepare_job(self):
        os.chdir(self.path)
        name = 'tmp_' + randomstring()
        tmp_path = os.path.join(self.path, name)
        os.mkdir(tmp_path)
        for file in ('INCAR', 'KPOINTS', 'POTCAR', 'POSCAR'):
            shutil.copyfile(os.path.join(self.path, file), os.path.join(tmp_path, file))
        os.chdir(tmp_path)
        self.set_kecutoff()
        self.write_kpoints()

    def run(self):
        exitcode = os.system('%s > %s' % ('vasp', 'vasp.out'))
        # print "test"
        if exitcode != 0:
            raise RuntimeError('Vasp exited with exit code: %d.  ' % exitcode)

        self.energy = self.read_energy()

        # print self.energy
        # self.force = self.read_force()
        os.chdir(self.path)

    def calculate(self):
        self.prepare_job()
        self.run()

    def set_kecutoff(self):
        incar = open('INCAR', 'r')
        new_incar = open('INCAR.new', 'w')
        for line in incar:
            if line.lower().find('encut') == -1:
                new_incar.write(line)

        new_incar.write("ENCUT= " + str(self.cutoff))
        incar.close()
        new_incar.close()
        shutil.move('INCAR.new', 'INCAR')

    def write_kpoints(self):
        """Writes the KPOINTS file."""
        p = self.controller.value
        # print p

        kpoints = open('KPOINTS', 'w')
        kpoints.write('KPOINTS created by Atomic Simulation Environemnt\n')
        kpoints.write('0\n')
        kpoints.write('Monkhorst-Pack\n')
        [kpoints.write('%i ' % kpt) for kpt in p]
        kpoints.write('\n0 0 0\n')
        kpoints.close()

    def read_energy(self):
        energy = 0.0
        for line in open('OSZICAR', 'r'):
            # print line.lower().find('e0=')
            if line.lower().find('e0=') != -1:
                # energy_free = float(line.split()[2])
                energy = float(line.split()[4])
        return energy

    def get_energy(self):
        self.calculate()
        return self.energy

    def get_force(self):
        self.calculate()
        return self.force
