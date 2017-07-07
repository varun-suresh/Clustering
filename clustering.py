# This is an implementation of https://arxiv.org/pdf/1604.00989.pdf, a modified
# version of rank-order clustering.

import pyflann
import numpy as np
from time import time
from profilehooks import profile
import scipy.io as sio


def build_index(dataset, n_neighbors):
    """
    Takes a dataset, returns the "n" nearest neighbors
    """
# Initialize FLANN
    flann = pyflann.FLANN()
    params = flann.build_index(dataset,
                               algorithm='kdtree',
                               trees=4
                               )
    # print params
    nearest_neighbors, dists = flann.nn_index(dataset, n_neighbors,
                                              checks=params['checks'])
    return nearest_neighbors, dists


def create_neighbor_lookup(nearest_neighbors):
    """
    Key is the reference face, values are the neighbors.
    """
    nn_lookup = {}
    for i in range(nearest_neighbors.shape[0]):
        nn_lookup[i] = nearest_neighbors[i, :]
    return nn_lookup


# @profile
def calculate_symmetric_dist_row(nearest_neighbors, nn_lookup, row_no):
    """
    This function calculates the symmetric distances for one row in the
    matrix.
    """
    dist_row = np.zeros([1, nearest_neighbors.shape[1]])
    f1 = nn_lookup[row_no]
    for idx, neighbor in enumerate(f1[1:]):
        Oi = idx+1
        try:
            row = nn_lookup[neighbor]
            Oj = np.where(row == row_no)[0][0] + 1
            # print 'Correct Oj: {}'.format(Oj)
        except IndexError:
            Oj = nearest_neighbors.shape[1]+1
        f2 = set(nn_lookup[row[0]])
        f1 = set(f1)
        dij = len(f1.difference(f2))
        dji = len(f2.difference(f1))

        # print 'dij: {}, dji: {}'.format(dij, dji)
        # print 'Oi: {}, Oj: {}'.format(Oi, Oj)
        dist_row[0, idx+1] = float(dij + dji)/min(Oi, Oj)
    # print dist_row
    return dist_row


def calculate_symmetric_dist(app_nearest_neighbors):
    """
    This function calculates the symmetric distance matrix.
    """
    dist_calc_time = time()
    nn_lookup = create_neighbor_lookup(app_nearest_neighbors)
    d = np.zeros(app_nearest_neighbors.shape)
    for row_no in range(app_nearest_neighbors.shape[0]):
        d[row_no, :] = calculate_symmetric_dist_row(app_nearest_neighbors,
                                                    nn_lookup, row_no)
    d_time = time()-dist_calc_time
    print 'Distance calculation time : {}'.format(d_time)
    return d


def aro_clustering(app_nearest_neighbors, distance_matrix, thresh):
    '''
    Approximate rank-order clustering. Takes in the nearest neighbors matrix
    and outputs clusters - list of lists.
    '''
    # Clustering :
    clusters = []
    # Start with the first face :
    nodes = set(list(np.arange(0, distance_matrix.shape[0])))
    # print 'Nodes initial : {}'.format(nodes)
    tc = time()
    plausible_neighbors = create_plausible_neighbor_lookup(
                                                            app_nearest_neighbors,
                                                            distance_matrix,
                                                            thresh)
    # print 'Time to create plausible_neighbors lookup : {}'.format(time()-tc)
    ctime = time()
    while nodes:
        # Get a node :
        n = nodes.pop()

        # This contains the set of connected nodes :
        group = {n}

        # Build a queue with this node in it :
        queue = [n]

        # Iterate over the queue :
        while queue:
            n = queue.pop(0)
            neighbors = plausible_neighbors[n]
            # Remove neighbors we've already visited :
            neighbors = nodes.intersection(neighbors)
            neighbors.difference_update(group)

            # Remove nodes from the global set :
            nodes.difference_update(neighbors)

            # Add the connected neighbors :
            group.update(neighbors)

            # Add the neighbors to the queue to visit them next :
            queue.extend(neighbors)
        # Add the group to the list of groups :
        clusters.append(group)

    # print 'Clustering Time : {}'.format(time()-ctime)
    return clusters


def create_plausible_neighbor_lookup(app_nearest_neighbors,
                                     distance_matrix,
                                     thresh):
    """
    Create a dictionary where the keys are the row numbers(face numbers) and
    the values are the plausible neighbors.
    """
    n_vectors = app_nearest_neighbors.shape[0]
    plausible_neighbors = {}
    for i in range(n_vectors):
        plausible_neighbors[i] = set(list(app_nearest_neighbors[i,
                                     np.where(
                                            distance_matrix[i, :] <= thresh)]
                                             [0]))
        # min_dist = np.min(distance_matrix[i, 1:])
        # if min_dist <= thresh:
        #     nn_indices = np.where(distance_matrix[i, :] == min_dist)
        #     old_nn_row = app_nearest_neighbors[i, :]
        #     plausible_neighbors[i] = set(list(old_nn_row[nn_indices]))
        # else:
        #     plausible_neighbors[i] = set([])
    return plausible_neighbors


def cluster(descriptor_matrix, n_neighbors=20, thresh=[2]):
    """
    Master function. Takes the descriptor matrix and returns clusters.
    n_neighbors are the number of nearest neighbors considered and thresh
    is the clustering distance threshold
    """
    app_nearest_neighbors, dists = build_index(descriptor_matrix, n_neighbors)
    distance_matrix = calculate_symmetric_dist(app_nearest_neighbors)
    # print distance_matrix
    clusters = []
    for th in thresh:
        clusters_th = aro_clustering(app_nearest_neighbors, distance_matrix, th)
        print 'N Clusters: {}, thresh: {}'.format(len(clusters_th), th)
        clusters.append({'clusters': clusters_th, 'threshold': th})
    return clusters


if __name__ == '__main__':
    descriptor_matrix = np.random.rand(30, 180)
    clusters = cluster(descriptor_matrix, n_neighbors=5)
    n_faces = 0
    for c in clusters:
        n_faces += len(c)
    print clusters
