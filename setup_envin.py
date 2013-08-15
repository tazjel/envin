import distribute_setup
distribute_setup.use_setuptools()


import subprocess
subprocess.call(['python setup.py install'], shell=True)
