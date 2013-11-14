#import os
#import urllib
#import logging
#import tempfile
#import subprocess
#
##TODO: perhaps we should import it form distribute.
#from setuptools.archive_util import unpack_archive
##from setuptools.command.easy_install import chmod
#
#
#from envin.python.config import PYTHONS
#from envin.python.config import SYSC_FLAGS
##from envin.python.config import SETUP_URL
#from envin.python.config import PATCHES_DIR
#from envin.python.config import INSTALL_COMMAND
##from envin.python.config import ACTIVATE_SCRIPT_SOURCE
#
#from envin.base.base import BaseCommand
#
#
#class PyInstall(BaseCommand):
#    """ Command that installs python. """
#
#    pythons = PYTHONS
#    log = logging.getLogger(__name__)
#
#    def install_requires(self):
#        """ Install required packages for pythons compilation. """
#
#        requirements = os.path.join(os.path.dirname(__file__),
#                                    'requirements.txt')
#        self.install_requires(packages=requirements)
#
#    def take_action(self, parsed_args):
#        greeting = ("You are going to install python. Please select "
#                    "which python distribution you want to install:\n"
#                    "{0}\nPlease enter order nubmers of desired python "
#                    "separated ','.\nFor expampel '1, 2, 4'. If you want to "
#                    "install all pythons simply enter '*'\n")
#
#        pythons = enumerate(self.pythons)
#        greeting = greeting.format(''.join(['{0}. {1}\n'.format(i+1, p[0])
#                                           for i, p in pythons]))
#
#        self.app.stdout.write(greeting)
#        pythons_to_install = raw_input("Enter python order numbers:")
#
#        #TODO: implement parsing of user input.
#        for num in pythons_to_install.split(','):
#            try:
#                idx = int(num)
#            except ValueError:
#                #TODO:do appropriate action.
#                pass
#
#            if idx in [p[0] for p in pythons]:
#                # to be continued
#
#
#
#        #TODO: implement installation path configuration.
#        #      separate for each python ?
#
#
#        #self.log.info('sending greeting')
#        #self.log.debug('debugging')
#        #self.app.stdout.write('hi!\n')
#
#        # install requirements
#        #self.install_requires()
#        # set python compilation flags
#        #unset = []
#
#        #for flag, value in SYSC_FLAGS.items():
#        #    subprocess.call('export %s=%s' % (flag, value), shell=True)
#        #    unset.append(flag)
#
#        #home = os.getcwd()
#        #for p, url in self.pythons.items():
#        #    os.chdir(tempfile.gettempdir())
#        #    source_file = url.split('/')[-1]
#        #    urllib.urlretrieve(url, source_file)
#        #    unpack_archive(source_file, '.')
#        #    source_dir = os.path.splitext(source_file)[0]
#
#        #    if os.path.exists(source_dir):
#        #        os.chdir(source_dir)
#        #        version = p.split('-')[1]
#        #        if version in os.listdir(PATCHES_DIR):
#        #            pdir = '%s/%s' % (PATCHES_DIR, version)
#        #            for patch in os.listdir(pdir):
#        #                subprocess.call('patch -p0 < %s/%s' % (pdir, patch),
#        #                                shell=True)
#
#        #    python_home = '%s/%s' % (home, p)
#        #    os.makedirs(python_home)
#        #    pyinst_cmd = \
#        #        './configure --prefix=%s; make; make install' % python_home
#        #    subprocess.call(pyinst_cmd, shell=True)
#        #    os.chdir(tempfile.gettempdir())
#
#        #for flag in unset:
#        #    subprocess.call('unset %s' % flag, shell=True)
#
#        # installing setuptools
#        #if 'distribute_setup.py' not in os.listdir(tempfile.gettempdir()):
#        #    urllib.urlretrieve(SETUP_URL, 'distribute_setup.py')
#        #subprocess.call('%s/bin/python distribute_setup.py' % python_home,
#        #                shell=True)
#
#        ## installing virtualenv
#        #subprocess.call('%s/bin/easy_install virtualenvwrapper' % python_home,
#        #                shell=True)
#
#        ## install activation script
#        #user_home = os.environ.get('HOME')
#        #bindir = os.path.join(user_home, 'bin')
#        #if not os.path.exists(bindir):
#        #    os.makedirs(bindir)
#        #script_name = '%s/bin/activate-%s' % (user_home, self.version)
#        #with open(script_name, 'w') as act_script:
#        #    info = {'workon_home': '%s/envs/python-%s' % (self.home,
#        #                                                  self.version),
#        #            'project_home': '%s/projects' % self.home,
#        #            'python': '%s/bin/python' % python_home,
#        #            'env': '%s/bin/virtualenv' % python_home,
#        #            'source': '%s/bin/virtualenvwrapper.sh' % python_home}
#        #    act_script.write(ACTIVATE_SCRIPT_SOURCE % info)
#        #chmod(script_name, 0755)
