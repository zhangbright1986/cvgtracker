from cvgtracker import Tracker
from cvgtracker.controller import *
from cvgtracker.calculator.kfun_fake import *
from cvgtracker.calculator.vasp import Vasp

# define controller and the scheme how it will be evolving
ini_kpts = [3, 3, 3]
controller = KptsController(ini_kpts, scheme='uniform',step=2)

# define the calculator as a function of controller
# calc=Kfunc(controller)
calc = Vasp(controller, cutoff=400, path='./')

# run the tracker
tracker = Tracker(calc, criteria=1.0E-3, log='converge.log',ttype='energy',isBokeh=False)
tracker.run()
tracker.clean_tmpdir()
