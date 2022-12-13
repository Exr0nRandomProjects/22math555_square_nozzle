from math import atan2, pi

# distances in meters
HOSE_HEIGHT = 1
SPRAY_SIDELEN = 2
NUM_NOZZLES = 26
NOZZLE_DEPTH = 5/1000

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
    print(f"{x:.2f} {y:.2f}")
