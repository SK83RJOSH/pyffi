"""Custom functions for bhkCapsuleShape."""

# ***** BEGIN LICENCE BLOCK *****
#
# Copyright (c) 2007, NIF File Format Library and Tools.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the NIF File Format Library and Tools
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****

import math # math.pi

from PyFFI.Utils import Inertia
from PyFFI.Utils.MathUtils import Vector, LMatrix

def applyScale(self, scale):
    """Apply scale factor <scale> on data."""
    # apply scale on dimensions
    self.radius *= scale
    self.radius1 *= scale
    self.radius2 *= scale
    self.firstPoint *= scale
    self.secondPoint *= scale

    # apply scale on all blocks down the hierarchy
    self.cls.NiObject.applyScale(self, scale)

def getMassCenterInertia(self, density = 1, solid = True):
    """Return mass, center, and inertia tensor."""
    # (assumes self.radius == self.radius1 == self.radius2)
    length = (self.firstPoint - self.secondPoint).getNorm()
    mass, inertia = Inertia.getMassInertiaCapsule(
        radius = self.radius, length = length,
        density = density, solid = solid)
    # now fix inertia so it is expressed in the right coordinates
    # need a transform that maps (0,0,length/2) on (second - first) / 2
    # and (0,0,-length/2) on (first - second)/2
    vec1 = (self.secondPoint - self.firstPoint) / length
    # find an orthogonal vector to vec1
    index = min(enumerate(vec1), key=lambda val: abs(val[1]))[0]
    vec2 = vec1.crossProduct(Vector((1 if i == index else 0)
                                    for i in xrange(3))).getNormalized()
    # find an orthogonal vector to vec1 and vec2
    vec3 = vec1.crossProduct(vec2)
    # get transform matrix
    transform = LMatrix(vec2, vec3, vec1).getTranspose()
    # check the result (debug)
    assert(vec1.getDistance(transform * Vector(0,0,1)) < 0.0001)
    assert(abs(transform.getDeterminant() - 1) < 0.0001)
    # transform the inertia tensor
    inertia = transform.getTranspose() * inertia * transform
    return mass, \
           ((self.firstPoint + self.secondPoint) * 0.5), \
           inertia
