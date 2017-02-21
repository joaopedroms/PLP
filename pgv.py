#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygraphviz as pgv
from PIL import Image


class UMLDiagram:
    def __init__(self):
        self.Graph = pgv.AGraph(strict=False, directed=True)
        self.Graph.node_attr['shape'] = 'record'
        self.Graph.node_attr['fillcolor'] = '#fdffd8'
        self.Graph.node_attr['style'] = 'filled'
        self.Graph.node_attr['fontname'] = 'calibri'

    def addClass(self, name, attrs, methods):
        line_break = '|'
        align_left = '\l'

        node_def = '{' + name + line_break

        for attr in attrs:
            node_def += attr + align_left

        node_def += line_break

        for method in methods:
            node_def += method + align_left

        node_def += '}'

        self.Graph.add_node(name, label=node_def)

    def display(self):
        self.Graph.layout(prog='dot')
        self.Graph.draw('UMLDiagram.png')
        print self.Graph
        img = Image.open('UMLDiagram.png')
        img.show()

    def addRelationship(self, from_, to, card):
        self.Graph.add_edge(from_, to, color='#0000ff', label=card)

    def addExtension(self, extends, extended):
        self.Graph.add_edge(extends, extended, color='#ff0000')



