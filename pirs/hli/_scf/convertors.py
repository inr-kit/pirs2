"""
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

Convert SCF results, as read by the scf.output module, 
to hpmc.solids
"""


def mean(v1, v2):
    """
    This function is often used in map().
    """
    return (v1 + v2)*0.5

def rod_to_solid(rod, solid, temperature='tfuave'):
    """
    for a given rod that is the result of a call to scf.output.read_ouput(),
    make a copy of solid and set the temperature values according to those
    found in channel.

    >>> (rods, channels) = scf.output.read_output(...)
    >>> new_rod = rod_to_solid(rods[i], original_rod) # i any index

    the optional third argument specifies the string identifier of the
    temperature coloumn in the scf output file.

    """

    zmin = rod.column('Zmin')
    zmax = rod.column('Zmax')
    T = rod.column(temperature)

    dz = map(lambda z1, z2: z2-z1, zmin, zmax)

    res = solid.copy_node()
    res.temp.set_values(0)
    res.temp.set_grid(dz)
    res.temp.set_values(T)
    res.temp = res.temp + 273.15 # Celsius -> Kelvin
    return res


def channel_to_solid(channel, solid):
    """
    for a given channel that is the result of a call to
    scf.output.read_ouput(), make a copy of solid and set the temperature and
    density values according to those found in channel.

    >>> (rods, channels) = scf.output.read_output(...)
    >>> new_channel = channel_to_solid(channels[i], original_channel) # i any index

    """

    z = channel.column('distance')
    T = channel.column('temperature')
    D = channel.column('density')

    dz = map(lambda z1, z2: z2-z1, z[:-1], z[1:])

    # output tables for channels give data at node boundaries, while in solids
    # average over axial node are needed.
    T = map(mean, T[:-1], T[1:])
    D = map(mean, D[:-1], D[1:])

    res = solid.copy_node()

    res.temp.set_values(0)
    res.temp.set_grid(dz)
    res.temp.set_values(T)

    res.dens.set_values(0)
    res.dens.set_grid(dz)
    res.dens.set_values(D)

    res.temp = res.temp + 273.15 # Celsius -> Kelvin
    res.dens = res.dens * 1e-3   # kg/m3 -> g/cm3

    return res

def to_float(v):
    """
    Convert a value that might carry an uncertainty to a regular floating point
    value.
    """

    r = None
    try:
        r = v.nominal_value
    except AttributeError:
        r = float(v)

    return r
