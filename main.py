# python3 -m pip install solidpython
from solid import scad_render_to_file
from solid import cube, sphere, cylinder, hole, translate
from solid.utils import difference
from solid.utils import up, down, left, right

from math import atan2, pi

# distances in meters
HOSE_HEIGHT = 1 * 1e3
SPRAY_SIDELEN = 2 * 1e3
NUM_NOZZLES = 26
NOZZLE_DEPTH = 5 * 10
NOZZLE_SIDELEN = 12 * 10
HOLE_RADIUS = 0.25

SEGMENTS = 50

farthest_distance = -1 + 1/NUM_NOZZLES

def deg(rad):
    return rad / pi * 180

print(deg(atan2(farthest_distance, HOSE_HEIGHT)))

def get_coords(n_nozzles, spray_sidelen):
    assert n_nozzles % 2 == 0
    square_sidelen = spray_sidelen / n_nozzles

    for i in range(1, n_nozzles+1):  # should probably use numpy.meshgrid or smt
        for j in range(1, n_nozzles+1):
            yield (
                -spray_sidelen/2 + i*square_sidelen - square_sidelen/2,
                -spray_sidelen/2 + j*square_sidelen - square_sidelen/2,
                0
                )

def get_angles_for_floor_coord(floor_coord, nozzle_cord):
    x, y, z = floor_coord
    nx, ny, nz = nozzle_cord
    return (deg(atan2(x-nx, nz-z)), deg(atan2(y-ny, nz-z)))

for floor_coord in get_coords(NUM_NOZZLES, SPRAY_SIDELEN):
    x, y = get_angles_for_floor_coord(floor_coord, [0, 0, HOSE_HEIGHT])
    # print(f"{x:.2f} {y:.2f}")




scad = up(-NOZZLE_DEPTH/2 + HOSE_HEIGHT)(cube([NOZZLE_SIDELEN, NOZZLE_SIDELEN, NOZZLE_DEPTH], center=True))

for floor_coord in get_coords(NUM_NOZZLES, SPRAY_SIDELEN):
    x, y, z = floor_coord
    scad += translate(floor_coord)(cylinder(r=HOLE_RADIUS*5e1, h=1))

# scad -= hole()(translate([0, 0, -1])(cylinder(r=2, h=12)))
scad_render_to_file(down(HOSE_HEIGHT)(scad), "square_nozzle.scad", file_header=f'$fn = {SEGMENTS};',)
