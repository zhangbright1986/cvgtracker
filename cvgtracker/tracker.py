#!/usr/bin/env python
import os
from helpers import *

try:
    from bokeh.plotting import figure, curdoc
    from bokeh.client import push_session
except:
    print "failed in importing bokeh"
    pass


class Tracker:
    def __init__(self, calc, criteria=1.0E-6, log='converge.log', ttype='energy', isBokeh=False):
        '''
        :param calc: calculator objector
        :param criteria:  Converge criteria
        :param log: output log
        :param ttype: tracker type: the quantity that is being tracked for convergence.
        :param isBokeh: wheher a Bokeh serve is turned on
       '''

        self.criteria = criteria
        self.calc = calc
        self.log = log
        self.isConverged = False
        self.target_type = ttype
        self.ty = None
        self.counter = 0
        self.r = None
        self.isBokeh = isBokeh

        print "Starting convergence tracker of " + str(self.target_type).capitalize() + " with " + str(
            self.calc.controller.type)

        print 'Calculator: ' + str(self.calc.type)

    def get_target(self):
        print "launching a new " + str(self.calc.type) + " calculation"
        if self.target_type == 'energy':
            target_value = self.calc.get_energy()
        return target_value

    def run(self):
        # run with the initial controller
        self.ty = self.get_target()

        # initialize output log
        openlog = open(self.log, 'w')
        header = 'NO. Itr \t ' + str(self.target_type) + '\t d-' + str(self.target_type) + '\t' + str(
            self.calc.controller.type)
        openlog.write(header + '\n')

        string = str(self.counter) + '\t' + str(self.ty) + '\t' + str(self.ty) + '\t' + str(self.calc.controller.value)
        openlog.write(string + '\n')

        openlog.close()

        print self.counter, self.calc.controller.value, self.ty

        self.counter += 1

        if self.isBokeh:
            self.bokeh_local()
        else:
            plot_log()

        while not self.isConverged:

            # controller update
            self.calc.controller.update()
            # get the target value of updated controller
            ty = self.get_target()

            # write to log file
            openlog = open(self.log, 'a')
            string = str(self.counter) + '\t' + str(ty) + '\t' + str(ty - self.ty) + '\t' + str(
                self.calc.controller.value)
            openlog.write(string + '\n')
            openlog.close()

            # update figure
            if self.isBokeh:
                self.bokeh_update()
            else:
                plot_log()

            # when it is conveged
            if abs(ty - self.ty) < self.criteria:
                self.isConverged = True
                print str(self.target_type).capitalize() + ' convereged with criteria of ' + str(
                    self.criteria) + " at " + str(self.calc.controller.value)

            # target value updated
            self.ty = ty
            print self.counter, self.calc.controller.value, self.ty
            self.counter += 1

    def bokeh_local(self):
        p = figure()
        x, y = read_log()
        # print x, y
        self.r = p.line(x, y, color='navy', line_width=3)
        session = push_session(curdoc())
        session.show()

    def bokeh_update(self):
        x, y = read_log()
        self.r.data_source.data["x"] = x
        self.r.data_source.data["y"] = y

    def clean_tmpdir(self):
        os.system('rm -rf tmp_*')
