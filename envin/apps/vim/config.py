SOURCE = 'ftp://ftp.vim.org/pub/vim/unix/vim-7.4.tar.bz2'
CONFIG_CMD = ('./configure'
              ' --enable-perlinterp'
              ' --enable-gpm'
              ' --enable-acl'
              ' --enable-cscope'
              ' --disable-selinux'
              ' --enable-rubyinterp'
              ' --enable-cscope'
              ' --with-features=huge'
              ' --prefix={home}')

PYTHON_CONFIG = (' --enable-{pversion}interp'
                 ' --with-python-config-dir={pconfig_path}'
                 ' vi_cv_path_{pversion}={vi_cv_path_python}')

INSTALL_CMD = 'make; make install'
VIM_DIR = 'vim74'
