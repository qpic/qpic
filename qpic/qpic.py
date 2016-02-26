#!/usr/bin/python
#############################################################################
#           Copyright (c) 2013-16, Institute for Defense Analyses           #
#      4850 Mark Center Drive; Alexandria, VA 22311-1882; 703-845-2500      #
#                                                                           #
#This material may be reproduced by or for the US Government pursuant to the#
#copyright license under the clauses at DFARS 252.227-7013 and 252.227-7014.#
#                                                                           #
#         Distributed under GNU General Public License, version 3.          #
#############################################################################

# qpic.py, by Tom Draper and Sandy Kutin

# commands

# basic commands
# name W [labels]
# names W [labels]
#    Declares a wire or wires.  Wires appear on the page in the order in which
#    they are declared.  Recommended usage:  all W lines at start of input.
#    Optional labels appear at beginning and end of wires.  Labels may
#    not contain white space.  Labels will be enclosed in $s.
#   Labels will be used in order; if only an end label is desired, insert
#   a start label of {}.
#   Wires may not start with - or +.  - preceding a wire name denotes a
#    negated control.  + denotes a target where a control would be expected.
#  A wire name starting with  "..." becomes an ellipsis.
#  If a wire with the given name has already been declared, simply add the
#  given labels to the list of labels for that wire.
#  If multiple names are given, labels are drawn across all wires
#  If a wire label starts or ends with < or >, braces are drawn
#
# wires may also be used without being declared, if no 'W' command has been
#  issued or if 'AUTOWIRES' has been used
# a wire name can be of the form "num" or "str[_][nums]", where
#  num is a (nonnegative) integer, str a sequence of lowercase letters, and
#  nums a comma-separated list of nonnegative inetgers.
# if a wire is first used in 'W', we match strings; if not we convert to
#  an integer or a tuple whose first entry is a string.  So, "a_0" and "a00"
#  are the same wire if undeclared, but different wires if declared
# By default, "num" wires have no label, "str[_][nums]" get a starting label
# target T control1 control2
# target C control
# target N
#   Toffoli, CNOT, negation gates.
# controls
#    controlled Z (all wires drawn with conrol).
#   Use + prefix to indicate target for controlled negation

# boxes and ellipses
# target1 target2 ... G name [control list]
# target1 target2 ... G| name [control list]
# target1 target2 ... |G name [control list]
# target1 target2 ...  P name [control list]
#    Boxes with one or more targets.
#    G| draws a slightly thicker line on the forward side; |G on the back.
#   (The side with the thick line is flipped when the gate is reversed.)
#    G draws a rectangle, P a circle/ellipse.  Shapes may be changed (see below)
# G, P, G|, |G each take all targets (since the start of line or the last
#  G, P, G|, |G) and may be combined.  E.g., "target1 G op1 target2 P op2".

# additional gates
# target X [control list]
# target Z [control list]
# target H [control list]
#    Unary operators.
# target1 target2 SWAP
#   swap values on two wires
# target1 target2 ... M [operator]
#   Measure; also changes targets to type=c
#   if operator specified, use D-shaped box; otherwise, use meter
# target1 target2 ... / [name]
#   draw slash on line to indicate wire size (name will be enclosed in $s)
# target IN value
# target OUT value
#   wire drops in or out with specified value (will be enclosed in $s)
# targets START
# targets END
#   targets start or end together, each using their next label
#   (unlike other gates, this cannot be put in a time-slice
#    before the most recent gate)
#
# options (may appear anywhere in line)
# color=????: set color for gate, wire, or level
# length=????: set length (in time dimension) for that gate (also applies to LABEL)
# breadth=????: set breadth (in wire dimension) for that gate
# height=????, width=????: set length or breadth (depending on horizontal/vertical orientation)
# size=????: set breadth and width for G, P gates
#            set target/control diameter for C,N,T,S,SWAP
# operator=????: set operator for target: -,|,+,\\,/,x,X,*,-*,.,0 or char to draw
#   *,-*: for circle/box, * draws 8 lines; otherwise, * draws to corners, -* to sides
#   "...": uses tikz code between quotes; (0,0) refers to center of operator
# shape=????: set shape for target, P, or one-target G:
#   0=none, 1=control, -1=negated control
#   2=circle; for n >=3, n=n-sided poly (flat on bottom), -n=same (point down)
#   (in vertical mode:  n=flat on right, -n=point on right)
# attached to a wire: size, operator, shape apply
# attached to the whole gate: size, operator, shape apply only to the targets
# style=????: style (pass to TikZ; underscores become spaces) for gate, wire, or level
# fill=????: set fill (pass to TikZ)
# hyperlink=????: sets hyperlink (currently works only with G and variants)
# type=????: quantum, classical, or off wire
#            (these can appear only in a W command or to change a wire)
#            first letter: qQ1->quantum; cC2->classical; oO0->off
#            predfined: qwire -> type=q, similar for cwire, owire
# qpic will match prefixes (2+ chars) of options types where possible
#
# Note: for targets, size is diameter, default=6; length, breadth are space
# For P, size is diameter; if not specified, fit shape into given length/breadth
# For G, size is length/breadth.
# 
# : options may be colon-separated instead of space-separated
# colon-separated options following a wire apply changes as of that line
# colon-separated options following G/P or other object apply to that object
# options specified on the line apply to everything
#   (but color, style, length, breadth do not propagate to wires)
#    e.g., length specified on line is passed to G/P
# length specified on G/P is not passed to the whole line, but the default
#   is make the gate long enough to contain all elements
# if a property is specified on line and at object, object value applies
#
# L
# [ % [comment] [% [comment]]
#   specifies one or two comments to gate to be placed on the side
# MARK word1 word2 ...
#   Defines "marks" at this depth for use by @ and R.
# [targets] @ [num1 | mark1 [num2 | mark2]] 
#   range of depths.  No args means d == current;
#                     [num1] means current - num1 < d <= current;
#                     [mark1] means mark1 < d <= current
#                     [num1 num2|mark2] means num1 <= d <= num2/mark2;
#                     [mark1 num2|mark2] means mark1 < d <= num2/mark2
#   if style= and fill= are not set, it does nothing, but lets you attach comments with braces
#   if style= or fill= is set, it draws in the indicated region
#   if targets specified, comments go next to specified wires; default is all wires
#
# Managing depth
# By default, qpic assigns the earliest possible depth to each gate.  Within
# a depth, gates are stacked where possible; each is placed as far to the
# left as it can be.  The following commands help one keep together gates
# which should go together.
# MIXGATES num
#    Sets "allow_different_gates" to num.  When it's 1, different
#    types of gates may coexist at one depth.  Default is 1.
# [wire1 wire2 ...] TOUCH
#    "Touch" the wire(s)--pretend that their depth is that of the most recent
#    gate.  If no argument is given, touch all wires.  If color or style are set,
#   draw a "barrier" between depths
# [wire1 wire2 ...] BARRIER
#   Same as TOUCH, but defaults to drawing a zigzag barrier
# LB
#    Begin a "level".  The gates within the level are all placed at the
#    same depth; no check is done about whether they overlap, or what
#    types of gates they are.  color=/fill=/style= sets default for the level.
# LE
#    End a "level".  Levels may be nested.
# [wire1 wire2 ...] PHANTOM
#    Same as "touch", but applies within a depth; pretend that each
#    wire was touched at the most recent subdepth.  If no target is
#    given, applies to all wires.
# ;
#   Multiple gates may be placed on one line, separated by ;
#   They all appear at the same level (included in a LB/LE)
#   If any "gate" has attributes only, the attributes are attached to the LB
#      and applied to all the gates


# Other commands
# [targets] LABEL label1 label2 ...
#    Inserts labels in the middle of the circuit.  If targets not specified, set to all wires.
#   Number of labels must equal number of wires (or 0 or 1).  Labels will be enclosed in $s.
#   For depth purposes, treated as a single gate touching all wires. "..." becomes "\cdots".
#   If one label is given, repeat it.  If none, we just add space to the circuit.
# [targets] = [label]
#   Like LABEL, but only one (centered) label is used.  Use label if provided, $=$ otherwise.
# [targets] [<,>]=[<,>] [label]
#   Generalization of =.  < or > before and/or after the =
#   draws a curly brace pointing in that direction.
# R [start end]
#   Repeats a section of the circuit, from time start to end.
#   start and end can be numbers or marks (see MARK above).  Default is start=-2, end=0.
#   Negative indices are as in python (i.e., add length).
#   Larger endpoint is included; smaller is included if a number, excluded if a mark.
#   If start >= end, circuit is reversed, otherwise repeated.
# DEPTHPAD num
#    Changes the padding on either side of a depth.  Default is 6 (pt).
# GATESIZE num
#    Changes the length and breadth of each box in the image.  Default is 12 (pt).
# WIREPAD num
#   Changes the extra separation between wires.  Default is 3 (pt).
# CORNERS num
#   Changes rounded corner size when wires bend.  Default is 4 (pt).  0 for no rounding.
# OPACITY num
#   Changes opacity for shaded rectangles.  Default is 0.2.
# COMMENTSIZE num
#   Changes the width of comment boxes.  Default is 144 (pt) (2in).
# WIRES string
#    String to be prepended to each wire command (e.g., \scriptstyle)
# PREMATH string
#  String to be prepended to dollar signs in wire commands
# POSTMATH string
#  String to be appended to dollar signs in wire commands
# PREAMBLE string
#  Line to insert into start of .tex file
# PRETIKZ string
#  Line to insert at start of TikZ environment
# POSTTIKZ string
#  Line to insert at end of TikZ environment
# HYPERTARGET string
#  Inserts \hypertarget{string}{} before TikZ environment
# SCALE multiplier
#   multiplies by an extra factor
# COLOR name r g b
#   Adds new color; also does \definecolor.  0 <= r, g, b <= 1
# CUT [nums] [options]
#    Inserts vertical dashed lines into spaces separating depths.
#   If CUT is followed by numbers, dashed lines appear before those time-slices
#   If no numbers are given, lines are drawn between all time-slices
#   color or style may be specified (default style is "dashed")
#   To determine color/style, use the latest CUT line with that number; if none,
#   use a CUT line with no numbers (if any).
# [args] DEFINE name word1 word2 word3 ...
#    Allows macro definitions; e.g., "A" for "G A" or "red" for "color=red".
#    From then on, if a line contains "name", then "name" is replaced by
#   the string "word1 word2 word3 ...".
#   If n args are present, then the n words preceding "name" will replace the
#   args.  E.g., after "x y DEFINE FOO x ; x y", "a b FOO" -> "a ; a b"
# VERTICAL [deg1 [deg2]]
#   Change orientation to vertical
#   If deg1 is set, use it as angle (in degrees) to rotate start/end labels
#   If deg2 is set, use different ones for start and end
#   0 is horizontal, 90 is vertical; default is 45
# HORIZONTAL
#   Change orientation to horizontal
# MEASURESHAPE shape
#   change shape of measurement to "D" or "tag" (default is D)
# HEADER string
#   Line to insert before \begin{document} in standalone file
# BGCOLOR [color]
#   Change background color (default is white)
#   If no color given, set it to "bg", which works in beamer
# AUTOWIRES
#   Allow undeclared wires (number or lowercase string, optional '_',
#      comma-separated numbers).  Default is 'on' until first 'W' declaration
#
########################################################
# WARNING: no longer allowed (use : syntax)
# wires CHANGE options
# Apply options (e.g., "color=???") to wires as of the most recent gate
#
# WARNING: no longer allowed (apply + to individual "controls")
# G, G|, |G, P, S: if gate name preceded by "+", controls are targets instead

from __future__ import print_function

import sys, string, copy, math, collections, types

def initialize_globals():
    global line_num
    global DEPTH_PAD, GATE_SIZE, BRACE_AMPLITUDE, WIRE_PAD, COMMENT_SIZE
    global wire_prefix, cut_info, premath_str, postmath_str, overall_scale
    global preamble_list, pretikz_list, posttikz_list, predocument_list
    global measure_shape, ROUNDED_CORNERS, OPACITY, allow_different_gates
    global orientation, start_degrees, end_degrees, bgcolor, auto_wires
    global CLASSICAL_SEP, EQUALS, legal_options, BARRIER_STYLE
    global valid_prefixes
    global master_depth_list, overall_depth, last_depth
    global wires, wires_in_order, declared_wires_in_order, level_stack
    global defined_symbols, new_colors, braces_list, depth_marks
    global new_wire_depth

    line_num = 0

    DEPTH_PAD = 6
    GATE_SIZE = 12
    BRACE_AMPLITUDE = 4
    WIRE_PAD = 3
    COMMENT_SIZE = 144
    wire_prefix = ''
    cut_info = {}
    premath_str = ''
    postmath_str = ''
    overall_scale = 1.0
    preamble_list = []
    pretikz_list = []
    posttikz_list = []
    predocument_list = []
    measure_shape = 'D'
    ROUNDED_CORNERS = 4
    OPACITY = 0.2

    allow_different_gates = 1
    orientation = 'horizontal'
    start_degrees = 45
    end_degrees = 45
    bgcolor = 'white'
    # choices: 'off' = disallow; 'on' = allow; 'default' = allow until wire declaration occurs
    auto_wires = 'default'

    CLASSICAL_SEP = 0.5

    EQUALS = []
    for s1 in ['<', '', '>']:
        for s2 in ['<', '', '>']:
            EQUALS.append(s1+'='+s2)

    legal_options = ['color', 'length', 'breadth', 'size', 'width', 'height', 'style', 'fill', 'hyperlink', 'type', 'shape', 'operator']

    BARRIER_STYLE="decorate,decoration={zigzag,amplitude=1pt,segment length=4}"

    valid_prefixes = ['+', '-']

    master_depth_list = []
    overall_depth = 0
    last_depth = 0
    wires = {}
    wires_in_order = []
    declared_wires_in_order = []
    level_stack = []
    defined_symbols = {}
    for c in ['o', 'c', 'q']:
        defined_symbols[c+'wire'] = ([], ['type=%s' % c])
    new_colors = []
    braces_list = []
    depth_marks = {}
    new_wire_depth = -1 # start at depth 0

def add_to_predocument(what):
    global predocument_list
    if what == "decorate":
        the_str = "\\usetikzlibrary{decorations.pathreplacing,decorations.pathmorphing}"
    elif what == "hyperref":
        the_str = "\\usepackage{hyperref}"
    elif what == "bg":
        the_str = "\\definecolor{bg}{rgb}{1,1,1}"
    else:
        sys.exit("Error: unknown predocument item %s (this should never happen)" % what)
    if the_str not in predocument_list:
        predocument_list.append(the_str)

def parse_options(word):
    global legal_options
    # look for =
    pos = 0
    while pos < len(word) and word[pos] != '=':
        if not word[pos].islower():
            return None
        pos += 1
    if pos in [0, len(word), len(word)-1]:
        return None
    opt_string = word[:pos]
    val_string = word[pos+1:]
    # which option was meant?
    if len(opt_string) == 1:
        raise SyntaxError('option specifier %s needs at least two characters' % opt_string)
    possible_options = []
    for opt in legal_options:
        if opt.startswith(opt_string):
            possible_options.append(opt)
    if not possible_options:
        raise SyntaxError('unknown option %s' % opt_string)
    if len(possible_options) > 1:
        raise SyntaxError('ambiguous option %s' % opt_string)
    opt = possible_options[0]
    if opt == 'width':
        if orientation == 'vertical':
            opt = 'breadth'
        else:
            opt = 'length'
    if opt == 'height':
        if orientation == 'vertical':
            opt = 'length'
        else:
            opt = 'breadth'
    if opt in ['color', 'fill', 'hyperlink', 'operator']:
        val = val_string
    elif opt == 'style':
        val = ' '.join(val_string.split('_')) # _ -> space
    elif opt in ['length', 'breadth', 'size']:
        val = float(val_string)
    elif opt == 'type':
        if val_string[0] in ['q', 'Q', '1']:
            val = 'q'
        elif val_string[0] in ['c', 'C', '2']:
            val = 'c'
        elif val_string[0] in ['o', 'O', '0']:
            val = 'o'
        else:
            raise SyntaxError('bad type %s' % val_string)
    elif opt == 'shape':
        if val_string == 'circle':
            val = 2
        elif val_string == 'box':
            val = 4
        else:
            val = int(val_string)
    else:
        raise SyntaxError('unknown option %s (which should never happen)' % opt)
    return {opt:val}

def get_x_y(pos, wire):
    global orientation
    if orientation == 'vertical':
        return (-wire, -pos)
    else:
        return (pos, wire)
    
def get_w_h(length, breadth): # return width, height
    if orientation == 'vertical':
        return (breadth, length)
    else:
        return (length, breadth)
def get_directions():
    if orientation == 'horizontal':
        directions = ['above,text centered', 'below,text centered']
    else:
        directions = ['left,text ragged left', 'right']
    return directions

# loc_or_pos is loc for lengthwise, pos for breadthwise
def draw_brace(start, end, loc_or_pos, delta, color=None, how='length'):
    brace_command = "\\draw[decorate,decoration={brace"
    dir = 1
    # if amplitude is too big, short braces look weird
    amplitude = min(abs(delta),0.25*abs(end-start))
    if (delta < 0):
        dir *= -1
    if orientation == 'vertical':
        dir *= -1
    if how == 'breadth':
        dir *= -1
    if dir == -1:
        brace_command += ",mirror"
    brace_command += ",amplitude = %fpt" % amplitude
    brace_command += "},very thick"
    if color:
        brace_command += ",color=%s" % color
    brace_command += "]"
    if how == 'length':
        brace_command += " (%f,%f)" % get_x_y(start, loc_or_pos)
        brace_command += " -- (%f,%f);" % get_x_y(end, loc_or_pos)
    else:
        brace_command += " (%f,%f)" % get_x_y(loc_or_pos, start)
        brace_command += " -- (%f,%f);" % get_x_y(loc_or_pos, end)        
    print(brace_command)

def draw_breadthwise_brace(start, end, pos, delta, color=None):
    draw_brace(start, end, pos, delta, color, how='breadth')
    
def draw_brace_old(start, end, loc, delta, color=None):
    mid = loc + 0.5*delta
    if color:
        color_string = ",color=%s" % color
    else:
        color_string = ""
    brace_command = "\\draw[very thick%s]" % color_string
    brace_command += " (%f,%f)" % get_x_y(start, loc)
    brace_command += " .. controls (%f,%f)" % get_x_y(start, mid)
    brace_command += " and (%f,%f)" % get_x_y(0.875*start + 0.125*end, mid)
    brace_command += " .. (%f,%f)" % get_x_y(0.75*start + 0.25*end, mid)
    brace_command += " .. controls (%f,%f)" % get_x_y(0.625*start + 0.375*end, mid)
    brace_command += " and (%f,%f)" % get_x_y(0.5*start+0.5*end, mid)
    brace_command += " .. (%f,%f)" % get_x_y(0.5*start + 0.5*end, loc + delta)
    brace_command += " .. controls (%f,%f)" % get_x_y(0.5*start+0.5*end, mid)
    brace_command += " and (%f,%f)" % get_x_y(0.375*start + 0.625*end, mid)
    brace_command += " .. (%f,%f)" % get_x_y(0.25*start + 0.75*end, mid)
    brace_command += " .. controls (%f,%f)" % get_x_y(0.125*start + 0.875*end, mid)
    brace_command += " and (%f,%f)" % get_x_y(end, mid)
    brace_command += ".. (%f,%f);" % get_x_y(end, loc)
    print(brace_command)

def draw_breadthwise_brace_old(start, end, pos, delta, color=None):
    mid = pos + 0.5*delta
    if color:
        color_string = ",color=%s" % color
    else:
        color_string = ""
    brace_command = "\\draw[very thick%s]" % color_string
    brace_command += " (%f,%f)" % get_x_y(pos, start)
    brace_command += " .. controls (%f,%f)" % get_x_y(mid, start)
    brace_command += " and (%f,%f)" % get_x_y(mid, 0.875*start + 0.125*end)
    brace_command += " .. (%f,%f)" % get_x_y(mid, 0.75*start + 0.25*end)
    brace_command += " .. controls (%f,%f)" % get_x_y(mid, 0.625*start + 0.375*end)
    brace_command += " and (%f,%f)" % get_x_y(mid,0.5*start+0.5*end)
    brace_command += " .. (%f,%f)" % get_x_y(pos+delta,0.5*start + 0.5*end)
    brace_command += " .. controls (%f,%f)" % get_x_y(mid,0.5*start+0.5*end)
    brace_command += " and (%f,%f)" % get_x_y(mid,0.375*start + 0.625*end)
    brace_command += " .. (%f,%f)" % get_x_y(mid,0.25*start + 0.75*end)
    brace_command += " .. controls (%f,%f)" % get_x_y(mid,0.125*start + 0.875*end)
    brace_command += " and (%f,%f)" % get_x_y(mid, end)
    brace_command += ".. (%f,%f);" % get_x_y(pos, end)
    print(brace_command)

# shapes: 0 = none, 1 = control, -1 = negated control, 2 = circle,
# otherwise n = num sides (flat down), -n = num sides (flat up)
def get_draw_options(gate_options, wname, default_spec):
    global bgcolor

    draw_options = {}
    wire_options = gate_options['wires'].get(wname,{})
    if 'shape' in wire_options:
        draw_options['shape'] = wire_options['shape']
    else:
        if default_spec == '+':
            spec = '+'
        else:
            spec = wire_options.get('prefix', default_spec)
        if spec == '+':
            draw_options['shape'] = gate_options.get('shape', 2)
        elif spec == '-':
            draw_options['shape'] = -1
        else:
            draw_options['shape'] = 1
    if draw_options['shape'] == 1: # control
        default_size = 3
    elif draw_options['shape'] == -1: # negated_control
        default_size = 4.5
    else:
        default_size = gate_options.get('size', 6) # xor
    draw_options['size'] = wire_options.get('size', default_size)
    draw_options['operator'] = wire_options.get('operator', gate_options.get('operator', '+'))
    draw_options['fill'] = wire_options.get('fill', bgcolor)
    return draw_options

# horizontal start is smallest vertex (indicated by angle) in range [-90, 270]
# our goal is to flip this; equivalently, rotate by 90 degrees
def find_vertical_start(horizontal_start, num_sides):
    horizontal_angles = []
    vertical_start = horizontal_start + 90 # first candidate is starting point
    for i in range(1, num_sides):
        angle = horizontal_start + 90 + (i*360.0/num_sides)
        if angle >= 270: # found a better candidate after looping around
            vertical_start = angle - 360
            break
    return vertical_start

def calculate_diameter(in_len, in_bre, in_size, shape, allow_breadth_shift=0):
    global orientation

    if shape > 2 or shape < -2:
        if shape > 2:
            num_sides = shape
            start=-90+360.0/(2*num_sides)
        else:
            num_sides = -shape
            start = -90
        if orientation == 'vertical':
            start = find_vertical_start(start, num_sides)
        angles = []
        for i in range(0, num_sides):
            angles.append(start + (i*360.0/num_sides))
        width_ratio = max([math.fabs(math.cos(a*2*math.pi/360)) for a in angles])
        height_ratio = max([math.fabs(math.sin(a*2*math.pi/360)) for a in angles])
        if orientation == 'vertical':
            breadth_ratio = width_ratio
            length_ratio = height_ratio
        else:
            breadth_ratio = height_ratio
            length_ratio = width_ratio
        if allow_breadth_shift:
            if orientation == 'vertical':
                locations = [math.cos(a*2*math.pi/360) for a in angles]
            else:
                locations = [math.sin(a*2*math.pi/360) for a in angles]
            min_loc = min(locations)
            max_loc = max(locations)
            breadth_shift = (max_loc + min_loc)/2 # subtract this from the location
            if orientation == 'vertical':
                breadth_shift *= -1 # because positive location is +x, not -y
            breadth_ratio = (max_loc - min_loc)/2
        else:
            breadth_shift = 0
    else:
        breadth_ratio = 1
        length_ratio = 1
        breadth_shift = 0
    if in_size:
        diameter = in_size
    else:
        if in_len != None and in_bre != None:
            diameter = max(in_len/length_ratio, in_bre/breadth_ratio)
        elif in_len != None:
            diameter = in_len/length_ratio
        elif in_bre != None:
            diameter = in_bre/breadth_ratio
        else:
            default_size = GATE_SIZE # used to be GATE_SIZE + WIRE_PAD
            # fit in a box that default_size by default_size
            diameter = default_size / max(length_ratio, breadth_ratio)
    if in_len == None:
        length = diameter * length_ratio
    else:
        length = in_len
    if in_bre == None:
        breadth = diameter * breadth_ratio
    else:
        breadth = in_bre
    return (length, breadth, diameter, breadth_shift)

def write_operator_name(x,y,operator):
    if operator[0] == '"':
        if operator[-1] != '"':
            operator += '"'
        operator_str = operator[1:-1]
        print("\\begin{scope}[shift={(%f,%f)}]" % (x,y))
        print(operator_str)
        print("\\end{scope}")
    else:
        print("\\draw (%f, %f) node {%s};" % (x,y,operator))

def draw_xor(x,y,options):
    global orientation, bgcolor
    if isinstance(options['size'], tuple):
        xradius = 0.5*options['size'][0]
        yradius = 0.5*options['size'][1]
        circle_str = 'ellipse'
        arc_str = '%fpt and %fpt' % (xradius, yradius)
    else:
        xradius = 0.5*options['size']
        yradius = xradius
        circle_str = 'circle'
        arc_str = '%fpt' % xradius
    shape = options['shape']
    operator = options['operator']
    fillcolor = options.get('fill',bgcolor)
    thick_side = options.get('thick_side',0)
    print("\\begin{scope}")
    if shape == 2:
        shape_line = "(%f, %f) %s(%s);" % (x,y,circle_str,arc_str)
        num_sides = 0
        if thick_side:
            if thick_side == 1:
                if orientation == 'vertical':
                    theta = -180
                else:
                    theta = -90
            elif orientation == 'vertical':
                theta = 0
            else:
                theta = 90
            thick_line = "(%f, %f) +(%f:%s) arc (%f:%f:%s);" % (x,y,theta,arc_str,theta,theta+180,arc_str)
        else:
            thick_line = ""
    elif shape > 2 or shape < -2:
        shape_line_start = "(%f, %f) " % (x,y)
        quadrants = [[],[],[],[]]
        points = [] 
        if shape > 2:
            num_sides = shape
            start=-90 + 360.0/(2*num_sides)
        else:
            num_sides = -shape
            start=-90
        if orientation == 'vertical':
            start = find_vertical_start(start, num_sides)
        for i in range(0, num_sides):
            angle = start + (i*360.0/num_sides)
            point_str = "+(%f:%s)" % (angle,arc_str)
            points.append(point_str)
            if angle <= 0:
                quadrants[0].append(point_str)
            if 0 <= angle and angle <= 90:
                quadrants[1].append(point_str)
            if 90 <= angle and angle <= 180:
                quadrants[2].append(point_str)
            if 180 <= angle:
                quadrants[3].append(point_str)
        shape_line = shape_line_start + " -- ".join(points) + " -- cycle;"
        if thick_side:
            if start == -90:
                quadrants[3].append("+(%f:%s)" % (start,arc_str))
            if thick_side == 1:
                if orientation == 'vertical':
                    thick_points = quadrants[3] + quadrants[0]
                else:
                    thick_points = quadrants[0] + quadrants[1]
            elif orientation == 'vertical':
                thick_points = quadrants[1] + quadrants[2]
            else:
                thick_points = quadrants[2] + quadrants[3]
            thick_line = shape_line_start + " -- ".join(thick_points) + ";"
        else:
            thick_line = ""
        #print(shape_line)
    else:
        shape_line = ""
        num_sides = 0
        thick_line = ""
    if shape_line:
        print(("\\draw[fill=%s] " % fillcolor) + shape_line);
        if thick_line:
            print("\\draw[very thick,solid] " + thick_line)
        print("\\clip " + shape_line);
    if operator in ['+', '-', '|', 'x', 'X', '/', '\\\\', '*', '0', '-*']:
        if operator in ['-', '+'] or (operator=='*' and num_sides in [-4,0,4]):
            print("\\draw (%f, %f) -- (%f, %f);" % (x-xradius,y,x+xradius,y))
        if operator in ['|', '+'] or (operator=='*' and num_sides in [-4,0,4]):
            print("\\draw (%f, %f) -- (%f, %f);" % (x,y-yradius,x,y+yradius))
        if operator in ['/', '\\\\', 'x', 'X'] or (operator=='*' and num_sides in [-4,0,4]):
            xh = xradius*math.sqrt(.5)
            yh = yradius*math.sqrt(.5)
            if operator != '\\\\':
                print("\\draw (%f, %f) -- (%f, %f);" % (x-xh,y-yh,x+xh,y+yh))
            if operator != '/':
                print("\\draw (%f, %f) -- (%f, %f);" % (x-xh,y+yh,x+xh,y-yh))
        if operator == '*' and num_sides not in [-4,0,4]:
            for i in range(0, num_sides):
                print("\\draw (%f, %f) -- +(%f:%s);" % (x,y,start+i*(360.0/num_sides),arc_str))
        if operator == '-*' and num_sides not in [-4,0,4]:
            for i in range(0, num_sides):
                print("\\draw (%f, %f) -- +(%f:%s);" % (x,y,start+(i+0.5)*(360.0/num_sides),arc_str))
    else:
        if operator == '.':
            print("\\filldraw (%f, %f) circle(%fpt);" % (x,y,.25))
        else:
            write_operator_name(x,y,operator)
    print("\\end{scope}")
    
def draw_control(x,y,size):
    print("\\filldraw (%f, %f) circle(%fpt);" % (x,y,0.5*size))
def draw_negated_control(x,y,size):
    global bgcolor
    print("\\draw[fill=%s] (%f, %f) circle(%fpt);" % (bgcolor,x,y,0.5*size))
def draw_xor_or_control(x,y,options):
    if options['shape'] == 1:
        draw_control(x,y,options['size'])
    elif options['shape'] == -1:
        draw_negated_control(x,y,options['size'])
    else:
        draw_xor(x,y,options)

def draw_rectangle(x,y,dx,dy,name,style=None,fill='bgcolor'):
    global bgcolor
    if fill == 'bgcolor':
        fill = bgcolor
    tikz_str = 'fill=%s' % fill
    if style:
        tikz_str += ',' + style
    print("\\draw[%s] (%f, %f) rectangle (%f, %f);" % (tikz_str,x-0.5*dx,y-0.5*dy,x+0.5*dx,y+0.5*dy))
    if name:
        print("\\draw (%f, %f) node {%s};" % (x,y,name))
def draw_slash(x,y,dx,dy,name=None,style=None):
    global orientation
    if style:
        style_str = '[%s]' % style
    else:
        style_str = ''
    if orientation == 'vertical':
        print("\\draw%s (%f, %f) -- (%f, %f);" % (style_str, x-0.5*dx, y-0.5*dy, x+0.5*dx, y+0.5*dy))
        if name:
            print("\\draw%s (%f, %f) node[below] {$\\scriptstyle{%s}$};" % (style_str,x+0.25*dx,y-0.25*dy,name))
    else:
        print("\\draw%s (%f, %f) -- (%f, %f);" % (style_str, x-0.5*dx, y-0.5*dy, x+0.5*dx, y+0.5*dy))
        if name:
            print("\\draw%s (%f, %f) node[right] {$\\scriptstyle{%s}$};" % (style_str,x+0.25*dx,y+0.25*dy,name))
        
def draw_equals(x,y,dx,dy,name):
    global bgcolor
    draw_rectangle(x,y,dx,dy,name,style='color=%s'%bgcolor,fill=bgcolor)

def draw_meter(x,y,dx,dy,style=None,fill='bgcolor'):
    global bgcolor
    if fill == 'bgcolor':
        fill = bgcolor
    draw_rectangle(x,y,dx,dy,None,style=style,fill=fill)
    # center of arc at x,z; radius is r.  Need r <= dx/2.
    # need x-z, x-z+r in box, so also
    radius = min(0.5*dx, 0.5*dy)
    if style:
        style_str = ',' + style
    else:
        style_str = ''
    print("\\draw[very thin%s] (%f, %f) arc (90:150:%fpt);" % (style_str,x,y-.45*dy+radius,radius))
    print("\\draw[very thin%s] (%f, %f) arc (90:30:%fpt);" % (style_str,x,y-.45*dy+radius,radius))
    print("\\draw[->,>=stealth%s] (%f, %f) -- +(%i:%fpt);" % (style_str,x, y-.45*dy, 80, radius*math.sqrt(3)))

def draw_measure_D(x,y,dx,dy,name,style=None,fill='bgcolor'):
    global bgcolor
    if fill == 'bgcolor':
        fill = bgcolor
    tikz_str = 'fill=%s' % fill
    if style:
           tikz_str += ',' + style
    if orientation == 'vertical':
        print("\\draw[%s] (%f, %f) -- (%f,%f) arc (-180:0:%fpt) -- (%f,%f) -- cycle;" % (tikz_str,x-0.5*dx,y+0.5*dy,x-0.5*dx,y+0.5*(dx-dy),0.5*dx,x+0.5*dx,y+0.5*dy))
    else:
        print("\\draw[%s] (%f, %f) -- (%f,%f) arc (-90:90:%fpt) -- (%f,%f) -- cycle;" % (tikz_str,x-0.5*dx,y-0.5*dy,x+0.5*(dx-dy),y-0.5*dy,0.5*dy,x-0.5*dx,y+0.5*dy))
    write_operator_name(x,y,name)

def draw_measure_tag(x,y,dx,dy,name,style=None,fill='bgcolor'):
    global bgcolor
    if fill == 'bgcolor':
        fill = bgcolor
    tikz_str = 'fill=%s' % fill
    if style:
        tikz_str += ',' + style
    if orientation == 'vertical':
        print("\\draw[%s] (%f, %f) -- (%f,%f) -- (%f,%f) -- (%f, %f) -- (%f, %f) -- cycle;" % (tikz_str,x,y+0.5*(dy+dx),x+0.5*dx,y+0.5*dy,x+0.5*dx,y-0.5*dy,x-0.5*dx,y-0.5*dy,x-0.5*dx,y+0.5*dy))
    else:
        print("\\draw[%s] (%f, %f) -- (%f,%f) -- (%f,%f) -- (%f, %f) -- (%f, %f) -- cycle;" % (tikz_str,x-0.5*(dx+dy),y,x-0.5*dx,y+0.5*dy,x+0.5*dx,y+0.5*dy,x+0.5*dx,y-0.5*dy,x-0.5*dx,y-0.5*dy))
    write_operator_name(x,y,name)

def draw_measurement(x,y,dx,dy,name=None,style=None,fill='bgcolor'):
    global measure_shape, bgcolor
    if fill == 'bgcolor':
        fill = bgcolor
    if not name:
        draw_meter(x,y,dx,dy,style=style,fill=fill)
    elif measure_shape == 'TAG':
        draw_measure_tag(x,y,dx,dy,name,style=style,fill=fill)
    else:
        draw_measure_D(x,y,dx,dy,name,style=style,fill=fill)
        
def draw_drop(x,y,dx,dy,name,dir,style=None):
    global bgcolor
    print("\\filldraw[color=%s] (%f, %f) rectangle (%f, %f);" % (bgcolor,x-0.5*dx, y-0.5*dy, x+0.5*dx, y+0.5*dy))
    if style:
        style_str = '[%s]' % style
    else:
        style_str = ''
    if orientation == 'vertical':
        line_pos = y - 0.5*dy*dir
        print("\\draw%s (%f, %f) -- (%f, %f);" % (style_str,x-0.5*dx, line_pos, x+0.5*dx, line_pos))
    else:
        line_pos = x + 0.5*dx*dir
        print("\\draw%s (%f, %f) -- (%f, %f);" % (style_str,line_pos, y-0.5*dy, line_pos, y+0.5*dy))
    print("\\draw%s (%f, %f) node {$\\scriptstyle{%s}$};" % (style_str,x,y,name))
    
def draw_comment(comment,x,y,direction,color=None):
    instructions=direction
    if color:
        instructions += ',color=%s'%color
    if not comment:
        return
    print("\\draw (%f, %f) node[text width=%spt,%s] {%s};" % (x,y,COMMENT_SIZE,instructions,comment))

def draw_highlight_region(corner1,corner2,options):
    fill_opacity = OPACITY
    if options.get('color', None):
        draw_opacity = 1
    else:
        draw_opacity = 0
    tikz_str = "draw opacity=%f,fill opacity=%f" % (draw_opacity, fill_opacity)
    if options.get('color', None):
        tikz_str += ",color=%s" % options['color']
    if options.get('fill', None):
        tikz_str += ",fill=%s" % options['fill']
    if options.get('style', None):
        tikz_str += "," + options['style']
    print("\\draw[%s] (%f,%f) rectangle (%f,%f);" % ((tikz_str,) + corner1 + corner2))

def make_scope_str(color=None,style=None):
    opts = []
    if color:
        opts.append("color=%s" % color)
    if style:
        opts.append(style)
    return ",".join(opts)

class Depth:
    def __init__(self, depth_to_copy=None, direction=1):
        self.depth_to_copy = depth_to_copy
        self.direction = direction
        self.gate_list = []

    def add_gate(self, gate):
        self.gate_list.append(gate)
    def add_gate_list(self, gate_list):
        self.gate_list.extend(gate_list)
        
    def get_type(self):
        if not self.gate_list:
            return None
        return self.gate_list[0].match_type

    def set_boundaries(self, start, end):
        self.start_position = start
        self.end_position = end

    def copy_gates(self, start_pos):
        global master_depth_list
        source = master_depth_list[self.depth_to_copy]
        for g in source.gate_list:
            (old_pos, old_dir) = g.position_list[0]
            if self.direction == 1:
                distance = old_pos - source.start_position
            else:
                distance = source.end_position - old_pos
            g.set_position(start_pos + distance, self.direction)
        end_pos = start_pos + (source.end_position - source.start_position)
        self.set_boundaries(start_pos, end_pos)
        return end_pos

class WireLabel:
    def __init__(self, text, count):
        self.text = text
        self.num_wires = count
        self.positions_seen = []
        self.tops_seen = []
        self.wires_seen = []
        self.bottoms_seen = []
        self.colors_seen = []
        self.info_seen = [] # left/right, etc.
        self.ready = 0
        if count == 0: # should not occur
            sys.exit("Error: somehow no wires for label %s\n" % text)
        if self.text[0] in ['<', '>']:
            self.start_brace = self.text[0]
            self.text = self.text[1:]
            add_to_predocument("decorate")
        else:
            self.start_brace = ''
        if self.text[-1] in ['<', '>']:
            self.end_brace = self.text[-1]
            self.text = self.text[:-1]
            add_to_predocument("decorate")
        else:
            self.end_brace = ''
    def register(self, pos, loc, breadth, color, info):
        self.positions_seen.append(pos)
        self.tops_seen.append(loc + 0.5*breadth)
        self.wires_seen.append(loc)
        self.bottoms_seen.append(loc - 0.5*breadth)
        self.colors_seen.append(color)
        self.info_seen.append(info)
        if len(self.positions_seen) == self.num_wires:
            self.ready = 1
            
    def is_ready(self):
        return self.ready

    def draw_label(self):
        global orientation, premath_str, wire_prefix, postmath_str, bgcolor
        
        if not self.ready: # should not occur
            sys.exit("Error: label %s is not ready\n")

        # check consistency, figure out position/location
        for i in range(1, len(self.positions_seen)):
            if self.positions_seen[i] != self.positions_seen[0]:
                sys.exit("Error: inconsistent positions for label %s\n" % self.text)
            if self.info_seen[i] != self.info_seen[0]:
                sys.exit("Error: inconsistent start/end for label %s\n" % self.text)
        pos = self.positions_seen[0]
        (lr, ab, ns, ew, shift, angle, tikz_str, gate_length) = self.info_seen[0]
        max_loc = max(self.tops_seen)
        min_loc = min(self.bottoms_seen)
        loc = 0.5*(min_loc + max_loc)
        # draw braces
        delta = BRACE_AMPLITUDE
        adjust = 0.75 * WIRE_PAD
        brace_max = 0.5*(max_loc + max(self.wires_seen))
        brace_min = 0.5*(min_loc + min(self.wires_seen))
        if self.start_brace:
            if lr == "left": # starting label; pos is ending edge
                if gate_length == None:
                    brace_pos = pos - GATE_SIZE - delta
                else:
                    brace_pos = pos - gate_length
                    gate_length -= delta
            else: # ending label; pos is starting edge
                brace_pos = pos
                pos += delta
                if gate_length != None:
                    gate_length -= delta
            print("\\filldraw[color=%s,fill=%s] (%f,%f) rectangle (%f,%f);" % ((bgcolor,bgcolor) + get_x_y(brace_pos, brace_min) + get_x_y(brace_pos+delta,brace_max)))
            if self.start_brace == '<':
                draw_breadthwise_brace(brace_min, brace_max, brace_pos + delta, -delta)
            else:
                draw_breadthwise_brace(brace_min, brace_max, brace_pos, delta)
        if self.end_brace:
            if lr == "left": # starting label; pos is ending edge
                brace_pos = pos
                pos -= delta
                if gate_length != None:
                    gate_length -= delta
            else: # ending label; pos is starting edge
                if gate_length == None:
                    brace_pos = pos + GATE_SIZE + delta
                else:
                    brace_pos = pos + gate_length
                    gate_length -= delta
            print("\\filldraw[color=%s,fill=%s] (%f,%f) rectangle (%f,%f);" % ((bgcolor,bgcolor) + get_x_y(brace_pos, brace_min) + get_x_y(brace_pos-delta,brace_max)))
            if self.end_brace == '<':
                draw_breadthwise_brace(brace_min, brace_max, brace_pos, -delta)
            else:
                draw_breadthwise_brace(brace_min, brace_max, brace_pos - delta, delta)
        if gate_length == None: # draw box to fill with bgcolor
            gate_length = 0
        if self.num_wires > 1:
            shift = "0pt" # shifting doesn't look right
        # draw the label
        command = "\\draw[color=%s] " % self.colors_seen[0]
        command += "(%f,%f) " % get_x_y(pos,loc)
        rotate_me = 0
        command += "node[" # add "draw," for debugging
        if tikz_str:
            bg_command = command + tikz_str + ","
            if orientation == 'horizontal':
                breadth_word = 'height'
                length_word = 'width'
                bg_command += "%s," % lr
            else:
                breadth_word = 'width'
                length_word = 'height'
                bg_command += "%s," % ab
            bg_command += "minimum %s=%fpt," % (breadth_word,max_loc-min_loc)
            bg_command += "minimum %s=%fpt," % (length_word,gate_length)
            if self.text == "...":
                if orientation == 'horizontal':
                    math_text = "\\;\\vdots\\;"
                    bg_command += "anchor = base,"
                else:
                    math_text = "\\cdots"
            else:
                math_text = self.text
            bg_command += "inner sep=0pt] "
            bg_command += "{\\phantom{%s$%s%s$%s}};" % (premath_str,wire_prefix,math_text,postmath_str)
            print(bg_command)
        #command += tikz_str + ","
        if self.text == "...":
            if orientation == 'horizontal':
                command += "anchor=mid %s] {%s$%s\\vdots$%s}" % (ew,premath_str,wire_prefix,postmath_str)
            else:
                command += "%s] {%s$%s\\cdots%s$}" % (ab,premath_str,wire_prefix,postmath_str)
        else:
            if orientation == 'horizontal':
                command += "%s" % lr
            elif angle == 0:
                command += "%s" % ab
            elif angle == 90:
                command += "%s,anchor=%s,inner sep=0pt" % (ab, ew)
                rotate_me = 1
            else:
                command += "%s,anchor=%s %s,xshift=%s,inner sep=0pt" % (ab, ns, ew, shift)
                rotate_me = 1
            if rotate_me:
                command += ",rotate=%i" % (0 - angle)
            command += "] {%s$%s%s$%s}" % (premath_str,wire_prefix,self.text,postmath_str)
        command += ";"
        print(command)

def string_to_descriptor(name):
    # allow number -> ('', number)
    if name.isdigit():
        return int(name)
    # find initial string of lowercase letters
    str_end = 0
    bad_descriptor = 0
    while str_end < len(name) and name[str_end].islower():
        str_end += 1
    if not str_end: # should be at least one letter
        bad_descriptor = 1
    else:
        descriptor_list = [name[:str_end]]
        # ignore '_' if it occurs
        if str_end < len(name) and name[str_end] == '_':
            str_end += 1
        # the rest should be comma-separated numbers
        if str_end < len(name):
            numstrs = name[str_end:].split(',')
            for n in numstrs:
                if n.isdigit():
                    descriptor_list.append(int(n))
                else:
                    bad_descriptor = 1
    if bad_descriptor:
        return None
    else:
        return tuple(descriptor_list)

def descriptor_to_tex(desc):
    if not isinstance(desc,tuple):
        return None
    texstr = desc[0]
    if len(desc) > 1:
        texstr += "_{"
        texstr += ",".join(["%i" % n for n in list(desc)[1:]])
        texstr += "}"
    return texstr

def get_wire_for_W(name):
    if name in wires:
        the_wire = wires[name]
    else:
        desc = string_to_descriptor(name)
        if desc in wires:
            the_wire = wires[desc]
        else:
            the_wire = None
    return the_wire

class Wire:
    def __init__(self, name, starting_depth, labels, options):
        self.name = name
        self.depth = starting_depth
        self.labels = copy.copy(labels)
        self.ellipsis = 0
        if isinstance(self.name,str) and self.name.startswith('...'):
            self.ellipsis = 1
        start_color = options.get('color', 'black') # default = black
        self.color_info = {}
        self.color_info[0] = start_color
        start_style = options.get('style', None)
        self.style_info = {}
        self.style_info[0] = start_style
        if self.ellipsis:
            default_start_type = 'o'
        else:
            default_start_type = 'q'
        start_type = options.get('type', default_start_type)
        self.type_info = {}
        self.type_info[0] = start_type
        self.input_line = current_input_line
        self.input_line_num = line_num
        self.start_at_start_of_circuit = 1
        self.explicit_end_seen = 0
        self.last_start_end = ''
        self.last_start_end_pos = -1
        self.specified_breadth = options.get('breadth', None)
        self.location_info = {}
        self.corners = []

    def __str__(self):
        return self.name.__str__()
    
    def get_color(self, pos):
        pos_to_use = 0
        for start in list(self.color_info.keys()):
            if start <= pos and start > pos_to_use:
                pos_to_use = start
        return self.color_info[pos_to_use]

    def get_style(self, pos):
        pos_to_use = 0
        for start in list(self.style_info.keys()):
            if start <= pos and start > pos_to_use:
                pos_to_use = start
        return self.style_info[pos_to_use]

    def get_type(self, pos):
        pos_to_use = 0
        for start in list(self.type_info.keys()):
            if start <= pos and start > pos_to_use:
                pos_to_use = start
        return self.type_info[pos_to_use]

    def change_color(self, pos, color):
        self.color_info[pos] = color

    def change_style(self, pos, style):
        self.style_info[pos] = style

    def change_type(self, pos, wire_type):
        self.type_info[pos] = wire_type

    def add_corner(self, pos):
        self.corners.append(pos)
        
    def get_depth(self):
        return self.depth
    def set_depth(self, d):
        if self.depth < d:
            self.depth = d

    def get_breadth(self):
        global GATE_SIZE, WIRE_PAD
        if self.specified_breadth != None:
            return self.specified_breadth
        return GATE_SIZE + WIRE_PAD
    
    def set_location(self, loc, pos=0):
        self.location_info[pos] = loc

    # what is location of the wire at position pos in the circuit?
    def location(self, pos):
        pos_to_use = 0
        for start in list(self.location_info.keys()):
            if start <= pos and start > pos_to_use:
                pos_to_use = start
        return self.location_info[pos_to_use]
    
    def touch(self, the_depth): # pretend wire was touched by the last gate
        self.set_depth(the_depth)

    def get_next_label(self):
        if self.labels:
            l = self.labels.pop(0)
            return l
        if self.ellipsis:
            return WireLabel("...",1)
        return None

    def add_labels(self, labels):
        self.labels.extend(labels)
        
    def draw_label(self, pos, text, tikz_str):
        if self.get_type(pos) == 'o': # not a real wire
            return
        if not text:
            return
        (x,y) = get_x_y(pos, self.location(pos))
        print("\\draw[color=%s] (%f, %f) node [%s] {%s$%s%s$%s};" % (self.get_color(pos),x,y,tikz_str,
                                                                     premath_str, wire_prefix, text, postmath_str))

    def draw_side_label(self, pos, lr, ab, ns, ew, shift, angle, tikz_str, length):
        label = self.get_next_label()
        if not label:
            return
        label.register(pos, self.location(pos), self.get_breadth(), self.get_color(pos), (lr, ab, ns, ew, shift, angle, tikz_str, length))
        if not label.is_ready():
            print ("%%   Deferring wire label at (%f,%f)" % get_x_y(pos,self.location(pos)))
            return
        label.draw_label()

    def draw_start_label(self, pos, tikz_str=None,length=None):
        self.draw_side_label(pos, "left", "above", "south", "east", "2pt", start_degrees, tikz_str, length)
        if pos > self.last_start_end_pos:
            self.last_start_end_pos = pos
            self.last_start_end = 'start'
            
    def draw_end_label(self, pos, tikz_str=None,length=None):
        self.draw_side_label(pos, "right", "below", "north", "west", "-2pt", end_degrees, tikz_str, length)
        if pos > self.last_start_end_pos:
            self.last_start_end_pos = pos
            self.last_start_end = 'end'

    def end_at_end_of_circuit(self):
        if self.last_start_end == 'end':
            return 0
        else:
            return 1
    
    def draw_wire(self, wirelen):
        transitions = list(self.color_info.keys())
        for k in list(self.style_info.keys()):
            if k not in transitions:
                transitions.append(k)
        for k in list(self.type_info.keys()):
            if k not in transitions:
                transitions.append(k)
        for k in list(self.location_info.keys()):
            if k not in transitions:
                transitions.append(k)
        transitions.sort()
        transitions.append(wirelen)
        print(self.input_line)
        for i in range(len(transitions) - 1):
            tikz_str = 'color=%s' % self.get_color(transitions[i])
            style_str = self.get_style(transitions[i])
            wire_type = self.get_type(transitions[i])
            start_loc = self.location(transitions[i])
            end_loc = self.location(transitions[i+1])
            if wire_type == 'o':
                continue
            if style_str:
                tikz_str += "," + style_str
            if wire_type == 'c':
                start_locs = [start_loc-CLASSICAL_SEP, start_loc+CLASSICAL_SEP]
                end_locs = [end_loc-CLASSICAL_SEP, end_loc+CLASSICAL_SEP]
            else: # wire_type == 'q'
                start_locs = [start_loc]
                end_locs = [end_loc]
            # check for corners -- cannot have other changes at corners
            if transitions[i+1] in self.corners:
                if transitions[i] in self.corners:
                    # continue commands
                    for l in range(len(start_locs)):
                        command_stubs[l] += " -- (%f,%f)" % get_x_y(transitions[i+1], end_locs[l])
                else:
                    # start commands
                    command_stubs = []
                    for l in range(len(start_locs)):
                        command_stubs.append("\\draw[%s,rounded corners=%fpt] (%f,%f) -- (%f,%f)" % ((tikz_str,ROUNDED_CORNERS) +
                                                                                get_x_y(transitions[i], start_locs[l]) +
                                                                                get_x_y(transitions[i+1], end_locs[l])))
            elif transitions[i] in self.corners:
                # end commands
                for l in range(len(start_locs)):
                    print(command_stubs[l] + " -- (%f,%f);" % get_x_y(transitions[i+1], end_locs[l]))
            else:
                for l in range(len(start_locs)):
                    print("\\draw[%s] (%f,%f) -- (%f,%f);" % ((tikz_str,) +
                                                              get_x_y(transitions[i], start_locs[l]) +
                                                              get_x_y(transitions[i+1], end_locs[l])))
        # draw labels in using color info
        if self.start_at_start_of_circuit:
            self.draw_start_label(0)
        
    def fix_wire(self, pos1, pos2, tikz_str=None):
        big_tikz_str = "color=%s" % self.get_color(pos1)
        if tikz_str:
            big_tikz_str += "," + tikz_str
        style_str = self.get_style(pos1)
        if style_str:
            big_tikz_str += "," + style_str
        wire_type = self.get_type(pos1)
        wire_loc = self.location(pos1)
        if wire_type == 'o':
            return
        if wire_type == 'c':
            locs = [wire_loc-CLASSICAL_SEP, wire_loc+CLASSICAL_SEP]
        else:
            locs = [wire_loc]
        for sub_loc in locs:
            print("\\draw[%s] (%f, %f) -- (%f, %f);" % ((big_tikz_str,) + get_x_y(pos1, sub_loc) +
                                                        get_x_y(pos2, sub_loc)))

# one "rectangle" (or other shape)
class Box:
    def __init__(self, box_type, targets, name, options={}):
        global level_stack, orientation, bgcolor
        self.type = box_type
        self.options = copy.deepcopy(options)
        if self.type == 'G|':
            self.type = 'G'
            self.thick_side = 1
        elif self.type == '|G':
            self.type = 'G'
            self.thick_side = -1
        else:
            self.thick_side = 0
        self.name = name
        # remove duplicates
        self.targets = []
        for wn in targets:
            if wn not in self.targets:
                self.targets.append(wn)
        if not self.targets:
            sys.exit("Error:  Line %i: %s needs at least one target\n" % (lin_num, box_type)) 
        if level_stack:
            default_color = level_stack[-1]['color']
            default_style = level_stack[-1]['style']
            default_fill = level_stack[-1]['fill']
        else:
            default_color = None
            default_style = None
            default_fill = bgcolor
        self.color = options.get('color', default_color)
        self.style = options.get('style', default_style)
        self.fill = options.get('fill', default_fill)
        self.options['color'] = self.color
        self.options['style'] = self.style
        self.options['fill'] = self.fill
        length = options.get('length', None)
        breadth = options.get('breadth', None)
        size = options.get('size', None)
        if self.type == 'P':
            if 'shape' not in self.options:
                self.options['shape'] = 2 # circle
            # calculate size; breadth_shift will not be used
            (length, breadth, self.size, breadth_shift) = calculate_diameter(length, breadth, size, self.options['shape'])
        else: # self.type == 'G'
            if 'shape' not in self.options:
                self.options['shape'] = 4 # box
            if size:
                if (length == None) or (length < size):
                    length = size
                if (breadth == None) or (breadth < size):
                    breadth = size
        self.specified_length = length
        self.specified_breadth = breadth
        self.hyperlink = options.get('hyperlink', None)
        if self.hyperlink:
            add_to_predocument("hyperref")
        self.check_wires()

    def min_and_max_wires(self, pos):
        global circuit_bottom, circuit_top
        minval = circuit_top
        maxval = circuit_bottom
        for wn in self.targets:
            if wires[wn].location(pos) < minval:
                minval = wires[wn].location(pos)
                argmin = wires[wn]
            if wires[wn].location(pos) > maxval:
                maxval = wires[wn].location(pos)
                argmax = wires[wn]
        return (argmin, argmax)
    
    def check_wires(self):
        input_targets = copy.copy(self.targets)
        self.targets = []
        for w in input_targets:
            (wname, wprefix) = get_wire_name(w)
            self.targets.append(wname)

    def get_length(self):
        if self.specified_length != None:
            return self.specified_length
        return GATE_SIZE

    def get_breadth(self):
        if self.specified_breadth != None:
            return self.specified_breadth
        return GATE_SIZE

    def draw_box(self, pos, dir):
        global wires, orientation
        scope_str = make_scope_str(color=self.color,style=self.style)
        if scope_str:
            print("\\begin{scope}[%s]" % scope_str)
        draw_options = copy.deepcopy(self.options)
        draw_options['operator'] = self.name
        target_locations = [wires[t].location(pos) for t in self.targets]
        target_min = min(target_locations)
        target_max = max(target_locations)
        pos_s = self.get_length() * 0.5
        the_breadth = self.get_breadth()
        if target_min != target_max:
            the_breadth = max(the_breadth, target_max - target_min + GATE_SIZE)
        target_start = 0.5*(target_min + target_max - the_breadth)
        target_end = 0.5*(target_min + target_max + the_breadth)
        (lratio, bratio, dratio, breadth_shift) = calculate_diameter(None, None, 1,
                                                                         draw_options['shape'], allow_breadth_shift=1)
        if the_breadth/bratio == self.get_length()/lratio:
            draw_options['size'] = the_breadth/bratio
        elif orientation == 'vertical':
            draw_options['size'] = (the_breadth/bratio, self.get_length()/lratio)
        else:
            draw_options['size'] = (self.get_length()/lratio, the_breadth/bratio)
        if self.style:
            style_str = ',' + self.style
        else:
            style_str = ''
        breadth_shift *= 0.5*the_breadth/bratio
        draw_options['thick_side'] = self.thick_side * dir
        (x,y) = get_x_y(pos, 0.5*(target_min + target_max) - breadth_shift)
        draw_xor(x,y,draw_options)
        if self.hyperlink:
            corner1 = get_x_y(pos-pos_s, target_start - breadth_shift)
            corner2 = get_x_y(pos+pos_s, target_end - breadth_shift)
            lower_left = (min(corner1[0], corner2[0]), min(corner1[1], corner2[1]))
            box_width = corner1[0] + corner2[0] - 2*lower_left[0]
            box_height = corner1[1] + corner2[1] - 2*lower_left[1]
            print("\\draw (%f,%f) node[inner sep=0pt, outer sep=0pt, anchor=south west] {\\hyperlink{%s}{\\phantom{\\rule{%fpt}{%fpt}}}};" % (lower_left + (self.hyperlink, box_width, box_height)))
        if scope_str:
            print("\\end{scope}")
            
class Gate:
    # note: "args" includes name of gate and controls
    def __init__(self, gate_type, targets, args, boxes, options={}, comments = None):
        global orientation
        self.type = gate_type
        self.position_list = []
        self.comments = comments
        self.wire_color_changes = {}
        self.wire_style_changes = {}
        self.wire_type_changes = {}
        self.change_to_classical = 0
        self.options = copy.deepcopy(options)
        self.boxes = []
        self.already_drawn = 0
        if self.type == 'G':
            self.boxes = boxes
            self.controls = copy.copy(args)
            self.targets = []
        elif self.type == 'LABEL':
            self.targets = copy.copy(targets)
            self.controls = []
            if len(args) == 0:
                self.labels = [''] # so we can pad the circuit with space
            else:
                self.labels = copy.copy(args)
            for i in range(len(self.labels)):
                if self.labels[i] == '...':
                    self.labels[i] = '\\cdots'
        elif self.type in EQUALS:
            if len(args) == 0:
                if orientation == 'vertical':
                    self.label_string = '\\rotatebox{-90}{$=$}'
                else:
                    self.label_string = '$=$'
            else:
                self.label_string = args[0]
            self.targets = copy.copy(targets)
            self.controls = []
            if self.type != '=':
                add_to_predocument("decorate")
        elif self.type == 'PHANTOM':
            self.targets = copy.copy(targets)
            self.controls = []
        elif self.type in ['IN', 'OUT']:
            self.targets = copy.copy(targets)
            self.name = args[0]
            self.controls = []
        elif self.type in ['START', 'END']:
            self.targets = copy.copy(targets)
            self.controls = []
        elif self.type in ['M','/']:
            if 'operator' in options.keys():
                self.name = options['operator']
            elif len(args) == 0:
                self.name = None
            else:
                self.name = args[0]
            self.controls = []
            self.targets = copy.copy(targets)
        else:
            self.controls = copy.copy(args)
            self.targets = copy.copy(targets)
        # remove duplicates
        save_targets = self.targets
        self.targets = []
        for wn in save_targets:
            if wn not in self.targets:
                self.targets.append(wn)
        save_controls = self.controls
        self.controls = []
        for wn in save_controls:
            if wn not in self.targets and wn not in self.controls:
                self.controls.append(wn)
        if level_stack:
            default_color = level_stack[-1]['color']
            default_style = level_stack[-1]['style']
            default_fill = level_stack[-1]['fill']
        else:
            default_color = None
            default_style = None
            default_fill = bgcolor
        self.color = options.get('color', default_color)
        self.style = options.get('style', default_style)
        self.fill = options.get('fill', default_fill)
        length = options.get('length', None)
        breadth = options.get('breadth', None)
        size = options.get('size', None)
        if self.type == 'N' and length == None:
            max_size = options.get('size', 6)
            for wn in self.controls + self.targets:
                max_size = max(max_size, options['wires'].get(wn,{}).get('size',0))
            if max_size > 6:
                length = max_size
        self.specified_length = length
        self.specified_breadth = breadth
        self.check_wires()
        if self.type == 'M': # changing wires
            for w in self.targets:
                if not options['wires'].get(w,{}).get('type',None):
                    self.change_wires([w], dict(type='c'), maybe=1)
            self.controls = [] # do not allow controlled measurements
        if self.type == 'IN':
            self.change_wires(self.targets, dict(type='q'), maybe=1)
        if self.type == 'START':
            for wn in self.targets:
                if wires[wn].start_at_start_of_circuit and not wires[wn].explicit_end_seen:
                    start_type = wires[wn].type_info[0]
                    wires[wn].type_info[0] = 'o'
                    wires[wn].start_at_start_of_circuit = 0
                    self.change_wires([wn], dict(type=start_type), maybe=1)
                else:
                    self.change_wires([wn], dict(type='q'), maybe=1)
        if self.type in ['OUT', 'END']:
            self.change_wires(self.targets, dict(type='o'), maybe=1)
            if self.type == 'END':
                for wn in self.targets:
                    wires[wn].explicit_end_seen = 1
        self.pi = None
        self.input_line = current_input_line
        self.input_line_num = line_num
        if self.type == 'N':
            self.match_type = len(self.targets) + len(self.controls)
        elif self.boxes:
            self.match_type = 'G'
        else:
            self.match_type = self.type
        
    def match(self,the_depth):
        other_type = the_depth.get_type()
        if (self.match_type == 'PHANTOM'):
            return 1
        if isinstance(self.match_type,int):
            if other_type == self.match_type:
                return 1
            else:
                return 0
        elif self.match_type == 'G':
            if other_type == 'G':
                return 1
            else:
                return 0
        elif other_type == 'G' or isinstance(other_type,int):
            return 0
        else:
            return 1

    # deal with gates that target 'all' wires when they might not yet have been defined
    # needed for LABEL
    def fix_targets(self):
        if self.type in ['LABEL','PHANTOM'] + EQUALS:
            if not self.targets:
                self.targets = copy.copy(wires_in_order)
            if self.type == 'LABEL':
                if len(self.labels) == 1:
                    self.labels = [self.labels[0]] * len(self.targets)
                if len(self.labels) != len(self.targets):
                    sys.exit(("Error:  Line %i: Wrong number of labels in: " % self.input_line_num) + ' '.join(self.labels))
    
    def change_wires(self, raw_wire_names, options, maybe=0):
        # This gate changes these wires' color/style/type; length not currently supported
        # maybe = 1:  don't make the change if it's already present
        wire_names = [get_wire_name(wn,return_prefix=0) for wn in raw_wire_names]
        did_something = 0
        if options.get('color', None):
            for wn in wire_names:
                self.wire_color_changes[wires[wn]] = options['color']
            did_something = 1
        if options.get('style', None):
            for wn in wire_names:
                self.wire_style_changes[wires[wn]] = options['style']
            did_something = 1
        if options.get('type', None):
            any_changes = 0
            for wn in wire_names:
                if (maybe and wires[wn] in self.wire_type_changes):
                    pass
                else:
                    self.wire_type_changes[wires[wn]] = options['type']
                    any_changes = 1
            if (options['type'] == 'c') and any_changes:
                self.change_to_classical = 1
            if any_changes:
                did_something = 1
        if not did_something:
            #With wire-specific operators this is now reasonable
            #print("Warning: Line %i: empty wire change\n" % line_num, file=sys.stderr)
            pass

    def all_wires(self):
        wires_to_use = []
        if self.targets:
            wires_to_use.extend(self.targets)
        if self.controls:
            wires_to_use.extend(self.controls)
        if self.boxes:
            for box in self.boxes:
                wires_to_use.extend(box.targets)
        if not wires_to_use: # could be all wires by default
            if self.type in ['LABEL','TOUCH'] + EQUALS:
                wires_to_use.extend(list(wires.keys()))
        return wires_to_use

    def any_wires(self):
        if self.targets or self.controls or self.boxes:
            return 1
        return 0
    
    def max_depth(self):
        if self.type == 'PHANTOM':
            return -1
        return max([wires[w].get_depth() for w in self.all_wires()])

    def check_wires(self):
        # get_wire_name checks if wire name is valid
        global auto_wires, new_wire_depth
        input_targets = copy.copy(self.targets)
        input_controls = copy.copy(self.controls)
        box_targets = []
        for b in self.boxes:
            box_targets.extend(copy.copy(b.targets))
        self.targets = []
        self.controls = []
        for w in input_targets:
            (wname, wprefix) = get_wire_name(w)
            if wname in box_targets:
                continue
            self.targets.append(wname)
        for w in input_controls:
            (wname, wprefix) = get_wire_name(w)
            if (wname in box_targets) or (wname in self.targets):
                continue
            self.controls.append(wname)
        my_wires = box_targets + self.controls + self.targets
        named_opts = copy.copy(self.options['wires'])
        for wstr in named_opts.keys():
            if self.options['wires'][wstr] and (wstr not in my_wires):
                wname = get_wire_name(wstr, return_prefix=0, create_wire=0)
                if wname != None:
                    self.options['wires'][wname] = self.options['wires'][wstr]
        for g in my_wires:
            if self.options['wires'].get(g,None):
                self.change_wires([g], self.options['wires'][g])
                
    def min_and_max_wires(self, pos, quantum_only = 0):
        global circuit_bottom, circuit_top
        names_to_use = self.targets + self.controls
        for box in self.boxes:
            names_to_use.extend(box.targets)
        minval = circuit_top
        maxval = circuit_bottom
        for wn in names_to_use:
            if quantum_only and wires[wn].get_type(pos) != 'q':
                continue
            if wires[wn].location(pos) < minval:
                minval = wires[wn].location(pos)
                argmin = wires[wn]
            if wires[wn].location(pos) > maxval:
                maxval = wires[wn].location(pos)
                argmax = wires[wn]
        if quantum_only and maxval == circuit_bottom: # no wires
            return (wires[names_to_use[0]], wires[names_to_use[0]])
        return (argmin, argmax)

    def set_depth(self,d):
        global new_wire_depth
        if self.type == 'PHANTOM':
            return
        else:
            for w in self.all_wires():
                wires[w].set_depth(d)
            if self.type in (['LABEL','TOUCH'] + EQUALS) and not self.any_wires():
                # change default for new wires
                new_wire_depth = d

    # Note:  attach_to is now deprecated.  It was used in
    #   early compound gates, but has been replaced by the ';' syntax
    def attach_to(self, g):
        self.options['attach_to'] = g
        
    def set_position(self, pos, direction=1):
        for w in self.wire_color_changes:
            if direction == 1:
                new_color = self.wire_color_changes[w]
            else: # undo change
                new_color = w.get_color(self.position_list[0][0] - 0.001)
            w.change_color(pos, new_color)
        for w in self.wire_style_changes:
            if direction == 1:
                new_style = self.wire_style_changes[w]
            else: # undo change
                new_style = w.get_style(self.position_list[0][0] - 0.001)
            w.change_style(pos, new_style)
        for w in self.wire_type_changes:
            if direction == 1:
                new_type = self.wire_type_changes[w]
            else: # undo change
                new_type = w.get_type(self.position_list[0][0] - 0.001)
            w.change_type(pos, new_type)
        if self.type == 'PERMUTE':
            start_pos = pos - 0.5*self.get_length()
            end_pos = pos + 0.5*self.get_length()
            self.permute_wires(start_pos, end_pos, direction)
        self.position_list.append((pos,direction))

    def get_ranges(self, pos):
        raw_starts = []
        raw_ends = []
        for w in self.all_wires():
            loc = wires[w].location(pos)
            breadth = wires[w].get_breadth()
            raw_starts.append(loc - 0.5*breadth)
            raw_ends.append(loc + 0.5*breadth)
        raw_starts.sort()
        raw_ends.sort()
        starts = [raw_starts[0]]
        ends = []
        for i in range(len(raw_starts) - 1):
            if abs(raw_ends[i] - raw_starts[i+1]) > 0.0001: # really, start != end
                starts.append(raw_starts[i+1])
                ends.append(raw_ends[i])
        ends.append(raw_ends[-1])
        ranges = [(starts[i], ends[i]) for i in range(len(starts))]
        return ranges
    
    def set_pi(self, pos):
        global wires
        
        sorted_targets = copy.copy(self.targets)
        sorted_targets.sort(key=(lambda wn: wires[wn].location(pos)))
        sorted_targets.reverse()
        self.pi = {}
        self.pi_inverse = {}
        for i in range(len(sorted_targets)):
            self.pi[sorted_targets[i]] = self.targets[i]
            self.pi_inverse[self.targets[i]] = sorted_targets[i]
        
    def permute_wires(self, start_pos, end_pos, direction):
        # make list of affected wires
        global wires
        if not self.pi:
            self.set_pi(start_pos)

        (minw, maxw) = self.min_and_max_wires(start_pos)
        minloc = minw.location(start_pos)
        maxloc = maxw.location(start_pos)
        affected = []
        for w in wires.values():
            if w.location(start_pos) >= minloc and w.location(start_pos) <= maxloc:
                affected.append(w)
        affected.sort(key=(lambda w: w.location(start_pos)))
        # figure out new order
        new_order = []
        for w in affected:
            if w.name in self.targets:
                if direction == 1:
                    new_order.append(wires[self.pi[w.name]])
                else:
                    new_order.append(wires[self.pi_inverse[w.name]])
            else:
                new_order.append(w)
        # set new locations
        next_wire_begin = minw.location(start_pos) - 0.5*minw.get_breadth()    
        for w in new_order:
            w_breadth = w.get_breadth()
            old_location = w.location(start_pos)
            new_location = next_wire_begin + 0.5*w_breadth
            w.set_location(old_location, pos=start_pos)
            w.set_location(0.5*(old_location + new_location), 0.5*(start_pos+end_pos))
            w.set_location(new_location, pos=end_pos)
            if old_location != new_location:
                w.add_corner(start_pos)
                w.add_corner(end_pos)
            next_wire_begin += w_breadth

    def do_gate(self):
        global master_depth_list, overall_depth, last_depth
        global allow_different_gates
        if (self.type == 'PHANTOM'):
            pass
        else:
            if (self.type == 'TOUCH'):
                my_depth = max(self.max_depth(), last_depth)
            else:
                my_depth = 1 + self.max_depth()
                if self.type in ['START','END'] and my_depth < last_depth:
                    my_depth = last_depth
                while ((my_depth < overall_depth) and not allow_different_gates and not self.match(master_depth_list[my_depth])):
                    my_depth += 1
            if (my_depth >= overall_depth):
                new_depth()
            last_depth = my_depth
        depth_to_use = master_depth_list[last_depth]
        depth_to_use.add_gate(self)
        self.set_depth(last_depth)
        
    def get_length(self):
        if self.specified_length != None:
            return self.specified_length
        if self.type in ['PHANTOM', 'TOUCH']:
            return 0
        if self.type in ['LABEL', 'START', 'END', 'PERMUTE'] + EQUALS:
            return 15 # maybe not wide enough
        if self.type == '/':
            return GATE_SIZE * (2.0/3.0)
        if self.boxes:
            if self.controls:
                the_length = 6
            else:
                the_length = 0
            for box in self.boxes:
                the_length = max(the_length, box.get_length())
            return the_length
        if self.type in ['M']:
            return GATE_SIZE
        if self.change_to_classical:
            return GATE_SIZE
        if self.type in ['N', 'IN', 'OUT']:
            return 6
        assert 0, 'error: type is ' + self.type

    def get_breadth(self):
        if self.specified_breadth != None:
            return self.specified_breadth
        if self.type in ['IN', 'OUT']:
            return 6
        if self.type == 'M' and self.name:
            return GATE_SIZE * (2.0/3.0)
        return GATE_SIZE
    
    def draw_comments(self,pos):
        global circuit_bottom, circuit_top
        if not self.comments:
            return
        directions = get_directions()
        (x,y) = get_x_y(pos, circuit_top)
        draw_comment(self.comments[0], x, y, directions[0])
        (x,y) = get_x_y(pos, circuit_bottom)
        draw_comment(self.comments[1], x, y, directions[1])

    def ready_to_draw(self):
        if not self.options.get('attach_to',None):
            return 1
        return self.options['attach_to'].already_drawn
    
    def draw_gate(self):
        global wires, orientation, bgcolor
        print(self.input_line)
        self.already_drawn = 1
        if self.type == 'PHANTOM':
            return
        if self.type == 'PERMUTE': # already "drew" gate by changing wire positions
            return
        scope_str = make_scope_str(color=self.color)
        if scope_str:
            print("\\begin{scope}[%s]" % scope_str)
        (width,height) = get_w_h(self.get_length(), self.get_breadth())
        self.draw_comments(self.position_list[0][0])
        for (pos,dir) in self.position_list:
            fixed_wires = []
            if self.type == 'TOUCH':
                if scope_str or self.style:
                    draw_command = "\\draw"
                    if self.style:
                        draw_command += "[%s]" % self.style
                    wire_ranges = self.get_ranges(pos)
                    for (start, end) in wire_ranges:
                        print(draw_command + " (%f,%f) -- (%f,%f);" % (get_x_y(pos,start) + get_x_y(pos,end)))
            elif self.type == 'LABEL':
                tikz_str = "fill=%s" % bgcolor
                if orientation == 'vertical':
                    tikz_str += ", rotate around={-90:(0,0)}"
                for i in range(len(self.targets)):
                    wires[self.targets[i]].draw_label(pos, self.labels[i], tikz_str)
            elif self.type in EQUALS:
                target_locations = [wires[t].location(pos) for t in self.targets]
                target_min = min(target_locations)
                target_max = max(target_locations)
                (x,y) = get_x_y(pos, 0.5*(target_min + target_max))
                (w,h) = get_w_h(self.get_length(), target_max - target_min + self.get_breadth())
                draw_equals(x,y,w,h,self.label_string)
                delta = BRACE_AMPLITUDE
                start_loc = target_min - 0.5*self.get_breadth()
                end_loc = target_max + 0.5*self.get_breadth()
                if self.type[0] == '<':
                    draw_breadthwise_brace(start_loc, end_loc, pos - 0.5*self.get_length() + delta, -delta)
                elif self.type[0] == '>':
                    draw_breadthwise_brace(start_loc, end_loc, pos - 0.5*self.get_length(), delta)
                if self.type[-1] == '<':
                    draw_breadthwise_brace(start_loc, end_loc, pos + 0.5*self.get_length(), -delta)
                elif self.type[-1] == '>':
                    draw_breadthwise_brace(start_loc, end_loc, pos + 0.5*self.get_length() - delta, delta)
            else:
                # make the wire
                if self.type not in ['M','/','START','END']:
                    minw, maxw = self.min_and_max_wires(pos)
                    top = maxw.location(pos)
                    bottom = minw.location(pos)
                    qmin, qmax = self.min_and_max_wires(pos, quantum_only=1)
                    qtop = qmax.location(pos)
                    qbottom = qmin.location(pos)
                    draw_command = "\\draw"
                    if self.style:
                        draw_command += "[%s]" % self.style
                    if top != qtop:
                        for p in [pos-CLASSICAL_SEP,pos+CLASSICAL_SEP]:
                            print(draw_command + " (%f,%f) -- (%f,%f);" % (get_x_y(p, top) + get_x_y(p, qtop)))
                    if qtop != qbottom:
                        print(draw_command + " (%f,%f) -- (%f,%f);" % (get_x_y(pos, qtop) + get_x_y(pos, qbottom)))
                    if qbottom != bottom:
                        for p in [pos-CLASSICAL_SEP,pos+CLASSICAL_SEP]:
                            print(draw_command + " (%f,%f) -- (%f,%f);" % (get_x_y(p, qbottom) + get_x_y(p, bottom)))
                # make the box, controls, targets
                for box in self.boxes:
                    box.draw_box(pos, dir)
                    (minw, maxw) = box.min_and_max_wires(pos)
                    box_min = minw.location(pos)
                    box_max = maxw.location(pos)
                    pos_s = box.get_length() * 0.5
                    for wn in list(wires.keys()):
                        loc = wires[wn].location(pos)
                        if loc < box_min or box_max < loc:
                            continue
                        if wn in self.controls:
                            tikz_str = None
                        elif wn in self.all_wires():
                            continue
                        else:
                            tikz_str = 'dashed'
                        wires[wn].fix_wire(pos-pos_s,pos+pos_s, tikz_str=tikz_str)
                        fixed_wires.append(wn)
                # deal with other gate types
                if self.type in ['IN', 'OUT']:
                    if self.type == 'IN':
                        thick_side = 1 # right side
                    else:
                        thick_side = -1 # left side
                    thick_side *= dir
                    target = self.targets[0]
                    (x,y) = get_x_y(pos, wires[target].location(pos))
                    draw_drop(x,y,width, height, self.name,thick_side,style=self.style)
                elif self.type in ['START','END']:
                    if self.type == 'START':
                        forward = 1
                    else:
                        forward = -1
                    forward *= dir
                    for target in self.targets:
                        if forward == 1:
                            wires[target].draw_start_label(pos + 0.5*self.get_length(), "fill=%s" % bgcolor,length=self.get_length())
                        else:
                            wires[target].draw_end_label(pos - 0.5*self.get_length(), "fill=%s" % bgcolor,length=self.get_length())
                elif self.type in ['N', 'M','/']:
                    for target in self.targets:
                        (x,y) = get_x_y(pos, wires[target].location(pos))
                        if self.type == 'N':
                            draw_options = get_draw_options(self.options, target, '+')
                            draw_xor_or_control(x,y,draw_options)
                        elif self.type == 'M':
                            draw_measurement(x,y, width, height, name=self.name, style=self.style, fill=self.fill)
                        elif self.type == '/':
                            draw_slash(x,y,width,height,name=self.name,style=self.style)
                elif not self.boxes:
                    assert 0, 'unknown type %s' % self.type
                # draw controls
                for wn in self.controls:
                    (x,y) = get_x_y(pos, wires[wn].location(pos))
                    draw_options = get_draw_options(self.options, wn, '.')
                    draw_xor_or_control(x,y,draw_options)
                # did we implicitly measure any wires?
                if self.type not in ['M','/','IN','OUT','START','END'] and self.change_to_classical:
                    for w in list(self.wire_type_changes.keys()):
                        if self.wire_type_changes[w] == 'c' and w.name not in fixed_wires:
                            (x,y) = get_x_y(pos, w.location(pos))
                            draw_measurement(x, y, width, height, style=self.style, fill=self.fill)
                        
        if scope_str:
            print("\\end{scope}")

def new_depth(depth_to_copy=None,direction=1):
    global overall_depth, master_depth_list
    overall_depth += 1
    master_depth_list.append(Depth(depth_to_copy=depth_to_copy,direction=direction))

def begin_level(options):
    global level_stack, level_list, bgcolor
    if not level_stack: # starting the outer level
        level_list = []
        default_level_color = None
        default_level_style = None
        default_level_fill = bgcolor
    else:
        default_level_color = level_stack[-1].get('color', None)
        default_level_style = level_stack[-1].get('style', None)
        default_level_fill = level_stack[-1].get('fill', None)        
    level_options = {}
    level_options['color'] = options.get('color', default_level_color)
    level_options['style'] = options.get('style', default_level_style)
    level_options['fill'] = options.get('fill', default_level_fill)
    level_stack.append(level_options)

def end_level():
    global level_stack, level_list
    global master_depth_list, overall_depth, last_depth
    if (not level_stack):
        sys.exit("Error:  Line %i: Illegal level end\n" % line_num)
    level_stack.pop(-1)
    if level_stack: # nested levels remain
        return
    if not level_list: # no gates
        return
    my_depth = 1 + max([g.max_depth() for g in level_list])
    if (my_depth >= overall_depth):
        new_depth()
    master_depth_list[my_depth].add_gate_list(level_list)
    for g in level_list:
        g.set_depth(my_depth)
    last_depth = my_depth

def do_one_depth(gate_list, start_pos):
    global wires
    current_pos = 0
    sub_pos = {}
    for w in wires:
        sub_pos[w] = 0
    gate_assignments = []
    component = {}
    for w in wires:
        component[w] = set([w])
    for gate in gate_list:
        gate.fix_targets()
        if gate.type == 'TOUCH':
            continue
        if gate.type in ['M','/','LABEL','PHANTOM']:
            the_names = copy.copy(gate.targets)
        else:
            minw, maxw = gate.min_and_max_wires(current_pos)
            minloc = minw.location(current_pos)
            maxloc = maxw.location(current_pos)
            the_names = []
            for wn in wires:
                if wires[wn].location(current_pos) >= minloc and wires[wn].location(current_pos) <= maxloc:
                    the_names.append(wn)
        if gate.type == 'PHANTOM':
            for wn in gate.targets:
                sub_pos[wn] = current_pos
            gate_assignments += [(gate, current_pos)]
        else:
            pos_to_use = max([sub_pos[wn] for wn in the_names])
            gate_assignments += [(gate, pos_to_use + 0.5*gate.get_length())]
            for wn in the_names:
                sub_pos[wn] = pos_to_use + gate.get_length()
            #current_pos = max(current_pos, pos_to_use + gate.get_length())
            current_pos = max(sub_pos.values())
        the_component = component[the_names[0]]
        for wn in the_names:
            if wn not in the_component:
                c = component[wn]
                the_component.update(c)
                for j in c:
                    component[j] = the_component
    # find blocks (of wires) that can be centered
    blocks = []
    for wn in wires:
        if component[wn] not in blocks:
            blocks.append(component[wn])
    adjustment = {}
    for w in wires:
        adjustment[w] = 0
    for block in blocks:
        block_length = 0
        for i in block:
            if sub_pos[i] > block_length:
                block_length = sub_pos[i]
        for i in block:
            adjustment[i] = 0.5 * (current_pos - block_length)
    # set the positions
    for (gate, pos) in gate_assignments:
        minw, maxw = gate.min_and_max_wires(current_pos)
        if 'attach_to' not in gate.options:
            gate.set_position(start_pos + pos + adjustment[minw.name])
    for (gate, pos) in gate_assignments:
        if 'attach_to' in gate.options:
            attachee = gate.options['attach_to']
            (attach_pos, dir) = attachee.position_list[-1]
            pos_to_use = attach_pos + gate.options['attach_offset']
            gate.set_position(pos_to_use)
    return start_pos + current_pos

# either: repeat depths with start <= d <= end (without flipping)
#                         or start >= d >= end (with flipping)
# if start == end, assume we flip

def repeat_section(start, end):
    global master_depth_list, overall_depth, last_depth, wires
    if start < 0 or end < 0 or start >= overall_depth or end >= overall_depth:
        print("Cannot repeat %i to %i when depth is %i" % (start, end, overall_depth), file=sys.stderr)
        return
    if start < end:
        direction = 1
    else: # start >= end
        direction = -1
    for source in range(start, end+direction, direction):
        if master_depth_list[source].depth_to_copy != None:
            real_source = master_depth_list[source].depth_to_copy
            real_direction = direction * master_depth_list[source].direction
        else:
            real_source = source
            real_direction = direction
        new_depth(depth_to_copy=real_source,direction=real_direction)
    last_depth = overall_depth - 1
    for w in list(wires.values()):
        w.touch(last_depth)

# descriptor can be an integer, or a tuple whose first entry is a string
# build a sort key from this
def descriptor_key(a):
    # ints first
    if isinstance(a,int):
        return (0, a)
    # tuple: sort by initial string, then length, then contents
    return (1, a[0], len(a)) + a

def list_wires_in_order():
    descriptors = []
    for wname in wires:
        if wname not in declared_wires_in_order:
            descriptors.append(wname)
    descriptors.sort(key=descriptor_key)
    return declared_wires_in_order + descriptors

def end_circuit():
    global wires, master_depth_list, overall_depth, cut_info, wires_in_order, circuit_top, circuit_bottom
    current_pos = 0
    starts = []
    cut_lines = []
    wires_in_order = list_wires_in_order()
    # TO DO: add the other wires
    for i in range(len(wires)-1,-1,-1):
        # start with last wire at location 0
        w = wires[wires_in_order[i]]
        w_breadth = w.get_breadth()
        if i == len(wires) - 1:
            next_wire_begin = -0.5*w_breadth
            circuit_bottom = next_wire_begin
        w.set_location(next_wire_begin + 0.5*w_breadth)
        next_wire_begin += w_breadth
    circuit_top = next_wire_begin
    for current_depth_num in range(overall_depth):
        depth = master_depth_list[current_depth_num]
        if depth.depth_to_copy == None:
            if depth.gate_list:
                end_pos = DEPTH_PAD + do_one_depth(depth.gate_list, current_pos+DEPTH_PAD)
            else:
                end_pos = current_pos
            depth.set_boundaries(current_pos, end_pos)
        else:
            end_pos = depth.copy_gates(current_pos)
        for g in depth.gate_list:
            if g.type == 'TOUCH':
                g.set_position(end_pos)
        current_pos = end_pos
        if current_depth_num in cut_info or (('default' in cut_info) and (current_depth_num < overall_depth - 1)):
            if current_depth_num in cut_info:
                cut_options = cut_info[current_depth_num]
            else:
                cut_options = cut_info['default']
            cut_lines.append((current_pos, cut_options))
    print_circuit(current_pos, cut_lines)

def print_circuit(circuit_length, cut_lines):
    global wires, master_depth_list, orientation, braces_list
    global circuit_bottom, circuit_top, bgcolor

    for pre in predocument_list:
        print("%! " + pre)
    for pre in preamble_list:
        print(pre)
    for col in new_colors:
        print("\\definecolor{%s}{rgb}{%s,%s,%s}" % (col[0], col[1], col[2], col[3]))
    print("\\begin{tikzpicture}[scale=%f,x=1pt,y=1pt]" % overall_scale)
    print("\\filldraw[color=%s] (%f, %f) rectangle (%f, %f);" % ((bgcolor,) + get_x_y(0, circuit_bottom) + get_x_y(circuit_length, circuit_top)))
    for pre in pretikz_list:
        print(pre)
    # draw in the wires
    print("% Drawing wires")
    for w in list(wires.values()):
        w.draw_wire(circuit_length)
    # draw in the gates
    print("% Done with wires; drawing gates")
    pending_list = []
    for d in master_depth_list:
        for g in d.gate_list:
            if g.ready_to_draw():
                g.draw_gate()
                if pending_list:
                    new_pending_list = []
                    for h in pending_list:
                        if h.ready_to_draw():
                            h.draw_gate()
                        else:
                            new_pending_list.append(h)
                    pending_list = new_pending_list
            else:
                pending_list.append(g)
    print("% Done with gates; drawing ending labels")
    for w in list(wires.values()):
        if w.end_at_end_of_circuit():
            w.draw_end_label(circuit_length)
        if w.labels:
            print("Warning: %i unused label(s) on wire %s\n" % (len(w.labels), w), file=sys.stderr)
    print("% Done with ending labels; drawing cut lines and comments")
    # cut lines
    for (pos, cut_options) in cut_lines:
        cut_style = cut_options.get('style', 'dashed')
        if cut_options.get('color', None):
            cut_style += ',color=%s' % cut_options['color']
        print("\\draw[%s] (%f, %f) -- (%f, %f);" % ((cut_style,) + get_x_y(pos, circuit_bottom) + get_x_y(pos, circuit_top)))
    # comments
    directions = get_directions()
    for (start, end, targets, comment0, comment1, input_line, brace_options) in braces_list:
        print(input_line)
        start_pos = master_depth_list[start].start_position + 0.5*DEPTH_PAD
        end_pos = master_depth_list[end].end_position - 0.5*DEPTH_PAD
        brace_color = brace_options.get('color', None)
        if targets:
            tops = []
            bottoms = []
            for wn in targets:
                if wn in wires:
                    wname = wn
                else:
                    wname = get_wire_name(wn, return_prefix=0, create_wire=0)
                    if not wname:
                        sys.exit("Error:  Line %i:  Unknown wire %s" % (line_num, wn))
                tops.append(wires[wname].location(start_pos) + 0.5*wires[wname].get_breadth())
                bottoms.append(wires[wname].location(start_pos) - 0.5*wires[wname].get_breadth())
            top_location = max(tops)
            bottom_location = min(bottoms)
        else:
            top_location = circuit_top
            bottom_location = circuit_bottom
        if brace_options.get('style', None) or brace_options.get('fill', None):
            corner1 = get_x_y(start_pos, top_location)
            corner2 = get_x_y(end_pos, bottom_location)
            draw_highlight_region(corner1, corner2, brace_options)
            delta = 0
        else:
            delta = BRACE_AMPLITUDE
        if comment0:
            if delta:
                draw_brace(start_pos, end_pos, top_location, delta, color=brace_color)
            (x,y) = get_x_y(0.5*(start_pos + end_pos), top_location + delta)
            draw_comment(comment0, x, y, directions[0], color=brace_color)
        if comment1:
            if delta:
                draw_brace(start_pos, end_pos, bottom_location, -delta, color=brace_color)
            (x,y) = get_x_y(0.5*(start_pos + end_pos), bottom_location - delta)
            draw_comment(comment1, x, y, directions[1], color=brace_color)
        if brace_options.get('style', None) or brace_options.get('fill', None):
            corner1 = get_x_y(start_pos, top_location)
            corner2 = get_x_y(end_pos, bottom_location)
            draw_highlight_region(corner1, corner2, brace_options)
    print("% Done with comments")
    for post in posttikz_list:
        print(post)
    print("\\end{tikzpicture}")
        
def interpret_depth(ref, interpret_as_length = 0):
    global depth_marks, last_depth, line_num
    if ref in depth_marks:
        return depth_marks[ref]
    try:
        ref_num = int(ref)
    except:
        sys.exit("Error:  Line %i: bad depth indicator %s\n" % (line_num, ref))
    if interpret_as_length:
        return last_depth - ref_num + 1
    else:
        if ref_num < 0:
            ref_num += overall_depth
        return ref_num

def get_wire_name(word, check_if_wire=1,return_prefix=1,create_wire=1):
    global valid_prefixes
    if word and isinstance(word, str) and (word[0] in valid_prefixes):
        raw_name = word[1:]
        prefix = word[0]
    else:
        raw_name = word
        prefix = ''
    if not check_if_wire: # we just want the string at this point
        name = raw_name
    elif raw_name in wires:
        name = raw_name
    else: # try the descriptor, maybe create the wire
        name = string_to_descriptor(raw_name)
        if create_wire and (name not in wires):
            if (auto_wires == 'off') or (name is None):
                sys.exit("Error:  Line %i:  Unknown wire %s" % (line_num, raw_name))
            else:
                wires[name] = Wire(name, new_wire_depth, [], {})
                label = descriptor_to_tex(name)
                if label:
                    wires[name].add_labels([WireLabel(label,1)])
    if return_prefix:
        return (name, prefix)
    else:
        return name
    
def complete_update(d_main, d_in):
    for (k, v) in d_in.items():
        if isinstance(v, collections.Mapping):
            if (k not in d_main) or not isinstance(d_main[k], collections.Mapping):
                d_main[k] = v
            else:
                complete_update(d_main[k],v)
        else:
            d_main[k] = d_in[k]

# deal with backslashes
# should perhaps handle tex commands better
def parse_backslashes(line):
    pos = 0
    charlist = []
    while pos < len(line):
        if line[pos] == '\\':
            if pos == len(line) - 1:
                raise SyntaxError('trailing \\')
            nextchar = line[pos:pos+2]
            pos += 2
        else:
            nextchar = line[pos]
            pos += 1
        charlist.append(nextchar)
    return charlist


# deal with braces, dollars, quotes
def parse_groups(charlist):
    grouplist = []
    pos = 0
    depth = []
    while pos < len(charlist):
        if charlist[pos] in ['{','$','"']:
            group = charlist[pos]
            depth.append(charlist[pos]) 
            pos += 1
            while depth:
                if charlist[pos] == '{':
                    depth.append('{')
                elif charlist[pos] == '$':
                    if depth[-1] == '$':
                        depth = depth[:-1]
                    else:
                        depth.append('$')
                elif charlist[pos] == '"':
                    if depth[-1] == '"':
                        depth = depth[:-1]
                    else:
                        depth.append('"')
                elif charlist[pos] == '}':
                    if depth[-1] == '{':
                        depth = depth[:-1]
                    else:
                        raise SyntaxError('Unexpected } in math mode')
                group += charlist[pos]
                pos += 1
                if depth and (pos == len(charlist)):
                    raise SyntaxError('Unclosed ' + ''.join(depth))
            grouplist.append(group)
        elif charlist[pos] == '}':
            raise SyntaxError('Unexpected }')
        else:
            grouplist.append(charlist[pos])
            pos += 1
    return grouplist

# comments with # (drop the rest of the line)
# and comments with % (draw on the sides)
def parse_comments(grouplist):
    # comments with #
    if '#' in grouplist:
        hash_loc = grouplist.index('#')
        grouplist = grouplist[:hash_loc]
    # comments with %
    grouplist.extend(['%','%','%'])
    pct_locs = [i for i in range(len(grouplist)) if grouplist[i] == '%']
    main_piece = grouplist[:pct_locs[0]]
    comment0 = (''.join(grouplist[pct_locs[0]+1:pct_locs[1]])).strip()
    comment1 = (''.join(grouplist[pct_locs[1]+1:pct_locs[2]])).strip()
    return main_piece, comment0, comment1

# find arguments to a macro, and then put them into raw_expansion
def apply_definition(words, args, raw_expansion, def_name):
    global valid_prefixes
    arg_dict = {}
    num_words_left = len(words)

    for i in range(len(args) - 1, -1, -1): # go backwards through arguments
        arg_start = num_words_left - 1
        while (arg_start > 1) and words[arg_start-1] == ':':
            arg_start -= 2
        if arg_start < 0:
            raise SyntaxError("Not enough arguments to %s" % def_name) 
        arg_dict[args[i]] = words[arg_start:num_words_left]
        if ';' in arg_dict[args[i]]:
            raise SyntaxError("Cannot use ; as argument to %s" % def_name)
        num_words_left = arg_start
    words_out = words[:num_words_left]
    for w in raw_expansion:
        if w in arg_dict:
            words_out.extend(arg_dict[w])
        elif w and (w[0] in valid_prefixes) and (w[1:] in arg_dict):
            # if x -> a, then +x -> +a, -x -> -a
            temp_expansion = copy.copy(arg_dict[w[1:]])
            temp_expansion[0] = w[0] + temp_expansion[0]
            words_out.extend(temp_expansion)
        else:
            words_out.append(w)
    return words_out

# split based on whitespace ; return list of "words"
# semicolon is a special character; keep that in the list
# a "word" can be split into subwords by colons -- keep track of this
def parse_into_subwords(grouplist):
    spaces = [string.whitespace[i] for i in range(len(string.whitespace))]
    delimeters = [':',';']
    subwords = []
    current_word = ''
    last_word = ''
    grouplist.append(' ')
    for x in grouplist:
        if x in spaces + delimeters:
            if current_word:
                if (last_word != 'DEFINE') and ((current_word in defined_symbols) or (current_word[0] in valid_prefixes) and (current_word[1:] in defined_symbols)):
                    if current_word in defined_symbols:
                        the_prefix = ''
                        the_word = current_word
                    else:
                        the_prefix = current_word[0]
                        the_word = current_word[1:]
                    (args, raw_expansion) = defined_symbols[the_word]
                    subwords = apply_definition(subwords, args, raw_expansion, the_word)
                    if subwords:
                        subwords[0] = the_prefix + subwords[0]
                else:
                    subwords.append(current_word)
                last_word = current_word
            current_word = ''
            if x in delimeters:
                subwords.append(x)
        else:
            current_word += x
    return subwords

def parse_into_commands(subwords):
    subwords.append(';')
    semi_locs = [i for i in range(len(subwords)) if subwords[i] == ';']
    commands = [subwords[:semi_locs[0]]]
    for i in range(1,len(semi_locs)):
        commands.append(subwords[semi_locs[i-1]+1:semi_locs[i]])
    return commands
    
def parse_command(subwords):
    # parse options out
    # subwords includes attributes; real_words will not
    real_words = []
    line_options = {}
    wire_options = {}
    gate_options = []
    
    gate_names = ['G', 'G|', '|G', 'P']
    while subwords:
        w = subwords.pop(0)
        word_options = parse_options(w)
        if word_options:
            w = ''
            current_options = word_options
        else:
            real_words.append(w)
            current_options = {}
        while subwords and (subwords[0] == ':'):
            subwords.pop(0) # strip colon
            if not subwords:
                raise SyntaxError('Cannot end line with colon')
            raw_attribute = subwords.pop(0) 
            attribute = parse_options(raw_attribute)
            if not attribute:
                raise SyntaxError('Non-option %s after colon' % raw_attribute)
            else:
                complete_update(current_options, attribute)
        if w in gate_names:
            gate_options.append(current_options)
        elif w:
            (wname, prefix) = get_wire_name(w, check_if_wire = 0)
            if wname not in wire_options:
                wire_options[wname] = {}
            if prefix:
                wire_options[wname]['prefix'] = prefix
            complete_update(wire_options[wname], current_options)
        else:
            complete_update(line_options, current_options)
    return real_words, line_options, wire_options, gate_options

def parse_commands(commands):
    output = []
    overall_options = {}
    for command in commands:
        words, line_options, wire_options, gate_options = parse_command(command)
        if words:
            line_options['wires'] = wire_options
            output.append((words, line_options, gate_options))
        else:
            complete_update(overall_options, line_options)
    if len(output) > 1:
        output.insert(0, (['LB'], overall_options, {}))
        output.append((['LE'], {}, {}))
    return output

def tokenize(line):
    global defined_symbols
    
    charlist = parse_backslashes(line)
    grouplist = parse_groups(charlist)
    main_piece, comment0, comment1 = parse_comments(grouplist)
    subwords = parse_into_subwords(main_piece) # includes attributes
    
    # if it's a definition, don't do any more parsing
    if 'DEFINE' in subwords:
        def_pos = subwords.index('DEFINE')
        if len(subwords) < def_pos + 2:
            raise SyntaxError('DEFINE must have an argument')
        defined_symbols[subwords[def_pos+1]] = (subwords[:def_pos], subwords[def_pos+2:])
        return [], '', ''

    raw_commands = parse_into_commands(subwords)
    commands = parse_commands(raw_commands)
    return commands, comment0, comment1

def get_command_from_file(in_file):
    global line_num, current_input_line

    for line in in_file:
        line_num += 1
        current_input_line = "%% Line %i: " % line_num + line.strip()
        try:
            commands, comment0, comment1 = tokenize(line.strip())
        except SyntaxError as e:
            sys.exit("Syntax Error:  Line %i: %s\n" % (line_num, e))
        for i in range(len(commands)):
            (words, line_options, gate_options) = commands[i]
            if not words:
                continue
            if i == len(commands) - 1:
                the_comment0 = comment0
                the_comment1 = comment1
            else:
                the_comment0 = ''
                the_comment1 = ''
            yield (words, line_options, gate_options, the_comment0, the_comment1)
    return

def process_one_command(words, line_options, gate_options, comment0, comment1):
    global line_num, EQUALS
    global overall_depth, depth_marks, last_depth, braces_list
    global allow_different_gates, cut_info, wires, declared_wires_in_order
    global DEPTH_PAD, GATE_SIZE, BRACE_AMPLITUDE, WIRE_PAD, ROUNDED_CORNERS
    global OPACITY, COMMENT_SIZE, wire_prefix, premath_str, postmath_str
    global overall_scale, new_colors, preamble_list, pretikz_list
    global posttikz_list, orientation, start_degrees, end_degrees
    global measure_shape, bgcolor, auto_wires, predocument_list
    global level_stack, level_list
    original_line_options = copy.copy(line_options)
    if (words[0] == 'R'):
        if len(words) == 1:
            repeat_section(overall_depth-2,0)
        elif (len(words) == 3):
            sec_start = interpret_depth(words[1])
            sec_end = interpret_depth(words[2])
            if sec_start < sec_end:
                if words[1] in depth_marks:
                    sec_start += 1
            elif sec_end < sec_start:
                if words[2] in depth_marks:
                    sec_end += 1
            repeat_section(sec_start, sec_end)
        else:
            sys.exit("Error:  Line %i:  bad R command" % line_num)
    elif (words[0] == 'LB'):
        begin_level(line_options)
    elif (words[0] == 'LE'):
        end_level()
    elif (words[0] == 'MIXGATES'):
        allow_different_gates = int(words[1])
    elif (words[0] == 'CUT'):
        if words[1:]:
            for i in words[1:]:
                i_depth = interpret_depth(i)
                if i not in depth_marks:
                    i_depth-= 1 
                # -1 is to switch numbering "after" to "before"
                cut_info[i_depth] = copy.copy(line_options)
        else:
            cut_info['default'] = copy.copy(line_options)
    elif (words[0] == 'DEPTHPAD'):
        DEPTH_PAD = float(words[1])
    elif (words[0] == 'GATESIZE'):
        GATE_SIZE = float(words[1])
        BRACE_AMPLITUDE = GATE_SIZE / 3.0
    elif (words[0] == 'WIREPAD'):
        WIRE_PAD = float(words[1])
    elif (words[0] == 'CORNERS'):
        ROUNDED_CORNERS = float(words[1])
    elif (words[0] == 'OPACITY'):
        OPACITY = float(words[1])
    elif (words[0] == 'COMMENTSIZE'):
        COMMENT_SIZE = float(words[1])
    elif (words[0] == 'WIRES'):
        wire_prefix = words[1]
    elif (words[0] == 'PREMATH'):
        premath_str = words[1]
    elif (words[0] == 'POSTMATH'):
        postmath_str = words[1]
    elif (words[0] == 'SCALE'):
        overall_scale *= float(words[1])
    elif (words[0] == 'COLOR'):
        new_colors.append(words[1:])
    elif (words[0] == 'PREAMBLE'):
        preamble_list.append(' '.join(words[1:]))
    elif (words[0] == 'PRETIKZ'):
        pretikz_list.append(' '.join(words[1:]))
    elif (words[0] == 'POSTTIKZ'):
        posttikz_list.append(' '.join(words[1:]))
    elif (words[0] == 'HYPERTARGET'):
        preamble_list.append('\\hypertarget{%s}{}' % ' '.join(words[1:]))
        add_to_predocument("hyperref")
    elif (words[0] == 'HORIZONTAL'):
        orientation = 'horizontal'
    elif (words[0] == 'VERTICAL'):
        orientation = 'vertical'
        if len(words) >= 2:
            start_degrees = float(words[1])
            if len(words) >= 3:
                end_degrees = float(words[2])
            else:
                end_degrees = start_degrees
    elif (words[0] == 'MEASURESHAPE'):
        shape_name = words[1].upper()
        if shape_name in ['D', 'TAG']:
            measure_shape = shape_name
        else:
            sys.exit("Error:  Line %i: bad measure shape %s\n" % (line_num, shape_name))
    elif (words[0] == 'BGCOLOR'):
        if len(words) >= 2:
            bgcolor = words[1]
        else:
            bgcolor = 'bg'
            add_to_predocument("bg")
    elif (words[0] == 'AUTOWIRES'):
        auto_wires = 'on'
    elif (words[0] == 'MARK'):
        for w in words[1:]:
            depth_marks[w] = last_depth
    elif (words[0] == 'HEADER'):
        predocument_list.append(' '.join(words[1:]))
    else:
        targets = []
        controls = []
        boxes = []
        gate_type = None
        pos = 0
        while pos < len(words):
            word = words[pos]
            if word in ['W', 'T', 'C', 'N', 'X', 'H', 'Z', 'LABEL', 'PHANTOM', 'M', 'IN', 'OUT', 'SWAP', '/', 'TOUCH', 'BARRIER', 'START', 'END', 'PERMUTE', '@'] + EQUALS:
                gate_type = word
                controls = words[pos+1:]
                if boxes:
                    sys.exit("Error:  Line %i: cannot mix %s with G or P\n" % (line_num, word))
                break
            elif word in ['G', 'G|', '|G', 'P']:
                if not targets:
                    sys.exit("Error:  Line %i: %s needs at least one target\n" % (line_num, word))
                box_options = copy.copy(line_options)
                complete_update(box_options, gate_options[len(boxes)])
                if 'operator' in box_options:
                    name = box_options['operator']
                    next_pos = pos+1
                else:
                    if len(words) < pos+2:
                        sys.exit("Error: Line %i: %s needs an operator name\n" % (line_num, word))
                    name = words[pos+1]
                    next_pos = pos+2
                boxes.append(Box(word, targets, name, options=box_options))
                targets = []
                pos = next_pos
            else:
                targets.append(word)
                pos += 1
        if gate_type == 'W': # not a gate, just easier to handle it here
            if not targets: # must be at least one wire
                sys.exit("Error: Line %i: W needs a target\n" % line_num)
            num_targets = len(targets)
            labels = [WireLabel(s,num_targets) for s in controls]
            for wname in targets:
                w = get_wire_for_W(wname)
                if not w:
                    w = Wire(wname, new_wire_depth, [], line_options)
                    wires[wname] = w
                    declared_wires_in_order.append(wname)
                w.add_labels(labels)
            if auto_wires == 'default': # disallow
                auto_wires = 'off'
            return
        if gate_type:
            if gate_type == 'N' and len(controls) != 0:
                sys.exit("Error:  Line %i: N should have no control\n" % line_num)
            if gate_type == 'C' and len(controls) != 1:
                sys.exit("Error:  Line %i: C should have one control\n" % line_num)
            if gate_type in ['T'] and len(controls) != 2:
                sys.exit("Error:  Line %i: T should have two controls\n" % line_num)
            if gate_type in ['N', 'C', 'T'] and len(targets) != 1:
                sys.exit("Error:  Line %i: %s should have one target\n" % (gate_type,line_num))
            if gate_type in line_options['wires']:
                complete_update(line_options,line_options['wires'][gate_type])
                del line_options['wires'][gate_type]
        elif boxes: # any remaining "targets" are really controls
            gate_type = 'G'
            controls = copy.copy(targets)
            targets = []
        else: # just controls
            controls = copy.copy(targets)
            targets = [] #used to be [controls.pop(0)]
            gate_type = 'N'
        # comments
        if (gate_type == '@'):
            if len(controls) >= 2:
                start_depth = interpret_depth(controls[0])
                end_depth = interpret_depth(controls[1])
            elif len(controls) == 1:
                start_depth = interpret_depth(controls[0], interpret_as_length = 1)
                end_depth = last_depth
            else:
                start_depth = last_depth
                end_depth = last_depth
            if len(controls) >= 1 and controls[0] in depth_marks:
                start_depth += 1
            braces_list.append((start_depth, end_depth, copy.copy(targets), comment0, comment1, current_input_line, copy.copy(line_options)))
            if (comment0 or comment1) and not (line_options.get('style', None) or line_options.get('fill', None)):
                add_to_predocument("decorate")
            return
        # Use dots-only form for controlled-Z, S
        # now unnecessary -- just list the controls
        #if gate_type == 'Z' and len(targets) != 1:
        #    controls = targets + controls
        #    targets = []
        #    gate_type = 'N'
        #if gate_type == 'S':
        #    if len(targets) != 0:
        #        sys.exit("Error:  Line %i: should not be target to %s\n" % (line_num, gate_type))
        #    gate_type = 'N'
        if gate_type == 'SWAP':
            if len(targets) != 2:
                sys.exit("Error:  Line %i: SWAP should have exactly two targets\n" % line_num)
            if 'operator' not in line_options:
                line_options['operator'] = 'x'
            if 'shape' not in line_options:
                line_options['shape'] = 0
            gate_type = 'N'
        if gate_type in ['C', 'T']:
            gate_type = 'N'
        if gate_type == 'BARRIER':
            gate_type = 'TOUCH'
            add_to_predocument("decorate")
            if line_options.get('style',None):
                line_options['style'] = BARRIER_STYLE + "," + line_options['style']
            else:
                line_options['style'] = BARRIER_STYLE
        if gate_type in ['PHANTOM', 'TOUCH', 'PERMUTE'] and len(controls) != 0:
            real_control_count = 0
            for w in controls:
                if w not in targets:
                    real_control_count += 1
            if real_control_count:
                sys.exit("Error:  Line %i: should not be control to %s\n" % (line_num, gate_type))
        elif gate_type in ['X', 'H', 'Z', 'P', 'IN', 'OUT'] and len(targets) != 1:
            sys.exit("Error:  Line %i: need exactly one target to %s gate\n" % (line_num, gate_type))
        elif gate_type == 'PERMUTE' and len(targets) < 2:
            sys.exit("Error: Line %i: PERMUTE should have at least two targets\n" % line_num)
        if gate_type in ['X', 'H', 'Z']: # convert to boxes
            name = '$' + gate_type + '$'
            boxes.append(Box('G', targets, name, options=line_options))
            targets = []
            gate_type = 'G'
            line_options = original_line_options # strip off anything box-specific                
        new_gate = Gate(gate_type, targets, controls, boxes, options=line_options,
                        comments=[comment0,comment1])
        if level_stack:
            level_list.append(new_gate)
        else:
            new_gate.do_gate()

def main(infile):
    initialize_globals()
    for (words, line_options, gate_options, comment0, comment1) in get_command_from_file(infile):
        process_one_command(words, line_options, gate_options, comment0, comment1)
    # ready to end circuit
    if level_stack:
        sys.exit("Error:  Line %i: Unclosed level\n" % line_num)
    end_circuit()

# Delete eventually
if __name__ == "__main__":
    main(sys.stdin)
