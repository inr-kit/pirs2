# try:
#     from setuptools import setup
# except ImportError:
# from distutils.core import setup
from setuptools import setup

setup(
        name = 'pirs',

        # version X.Yy.R means the following:
        #
        # X -- Major version, backward-incompatible. New major version when:
        #      * changes in package structure,
        #      * change in concepts in pirs.core (relevant for all subpackages)
        #
        # Y -- Minor version, backward-compatible with all previous versions of
        #      the same major version. New minor verions when:
        #      * new classes, methods, functions are added
        #      * for alpha stage, when names are changed.
        #
        # Ya -- alpha stage. Means that API (class, method, function names) can
        #       be changed. For alpha versions, backward compatibility not
        #       assumed.
        #
        # R -- Bugs counter.
        #
        version='2.22a.10',
        description='Python Interfaces for Reactor Simulations',
        author='Anton Travleev',
        author_email='anton.travleev@kit.edu',
        url='',
        packages=['pirs',
                  # stuff reusable in other sub-packages
                  'pirs.core',
                  'pirs.core.tramat',
                  'pirs.core.trageom',
                  'pirs.core.scheduler',
                  # low-level interfaces
                  'pirs.mcnp',
                  'pirs.mcnp.auxiliary',
                  # 'pirs.scf',
                  'pirs.scf2',
                  'pirs.scf3',
                  # general tools
                  'pirs.tools',
                  'pirs.tools.plots',
                  # geometry modelling
                  'pirs.solids',
                  # high-level interfaces
                  'pirs.hli',
                  'pirs.hli.mcnp',
                  # 'pirs.hli.scf',
                  'pirs.hli.scf2',
                  ],
        scripts=['scripts/mcnp.outp.walltime', ],
        entry_points={'console_scripts': ['cadmcnp = pirs.mcnp.cad_vols:main']},
        install_requires=['uncertainties == 2.4.4'],
        provides=['pirs'],
     )
