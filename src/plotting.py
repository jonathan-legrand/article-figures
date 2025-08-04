import numpy as np
import matplotlib.pyplot as plt

from nichord.convert import convert_matrix
from nichord.chord import plot_chord

def matrix_to_chord(matrix, atlas, percentile=99.8,
                    diverging=False, 
                    positive_only=True,
                    RSN_to_color=None, title=None,
                    filename=None):
  


    RSNs = np.unique(atlas.macro_labels)
    idx_to_label = {i: RSN for i, RSN in enumerate(np.unique(atlas.macro_labels))}

    # tmp_coefs = MatrixResult(squareform(cluster_coefs[9]), atlas).get_macro_matrix().values
    tmp_coefs = matrix.copy()
    if percentile is not None:
        perc_thr = np.percentile(tmp_coefs, percentile)
    else:
        perc_thr = -np.inf
    
    vmin, vmax = None, None
    if diverging:
        cmap = 'RdBu_r'
        vmin = np.min(tmp_coefs)
        vmax = np.max(tmp_coefs) 
        vmax = np.max((np.abs(vmin), np.abs(vmax)))
        vmin = -vmax
        # tmp_coefs[np.abs(tmp_coefs) < perc_thr] = 0
    else:
        if positive_only:
            vmin = 0
            cmap = 'Reds'
            tmp_coefs[tmp_coefs < perc_thr] = 0
        else:
            vmax = 0
            vmin = None
            cmap = 'Blues'
            tmp_coefs[tmp_coefs > -perc_thr] = 0

    
    edges, edge_weights = convert_matrix(tmp_coefs)

    # fp_chord = 'tmp.png'
    fp_chord = filename
    max_linewidth = 8
    scaling_factor = max_linewidth / edge_weights.max()
    plot_chord(idx_to_label, edges, edge_weights=edge_weights, fp_chord=fp_chord, 
            network_colors=RSN_to_color,
            linewidths=(edge_weights * scaling_factor).tolist(), alphas=0.9, do_ROI_circles=True, label_fontsize=24, 
            # July 2023 update allows changing label fontsize
            do_ROI_circles_specific=False, ROI_circle_radius=0.01,
            # cmap='RdBu_r',
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            do_monkeypatch=True,
            black_BG=True,
            plot_count=False,
            arc_setting=False,
            dpi=600,
            # edge_threshold=5
            )
    if title is not None:
        plt.title(f'{title}', fontsize=10)