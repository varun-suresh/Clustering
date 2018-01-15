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
    cluster = request.args.get('cluster')
    return render_template("single_cluster.html",
                           idx_to_path=idx_to_path,
                           cluster=cluster)


@app.route('/clusters', methods=["GET"])
def display_clusters():
    """
    Method to display the clusters
    """
    offset = int(request.args.get('offset', '0'))
    limit = int(request.args.get('limit', '50'))
    clusters = json.load(open("clusters.json"))
    clusters_as_list = [v for c, v in clusters.iteritems()]
    clusters_as_list = sorted(clusters_as_list, key=lambda x:-len(x))
    batches = chunks(range(len(clusters_as_list)), size=limit)
    # clusters = []
    # for cluster_id in set(cluster_memberships_emb.values()):
    #     face_indices = [i for i in cluster_memberships_emb.keys() if str(cluster_memberships_emb[i]) == str(cluster_id)]
    #     face_indices = promote_selfie_to_top(face_indices)
    #     clusters.append({
    #         'face_indices': face_indices,
    #         'cluster_id': cluster_id
    #     })
    # total_number_clusters = len(clusters)
    # clusters = sorted(clusters, key=lambda c: -len(c['face_indices']))
    # num_single_clusters = len([c for c in clusters if len(c['face_indices']) == 1])
    # num_faces = len(face_idx_to_photo_emb)
    # batches = list(chunks(range(total_number_clusters), limit))
    return render_template('clusters.html',
        offset=offset, limit=limit, batches=batches,
        clusters=clusters_as_list[offset:offset+limit+1],
        idx_to_path=idx_to_path,
        # face_idx_to_photo=face_idx_to_photo_emb, clusters=clusters[offset:offset+limit+1],
        # total_number_clusters=total_number_clusters,
        # num_single_clusters=num_single_clusters,
        # num_faces=num_faces
        )

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Visualize Clusters")
    parser.add_argument("--lfw_dir", required=True, type=str)
    args = parser.parse_args()
    idx_to_path = create_idx_to_path(args.lfw_dir)
    app.run(debug=True)
    # print idx_to_path
