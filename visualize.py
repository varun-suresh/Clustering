"""
Flask app to visualize clusters.
"""
import os
import argparse
from flask import Flask, render_template

app = Flask(__name__)


def chunks(clusters, size):
    """
    Split clusters into chunks of size=size
    """
    for i in range(0, len(clusters), size):
        yield cluster[i:i+size]

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

@app.route('/clusters')
def display_clusters():
    return render_template("clusters.html")

if __name__ == "__main__":
    # app.run()
    parser = argparse.ArgumentParser("Visualize Clusters")
    parser.add_argument("--lfw_dir", required=True, type=str)
    args = parser.parse_args()
    idx_to_path = create_idx_to_path(args.lfw_dir)
    print idx_to_path
