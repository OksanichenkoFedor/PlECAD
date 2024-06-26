import numpy as np

def give_points_field(min_coord,max_coord,N):
    x = min_coord[0, 0] + np.arange(0, N, 1.0) * ((max_coord[0, 0] - min_coord[0, 0]) / (1.0 * N - 1.0))
    x = np.repeat(np.repeat(x.reshape(N, 1, 1), N, axis=1), N, axis=2).reshape(N, N, N, 1)
    y = min_coord[1, 0] + np.arange(0, N, 1.0) * ((max_coord[1, 0] - min_coord[1, 0]) / (1.0 * N - 1.0))
    y = np.repeat(np.repeat(y.reshape(1, N, 1), N, axis=0), N, axis=2).reshape(N, N, N, 1)
    z = min_coord[2, 0] + np.arange(0, N, 1.0) * ((max_coord[2, 0] - min_coord[2, 0]) / (1.0 * N - 1.0))
    z = np.repeat(np.repeat(z.reshape(1, 1, N), N, axis=1), N, axis=0).reshape(N, N, N, 1)
    coords = np.concatenate((x, y, z), axis=3)
    coords = coords + (np.random.random(coords.shape) - 0.5) * 0.05
    coords = coords.reshape(N * N * N, -1).T
    return coords

def give_points_field2d(min_coord, max_coord, Nx, Ny, rand=0.01):
    delta_x = ((max_coord[0, 0] - min_coord[0, 0]) / (1.0 * Nx - 1.0))
    delta_y = ((max_coord[1, 0] - min_coord[1, 0]) / (1.0 * Ny - 1.0))
    x = min_coord[0, 0] + np.arange(0, Nx, 1.0) * delta_x
    x = np.repeat(x.reshape(Nx, 1), Ny, axis=1).reshape(Nx, Ny, 1)
    y = min_coord[1, 0] + np.arange(0, Ny, 1.0) * delta_y
    y = np.repeat(y.reshape(1, Ny), Nx, axis=0).reshape(Nx, Ny, 1)
    coords = np.concatenate((x, y), axis=2)
    coords = coords + (np.random.random(coords.shape) - 0.5) * rand
    coords = coords.reshape(Nx * Ny, -1).T
    return coords, delta_x, delta_y


def give_inlets_surroundings(inlets,mult=1.1,Nz=20, N_phi=10, N_r=30):
    coords = None
    for inlet in inlets:
        new_in = inlet.get_around_points(mult)
        new_in.generate_points(Nz=Nz, N_phi=N_phi, N_r=N_r, uniq=True)
        if coords is None:
            coords = new_in.coords
        else:
            coords = np.concatenate((coords,new_in.coords),axis=1)
    return coords