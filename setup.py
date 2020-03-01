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

with open('README.rst', 'r') as f:
    long_descr = f.read()
    long_descr_type = 'text/x-rst'

setup(
    name='pirs2',
    use_scm_version=True,
    description='Python Interfaces for Reactor Simulations',
    long_description=long_descr,
    long_description_content_type=long_descr_type,
    author='Anton Travleev',
    author_email='anton.travleev@kit.edu',
    url='https://github.com/inr-kit/pirs2',
    keywords='MCNP SCF COUPLED REACTOR CALCULATIONS',
    package_data={
        '': ['*.rst'],
    },
    packages=[
        'pirs',
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
    setup_requires=['setuptools_scm'],
    provides=['pirs'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering',
    ],
    )
