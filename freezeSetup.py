from cx_Freeze import setup, Executable
import os
import datetime

year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
desktop = os.path.join(os.environ["HOMEPATH"], "Desktop").replace('\\', '/')
cwd = os.getcwd().replace('\\', '/')

# executable options
script = 'main.py'
base = 'Win32GUI'  # Win32GUI para gui's e None para console
icon = './img/icon.ico'
targetName = 'MyProject.exe'

# setup options
name = 'MyProject'
version = '0.1'
description = 'MyProject'

# build options
build_directory = 'C:{}/{} Builds/build - {}.{:02d}.{:02d}/build-exe.win32-3.6/'.format(desktop, name, year, month, day)
packages = ['matplotlib', 'atexit', 'PyQt5.QtCore', 'tkinter', 'numpy']
includes = []
include_files = [os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                 os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                 '{}/gui'.format(cwd),
                 '{}/img'.format(cwd)]
excludes = ['zmq']
zip_include_packages = ['asncio', 'ctypes', 'collections', 'curses', 'dateutil', 'distutils', 'email',
                        'encodings', 'imageformats', 'importlib', 'lib2to3', 'logging', 'matplotlib', 'mpl-data',
                        'numpy', 'packaging', 'PyQt5', 'pytz', 'tcl', 'tk', 'tkinter', 'unittest', 'urllib',
                        'colorama', 'concurrent', 'html', 'http', 'ipykernel', 'IPython',
                        'ipython_genutils', 'jinja2', 'json', 'jsonschema', 'jupyter_client', 'jupyter_core',
                        'markupsafe', 'mistune', 'multiprocessing', 'nbconvert', 'nbformat', 'nose', 'notebook',
                        'pkg_resources', 'platforms', 'prompt_toolkit', 'pydoc_data', 'pygments', 'setuptools',
                        'sqlite3', 'test', 'testpath', 'tornado', 'traitlets', 'wcwidth', 'xml', 'xmlrpc', 'PIL',
                        ]
silent = True
optimize = 2

# shortcut options
shortcut_name = 'MyProject'

# bdist_msi options
company_name = 'Mario Raul Freitas'
product_name = 'MyProject'
upgrade_code = '{63320F3A-DC5F-11E2-D341-1132HK39B01E}'
add_to_path = False
install_directory = 'C:{}/{} Builds/build - {}.{:02d}.{:02d}/msi-exe.win32-3.6'.format(desktop, name, year, month, day)

"""
Edit the code above this comment.
Don't edit any of the code bellow.
"""

msi_data = {'Shortcut': [
    ("DesktopShortcut",  # Shortcut
     "DesktopFolder",  # Directory_
     shortcut_name,  # Name
     "TARGETDIR",  # Component_
     "[TARGETDIR]/{}".format(targetName),  # Target
     None,  # Arguments
     None,  # Description
     None,  # Hotkey
     None,  # Icon
     None,  # IconIndex
     None,  # ShowCmd
     "TARGETDIR",  # WkDir
     ),

    ("ProgramMenuShortcut",  # Shortcut
     "ProgramMenuFolder",  # Directory_
     shortcut_name,  # Name
     "TARGETDIR",  # Component_
     "[TARGETDIR]/{}".format(targetName),  # Target
     None,  # Arguments
     None,  # Description
     None,  # Hotkey
     None,  # Icon
     None,  # IconIndex
     None,  # ShowCmd
     "TARGETDIR",  # WkDir
     )
]
}

opt = {
    'build_exe': {'packages': packages,
                  'includes': includes,
                  'include_files': include_files,
                  'excludes': excludes,
                  'zip_include_packages': zip_include_packages,
                  'build_exe': build_directory,
                  'silent': silent,
                  'optimize': optimize
                  },
    'bdist_msi': {'upgrade_code': upgrade_code,
                  'add_to_path': add_to_path,
                  'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
                  'data': msi_data
                  },
    'install_exe': {
        'build_dir': build_directory,
        'skip_build': True
    }
}

exe = Executable(
    script=script,
    base=base,
    icon=icon,
    targetName=targetName,
    # shortcutName=shortcut_name,
    # shortcutDir='DesktopFolder'
)
setup(name=name,
      version=version,
      description=description,
      options=opt,
      executables=[exe]
      )