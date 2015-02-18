#!/usr/bin/python

import fileinput
modes = dict()

for line in fileinput.input("modes.txt"):
    if line[0] != '#':
        line = line.split()
        modes[line[0]] = line

print "// This file is generated by 'svo_defines.py'."

print """
`define SVO_XYBITS 14

`define SVO_DEFAULT_PARAMS parameter \\
    SVO_MODE             =  "640x480", \\
    SVO_FRAMERATE        =  60, \\
    SVO_BITS_PER_PIXEL   =  18, \\
    SVO_BITS_PER_RED     =   6, \\
    SVO_BITS_PER_GREEN   =   6, \\
    SVO_BITS_PER_BLUE    =   6, \\
    SVO_BITS_PER_ALPHA   =   0

`define SVO_PASS_PARAMS \\
    .SVO_MODE             (SVO_MODE),           \\
    .SVO_FRAMERATE        (SVO_FRAMERATE),      \\
    .SVO_BITS_PER_PIXEL   (SVO_BITS_PER_PIXEL), \\
    .SVO_BITS_PER_RED     (SVO_BITS_PER_RED),   \\
    .SVO_BITS_PER_GREEN   (SVO_BITS_PER_GREEN), \\
    .SVO_BITS_PER_BLUE    (SVO_BITS_PER_BLUE),  \\
    .SVO_BITS_PER_ALPHA   (SVO_BITS_PER_ALPHA)
"""

print "`define SVO_DECLS \\"

print "localparam SVO_HOR_PIXELS = \\"
for mode in modes.values():
    print "  SVO_MODE == \"%s\" ? %d : \\" % (mode[0], int(mode[1]))
print "  'bx; \\"

print "localparam SVO_VER_PIXELS = \\"
for mode in modes.values():
    print "  SVO_MODE == \"%s\" ? %d : \\" % (mode[0], int(mode[2]))
print "  'bx; \\"

print "localparam SVO_HOR_FRONT_PORCH = \\"
for mode in modes.values():
    print "  SVO_MODE == \"%s\" ? %d : \\" % (mode[0], int(mode[3]))
print "  'bx; \\"

print "localparam SVO_HOR_SYNC = \\"
for mode in modes.values():
    print "  SVO_MODE == \"%s\" ? %d : \\" % (mode[0], int(mode[4]))
print "  'bx; \\"

print "localparam SVO_HOR_BACK_PORCH = \\"
for mode in modes.values():
    print "  SVO_MODE == \"%s\" ? %d : \\" % (mode[0], int(mode[5]))
print "  'bx; \\"

print "localparam SVO_VER_FRONT_PORCH = \\"
for mode in modes.values():
    print "  SVO_MODE == \"%s\" ? %d : \\" % (mode[0], int(mode[6]))
print "  'bx; \\"

print "localparam SVO_VER_SYNC = \\"
for mode in modes.values():
    print "  SVO_MODE == \"%s\" ? %d : \\" % (mode[0], int(mode[7]))
print "  'bx; \\"

print "localparam SVO_VER_BACK_PORCH = \\"
for mode in modes.values():
    print "  SVO_MODE == \"%s\" ? %d : \\" % (mode[0], int(mode[8]))
print "  'bx; \\"

print """\
function integer svo_clog2; \\
  input integer v; \\
  begin \\
    if (v > 0) \\
      v = v - 1; \\
    svo_clog2 = 0; \\
    while (v) begin \\
      v = v >> 1; \\
      svo_clog2 = svo_clog2 + 1; \\
    end \\
  end \\
endfunction \\
function integer svo_max; \\
  input integer a, b; \\
  begin \\
    svo_max = a > b ? a : b; \\
  end \\
endfunction \\
function [SVO_BITS_PER_RED-1:0] svo_r; \\
  input [SVO_BITS_PER_PIXEL-1:0] rgba; \\
  svo_r = rgba[0 +: SVO_BITS_PER_RED]; \\
endfunction \\
function [SVO_BITS_PER_RED-1:0] svo_g; \\
  input [SVO_BITS_PER_PIXEL-1:0] rgba; \\
  svo_g = rgba[SVO_BITS_PER_RED +: SVO_BITS_PER_GREEN]; \\
endfunction \\
function [SVO_BITS_PER_RED-1:0] svo_b; \\
  input [SVO_BITS_PER_PIXEL-1:0] rgba; \\
  svo_b = rgba[SVO_BITS_PER_RED + SVO_BITS_PER_GREEN +: SVO_BITS_PER_BLUE]; \\
endfunction \\
function [SVO_BITS_PER_RED-1:0] svo_a; \\
  input [SVO_BITS_PER_PIXEL-1:0] rgba; \\
  svo_a = rgba[SVO_BITS_PER_ALPHA ? SVO_BITS_PER_RED + SVO_BITS_PER_GREEN + SVO_BITS_PER_BLUE : 0 +: svo_max(SVO_BITS_PER_ALPHA, 1)]; \\
endfunction \\
function [SVO_BITS_PER_PIXEL-1:0] svo_rgba; \\
  input [SVO_BITS_PER_RED-1:0] r; \\
  input [SVO_BITS_PER_GREEN-1:0] g; \\
  input [SVO_BITS_PER_BLUE-1:0] b; \\
  input [SVO_BITS_PER_ALPHA-1:0] a; \\
  svo_rgba = {a, b, g, r}; \\
endfunction \\
localparam SVO_HOR_TOTAL = SVO_HOR_FRONT_PORCH + SVO_HOR_SYNC + SVO_HOR_BACK_PORCH + SVO_HOR_PIXELS; \\
localparam SVO_VER_TOTAL = SVO_VER_FRONT_PORCH + SVO_VER_SYNC + SVO_VER_BACK_PORCH + SVO_VER_PIXELS; \\
initial if (SVO_HOR_PIXELS === 'bx) begin $display(\"Invalid SVO_MODE value: %0s\", SVO_MODE); $finish; end
"""
