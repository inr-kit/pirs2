from setuptools import setup
# Copyright 2015 Karlsruhe Institute of Technology (KIT)
#
# This file is part of PIRS-2.
#
# PIRS-2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PIRS-2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


setup(
    name='pirs',

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
    version='2.24a.11',
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
                'pirs.hli.scf2'],
    scripts=['scripts/mcnp.outp.walltime', ],
    entry_points={'console_scripts': [
        'cadmcnp = pirs.mcnp.cad_vols:main',
        'isocomp = pirs.mcnp.isocomps:main']},
    install_requires=['uncertainties == 2.4.4'],
    provides=['pirs'],
    )
