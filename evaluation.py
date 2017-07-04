# Script to evaluate the performance of the clustering algorithm.
import argparse
from itertools import combinations


def count_correct_pairs(cluster, labels_lookup):
    """
    Given a cluster, count the number of pairs belong to the same label and
    the total number of pairs.
    """
    total_pairs = 0
    correct_pairs = 0
    pairs = combinations(cluster, 2)
    for f1, f2 in pairs:
        if labels_lookup[f1] == labels_lookup[f2]:
            correct_pairs += 1
        total_pairs += 1
    return correct_pairs, total_pairs


def calculate_pairwise_precision(clusters, labels_lookup):
    """
    Given a cluster, return pairwise precision.
    """
    correct_pairs = 0
    total_pairs = 0
    for cluster in clusters:
        cp, tp = count_correct_pairs(cluster, labels_lookup)
        correct_pairs += cp
        total_pairs += tp
    print correct_pairs, total_pairs


def calculate_pairwise_recall():
    """
    Given all the clusters and the labels, calculate the pairwise recall for
    the dataset.
    """
    raise NotImplementedError


if __name__ == '__main__':
    parser = argparse.ArgumentError()
    parser.add_argument('-c', '--clusters', help='List of lists where each \
                        list is a cluster')
    parser.add_argument('-l', '--labels', help='List of labels associated \
                        with each vector.')
