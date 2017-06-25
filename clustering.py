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
def calculate_symmetric_dist(nearest_neighbors, nn_lookup, row_no):
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


def aro_clustering(nearest_neighbors, thresh):
    '''
    Approximate rank-order clustering. Takes in the nearest neighbors matrix
    and outputs clusters - list of lists.
    '''
    dist_calc_time = time()
    # Calculate the Symmetric distances : Using np.setdiff1d
    nn_lookup = create_neighbor_lookup(nearest_neighbors)
    d = np.zeros(nearest_neighbors.shape)
    # print 'nearest_neighbors.shape: {}'.format(nearest_neighbors.shape)
    for row_no in range(nearest_neighbors.shape[0]):
        d[row_no, :] = calculate_symmetric_dist(nearest_neighbors,
                                                nn_lookup, row_no)
    d_time = time()-dist_calc_time
    print 'Distance calculation time : {}'.format(d_time)
    # Clustering :
    clusters = []
    # Start with the first face :
    nodes = set(list(np.arange(0, nearest_neighbors.shape[0])))
    tc = time()
    plausible_neighbors = create_plausible_neighbor_lookup(
                                                            nearest_neighbors,
                                                            d,
                                                            thresh)
    print 'Time to create plausible_neighbors lookup : {}'.format(time()-tc)
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
            neighbors.difference_update(group)

            # Remove nodes from the global set :
            nodes.difference_update(neighbors)

            # Add the connected neighbors :
            group.update(neighbors)

            # Add the neighbors to the queue to visit them next :
            queue.extend(neighbors)
        # Add the group to the list of groups :
        clusters.append(group)

    print 'Clustering Time : {}'.format(time()-ctime)
    return clusters


def create_plausible_neighbor_lookup(nearest_neighbors,
                                     distance_matrix,
                                     thresh):
    """
    Create a dictionary where the keys are the row numbers(face numbers) and
    the values are the plausible neighbors.
    """
    plausible_neighbors = {}
    for i in range(nearest_neighbors.shape[0]):
        plausible_neighbors[i] = set(list(nearest_neighbors[
                                i,
                                np.where(distance_matrix[i, :] <= thresh)
                                ][0]))
    return plausible_neighbors


def cluster(descriptor_matrix, n_neighbors=20, thresh=2):
    """
    Master function. Takes the descriptor matrix and returns clusters.
    n_neighbors are the number of nearest neighbors considered and thresh
    is the clustering distance threshold
    """
    nearest_neighbors, dists = build_index(descriptor_matrix, n_neighbors)
    clusters = aro_clustering(nearest_neighbors, thresh)
    return clusters
