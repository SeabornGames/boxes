#!/usr/bin/env python3
# Copyright (C) 2013-2018 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *


class ModelHome(Boxes):
    """Model of a home from a layout file"""

    ui_group = "Layout"

    def __init__(self):
        Boxes.__init__(self)
        self.addSettingsArgs(boxes.edges.FingerJointSettings)
        self.addSettingsArgs(boxes.edges.FlexSettings)
        self.buildArtParser("diagram_file", "wall_file",
                            "wall_height", "window_bottom", "window_top",
                            "door", "filter_room", "exclude_room", "scale")
        self.argparser.add_argument('--diagram-file', default=None,
                                    help='Path to the diagram file.  If this'
                                         ' file is not provided then'
                                         ' floors will not be generated.')
        self.argparser.add_argument('--wall-file', default=None,
                                    help='Path to the wall file.  If this'
                                         ' file is not provided then'
                                         ' walls will not be generated.')
        self.argparser.add_argument('--wall-height', type=float, default=10.0,
                                    help='default height of the walls')
        self.argparser.add_argument('--window-bottom', type=float, default=2,
                                    help='default height of the bottom of the'
                                         ' windows')
        self.argparser.add_argument('--window-top', type=float, default=7,
                                    help='default height of the top of the'
                                         ' windows')
        self.argparser.add_argument('--door', type=float, default=9,
                                    help='default height of the doors')
        self.argparser.add_argument('--filter-room', default=None, nargs='+',
                                    help='Only generate walls and floors for'
                                         ' these rooms.')
        self.argparser.add_argument('--exclude-room', default=None, nargs='+',
                                    help='Exclude these rooms from generating'
                                         ' walls and floors.')
        self.argparser.add_argument('--scale', default=0.1, type=float,
                                    help='number of inches in the model for'
                                         ' every foot in the diagram.')

    def render(self):

        x, y = self.x, self.y
        heights = [self.height0, self.height1, self.height2, self.height3]

        if self.outside:
            x = self.adjustSize(x)
            y = self.adjustSize(y)
            for i in range(4):
                heights[i] = self.adjustSize(heights[i], self.bottom_edge,
                                             self.lid)

        t = self.thickness
        h0, h1, h2, h3 = heights
        b = self.bottom_edge

        self.trapezoidWall(x, h0, h1, [b, "F", "e", "F"], move="right")
        self.trapezoidWall(y, h1, h2, [b, "f", "e", "f"], move="right")
        self.trapezoidWall(x, h2, h3, [b, "F", "e", "F"], move="right")
        self.trapezoidWall(y, h3, h0, [b, "f", "e", "f"], move="right")

        with self.saved_context():
            if b != "e":
                self.rectangularWall(x, y, "ffff", move="up")

            if self.lid:
                maxh = max(heights)
                lidheights = [maxh-h for h in heights]
                h0, h1, h2, h3 = lidheights
                lidheights += lidheights
                edges = ["E" if (lidheights[i] == 0.0 and lidheights[i+1] == 0.0) else "f"
                         for i in range(4)]
                self.rectangularWall(x, y, edges, move="up")

        if self.lid:
            self.moveTo(0, maxh+self.edges["F"].spacing()+self.edges[b].spacing()+3*self.spacing, 180)
            self.trapezoidWall(y, h0, h3, "Ffef", move="right" +
                      (" only" if h0 == h3 == 0.0 else ""))
            self.trapezoidWall(x, h3, h2, "FFeF", move="right" +
                      (" only" if h3 == h2 == 0.0 else ""))
            self.trapezoidWall(y, h2, h1, "Ffef", move="right" +
                      (" only" if h2 == h1 == 0.0 else ""))
            self.trapezoidWall(x, h1, h0, "FFeF", move="right" +
                      (" only" if h1 == h0 == 0.0 else ""))
