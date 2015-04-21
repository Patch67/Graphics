Htis is the Git hub repository for Patrick Biggs.

In here you'll find all my public code.

Notably you'll find the Python libraries and source code f my projects.

Graphics App 1: This app allows a user to open various types of 2D file, edit them, and save them in various ways.

Input Formats Supported
-----------------------
None

Output Formats Supported
------------------------
Text
GCode
DXF - Partial support as of 21/04/2015

Input Formats Proposed
----------------------
SVG
DXF
Gcode

Output Formats Proposed
-----------------------
SVG
PDF

Application Proposal
--------------------
Multi Platform Windowed app - using Python and tkinter
Internal Graphics function provided by Graph.py
Various decorator wrappers for the different output formats...TextGraph.py, DXFGraph.py, Gcode.Graph.py
Undo / redo functionality via Memento pattern.  Need to investigate zippers.

