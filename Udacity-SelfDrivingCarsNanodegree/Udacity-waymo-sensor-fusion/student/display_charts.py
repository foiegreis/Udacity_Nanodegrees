import matplotlib.pyplot as plt
import json
import numpy as np

with open("data.json", "r") as data_file:
    data_json = json.load(data_file)

precision = data_json['precision']
recall = data_json['recall']
ious_all = data_json['ious']
devs_x = data_json['devs_x']
devs_y = data_json['devs_y']
devs_z = data_json['devs_z']

data = [precision, recall, ious_all, devs_x, devs_y, devs_z]

titles = ['detection precision', 'detection recall', 'intersection over union', 'position errors in X',
          'position errors in Y', 'position error in Z']
textboxes = ['', '', '',
             '\n'.join((r'$\mathrm{mean}=%.4f$' % (np.mean(devs_x),),
                        r'$\mathrm{sigma}=%.4f$' % (np.std(devs_x),), r'$\mathrm{n}=%.0f$' % (len(devs_x),))),
             '\n'.join((r'$\mathrm{mean}=%.4f$' % (np.mean(devs_y),),
                        r'$\mathrm{sigma}=%.4f$' % (np.std(devs_y),), r'$\mathrm{n}=%.0f$' % (len(devs_x),))),
             '\n'.join((r'$\mathrm{mean}=%.4f$' % (np.mean(devs_z),),
                        r'$\mathrm{sigma}=%.4f$' % (np.std(devs_z),), r'$\mathrm{n}=%.0f$' % (len(devs_x),)))]

f, a = plt.subplots(2, 3)
a = a.ravel()
num_bins = 20
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
for idx, ax in enumerate(a):
    ax.hist(data[idx], num_bins)
    ax.set_title(titles[idx])
    if textboxes[idx]:
        ax.text(0.05, 0.95, textboxes[idx], transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)
plt.tight_layout()
plt.show()
