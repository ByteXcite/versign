import os, scipy.io, sys

def main():
    if len(sys.argv) < 4:
        return

    in_dir = sys.argv[1]
    if not in_dir.endswith("/"):
        in_dir += "/"

    out_dir = sys.argv[2]
    if not out_dir.endswith("/"):
        out_dir += "/"

    id = sys.argv[3]

    F = []
    G = []
    for f in os.listdir(in_dir):
        if f.endswith(".mat"):
            mat = scipy.io.loadmat(in_dir + f)
            feat = np.array(mat['feature_vector'][0][:])
            if f.startswith("F"):
                F.append(feat)
            
            if f.startswith("G"):
                G.append(feat)

    