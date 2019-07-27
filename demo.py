# Clustering example using LFW data:
import os
import pandas as pd
from matplotlib import pyplot as plt
import argparse
import json
import scipy.io as sio
from clustering import cluster
from evaluation import calculate_pairwise_pr


def plot_histogram(lfw_dir):
    """
    Function to plot the distribution of cluster sizes in LFW.
    """
    filecount_dict = {}
    for root, dirs, files in os.walk(lfw_dir):
        for dirname in dirs:
            n_photos = len(os.listdir(os.path.join(root, dirname)))
            filecount_dict[dirname] = n_photos
    print("No of unique people: {}".format(len(filecount_dict.keys())))
    df = pd.DataFrame(filecount_dict.items(), columns=['Name', 'Count'])
    print("Singletons : {}\nTwo :{}\n".format((df['Count'] == 1).sum(),
                                              (df['Count'] == 2).sum()))
    plt.hist(df['Count'], bins=max(df['Count']))
    plt.title('Cluster Sizes')
    plt.xlabel('No of images in folder')
    plt.ylabel('No of folders')
    plt.show()


def approximate_rank_order_clustering(vectors):
    """
    Cluster the input vectors.
    """
    clusters = cluster(vectors, n_neighbors=200, thresh= [1.1])
    return clusters


def evaluate_clusters(clusters, labels_lookup):
    """
    This function calculates the pairwise precision and recall for the
    clusters.
    Input:
        clusters: list of lists
            Each list contains a set of integers that correspond to a particular
            image in the LFW dataset.
        labels: dict
            It is a dictionary where the keys are row numbers and the values
            are lables(string).
    Output:
        pairwise_precision: float
            Fraction of pair of samples within a cluster that belong to one
            identity

        pairwise_recall: float
            Fraction of pairs of samples within a cluster which are placed in
            the same cluster over the total number of same cluster pairs within
            the dataset.

        f1_score: float
            Defined as the harmonic mean of precision and recall.
    """
    precision, recall = calculate_pairwise_pr(clusters, labels_lookup)
    f1_score = 2*precision*recall/(precision+recall)
    print("Precision : {}\nRecall : {}\nf1_score : {}".format(precision,
                                                              recall,
                                                              f1_score
                                                              ))
    print("---------------------------------------------------------")
    return f1_score


def create_labels_lookup(labels):
    """
    Create a dictionary where the key is the row number and the value is the
    actual label.
    In this case, labels is an array where the position corresponds to the row
    number and the value is an integer indicating the label.
    """
    labels_lookup = {}
    for idx, label in enumerate(labels):
        labels_lookup[idx] = int(label[0][:])
    return labels_lookup


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Approximate Rank Order Clustering Demo')
    parser.add_argument('--lfw_path', required=True,
                        help='Enter tha directory where LFW images are saved.')
    parser.add_argument('-v', '--vector_file', required=False,
                        help="Path to where the vectors to be clustered are saved.")
    args = vars(parser.parse_args())
    # plot_histogram(args['lfw_path'])
    if args['vector_file']:
        f = sio.loadmat(args['vector_file'])
        vectors = f['features']
        labels = f['labels_original'][0]
        clusters_thresholds = approximate_rank_order_clustering(vectors)
        clusters_at_th = clusters_thresholds[0]
        clusters_to_be_saved = {}
        for i, cluster in enumerate(clusters_at_th["clusters"]):
            c = [int(x) for x in list(cluster)]
            clusters_to_be_saved[i] = c

        with open("data/clusters.json","w") as f:
            json.dump(clusters_to_be_saved, f)

        labels_lookup = create_labels_lookup(labels)
        for clusters in clusters_thresholds:
            print("No of clusters: {}".format(len(clusters['clusters'])))
            print("Threshold : {}".format(clusters['threshold']))
            f1_score = evaluate_clusters(clusters['clusters'], labels_lookup)
        # n_faces = 0
        # for c in clusters:
        #     print c
        #     n_faces += len(c)
        # print 'No of faces : {}'.format(n_faces)
