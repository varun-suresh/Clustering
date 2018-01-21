"""
Flask app to visualize clusters.
"""
import os
import json
import argparse
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__, static_url_path='')


def chunks(clusters, size):
    """
    Split clusters into chunks of size=size
    """
    for i in range(0, len(clusters), size):
        yield clusters[i:i+size]

def create_idx_to_path(lfw_dir):
    """
    Create a dictionary where the key is the image index and the value is the
    path to the image.
    """
    labels = sorted(os.listdir(lfw_dir))
    idx = 0
    idx_to_path = {}
    for label in labels:
        for img in sorted(os.listdir(os.path.join(lfw_dir, label))):
            idx_to_path[idx] = os.path.join(lfw_dir, label, img)
            idx += 1
    return idx_to_path

@app.route('/img/<path:fpath>', methods=['GET'])
def get_img_path(fpath):
    print os.path.dirname(fpath), fpath.split('/')[-1]
    return send_from_directory(os.path.dirname(fpath),fpath.split('/')[-1])

@app.route('/single_cluster', methods=["GET"])
def display_one_cluster():
    """
    Method to display images in ine cluster.
    """
    cluster_id = request.args.get('cluster')
    print type(clusters.keys()[0])
    print clusters.keys()[0]
    return render_template("single_cluster.html",
                           cluster_id=cluster_id,
                           idx_to_path=idx_to_path,
                           clusters=clusters)


@app.route('/clusters', methods=["GET"])
def display_clusters():
    """
    Method to display the clusters
    """
    offset = int(request.args.get('offset', '0'))
    limit = int(request.args.get('limit', '50'))
    clusters_id_sorted = sorted(clusters, key=lambda x : -len(clusters[x]))
    batches = chunks(range(len(clusters_id_sorted)), size=limit)
    return render_template('clusters.html',
        offset=offset, limit=limit, batches=batches,
        ordered_list=clusters_id_sorted[offset:offset+limit+1],
        idx_to_path=idx_to_path,
        clusters=clusters)

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Visualize Clusters")
    parser.add_argument("--lfw_dir", required=True, type=str)
    args = parser.parse_args()
    idx_to_path = create_idx_to_path(args.lfw_dir)
    clusters = json.load(open("clusters.json"))
    app.run(debug=False)
