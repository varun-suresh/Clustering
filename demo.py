# Clustering example using LFW data:
import os
import pandas as pd
from matplotlib import pyplot as plt
import argparse
import scipy.io as sio
from clustering import cluster


def plot_histogram(lfw_dir):
    """
    Function to plot the distribution of cluster sizes in LFW.
    """
    filecount_dict = {}
    for root, dirs, files in os.walk(lfw_dir):
        for dirname in dirs:
            n_photos = len(os.listdir(os.path.join(root, dirname)))
            filecount_dict[dirname] = n_photos
    print 'No of unique people: {}'.format(len(filecount_dict.keys()))
    df = pd.DataFrame(filecount_dict.items(), columns=['Name', 'Count'])
    print 'Singletons : {}\nTwo :{}\n'.format((df['Count'] == 1).sum(),
                                              (df['Count'] == 2).sum())
    plt.hist(df['Count'], bins=max(df['Count']))
    plt.show()


def approximate_rank_order_clustering(vectors):
    """
    Cluster the input vectors.
    """
    clusters = cluster(vectors)
    return clusters


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Approximate Rank Order Clustering Demo')
    parser.add_argument('--lfw_path', required=True,
                        help='Enter tha directory where LFW images are saved.')
    parser.add_argument('-v', '--vector_file', required=False,
                        help="Path to where the vectors to be clustered are saved.")
    args = vars(parser.parse_args())
    plot_histogram(args['lfw_path'])
    if args['vector_file']:
        f = sio.loadmat(args['vector_file'])
        vectors = f['features']
        clusters = approximate_rank_order_clustering(vectors)
