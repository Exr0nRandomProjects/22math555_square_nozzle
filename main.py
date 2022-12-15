# python3 -m pip install solidpython
from solid import scad_render_to_file
# from solid import cube, sphere, cylinder, hole, translate
# from solid.utils import difference
# from solid.utils import up, down, left, right

# python3 -m pip install solidpython2
from solid2 import cube, cylinder, translate

from math import atan2, pi

# distances in meters
HOSE_HEIGHT = 1 * 1e3
SPRAY_SIDELEN = 2 * 1e3
NUM_NOZZLES = 26
NOZZLE_DEPTH = 5 * 10
NOZZLE_SIDELEN = 12 * 10
HOLE_RADIUS = 0.25

SEGMENTS = 50

# farthest_distance = -1 + 1/NUM_NOZZLES

def deg(rad):
    return rad / pi * 180

# print(deg(atan2(farthest_distance, HOSE_HEIGHT)))

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
def norm(vec):
    from math import sqrt
    return sqrt(sum([x**2 for x in vec]))

def get_angles_for_floor_coord(floor_coord, nozzle_cord):
    fx, fy, fz = floor_coord
    nx, ny, nz = nozzle_cord
    # return (deg(atan2(x-nx, nz-z)), deg(atan2(y-ny, nz-z)))
    # now we doing euler angles yooo
    print(fx-nx, fy-ny, norm([fx, fy]), nz-fz)
    return [deg(atan2(fy-ny, fx-nx)), deg(atan2( norm([fx, fy]), nz-fz ))]


def make_cylinder_from_nozzle_normal(from_x, up, r=HOLE_RADIUS, h=10):
    return cylinder(r=r, h=h).down(h).rotateY(-up).rotateZ(from_x)

if __name__ == '__main__':
    HEIGHT = 10
    eangles = get_angles_for_floor_coord([0, -1000, 0], [0, 0, HOSE_HEIGHT])
    scad = make_cylinder_from_nozzle_normal(*eangles, h=HEIGHT)
    # scad =  cylinder(r=HOLE_RADIUS, h=HEIGHT).down(HEIGHT).rotateY(-90) .rotateY(-45).rotateZ(90)
    # scad += cylinder(r=HOLE_RADIUS, h=HEIGHT).down(HEIGHT).rotateX(45)
    # scad += cylinder(r=HOLE_RADIUS, h=HEIGHT).down(HEIGHT).rotateX(45).rotateY(45)
    # scad += cylinder(r=HOLE_RADIUS, h=HEIGHT).down(HEIGHT).rotateY(45).rotateX(45)
    scad_render_to_file(scad, 'square_nozzle.scad', file_header=f'$fn = {SEGMENTS};')
    print('done')



if __name__ == 'e__main__':
    for floor_coord in get_coords(NUM_NOZZLES, SPRAY_SIDELEN):
        x, y = get_angles_for_floor_coord(floor_coord, [0, 0, HOSE_HEIGHT])
        # print(f"{x:.2f} {y:.2f}")

    scad = up(-NOZZLE_DEPTH/2 + HOSE_HEIGHT)(cube([NOZZLE_SIDELEN, NOZZLE_SIDELEN, NOZZLE_DEPTH], center=True))

    for floor_coord in get_coords(NUM_NOZZLES, SPRAY_SIDELEN):
        x, y, z = floor_coord
        scad += translate(floor_coord)(cylinder(r=HOLE_RADIUS*5e1, h=1))

# scad -= hole()(translate([0, 0, -1])(cylinder(r=2, h=12)))
    scad_render_to_file(down(HOSE_HEIGHT)(scad), "square_nozzle.scad", file_header=f'$fn = {SEGMENTS};',)
