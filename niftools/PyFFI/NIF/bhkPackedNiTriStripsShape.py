# --------------------------------------------------------------------------
# NifFormat.bhkPackedNiTriStripsShape
# Custom functions for bhkPackedNiTriStripsShape.
# --------------------------------------------------------------------------
# ***** BEGIN LICENSE BLOCK *****
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
# ***** END LICENCE BLOCK *****
# --------------------------------------------------------------------------

def addShape(self, triangles, normals, vertices, layer = 0, material = 0):
    """Pack the given geometry."""
    # increase number of shapes
    num_shapes = self.numSubShapes
    self.numSubShapes = num_shapes + 1
    self.subShapes.updateSize()
    # add the shape
    self.subShapes[num_shapes].layer = layer
    self.subShapes[num_shapes].numVertices = len(vertices)
    self.subShapes[num_shapes].material = material
    # add the shape data
    if not self.data:
        self.data = self.cls.hkPackedNiTriStripsData()
    data = self.data
    data.numTriangles = len(triangles)
    data.triangles.updateSize()
    for tdata, t, n in zip(data.triangles, triangles, normals):
        tdata.triangle.v1 = t[0]
        tdata.triangle.v2 = t[1]
        tdata.triangle.v3 = t[2]
        tdata.normal.x = n[0]
        tdata.normal.y = n[1]
        tdata.normal.z = n[2]
    data.numVertices = len(vertlist)
    data.vertices.updateSize()
    for vdata, v in zip(data.vertices, vertices):
        vdata.x = v[0] / 7.0
        vdata.y = v[1] / 7.0
        vdata.z = v[2] / 7.0

