import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import pickle


stats = pickle.load(open('stats.pkl', 'rb'))

beta = 1
name, p, r, f = [], [], [], []
for k in stats:
    name.append(k)
    p.append(stats[k]['precision'])
    r.append(stats[k]['recall'])
    f.append(stats[k]['f-measure'])
    beta = stats[k]['beta']


n_groups = len(name)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.2

opacity = 0.5
error_config = {'ecolor': '0.3'}

rects1 = ax.bar(index - 0.5 * bar_width, p, bar_width,
                alpha=opacity, color='b', error_kw=error_config,
                label='Precision')

rects2 = ax.bar(index + 0.5 *bar_width, r, bar_width,
                alpha=opacity, color='r', error_kw=error_config,
                label='Recall')

rects3 = ax.bar(index + 1.5 * bar_width, f, bar_width,
                alpha=opacity, color='g', error_kw=error_config,
                label='F-{}'.format(beta))

ax.set_xlabel('Entity Type')
ax.set_ylabel('')
ax.set_title('')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(name)
ax.legend()

fig.tight_layout()
fig.savefig("graphs/entity_prf.png")



met = ['precision', 'recall', 'f-measure']
stat = ['annotated', 'avg_len', 'len_std', 'uni']

for me in met:
    for st in stat:
        avg_len, f = [], []
        for k in stats:
            if st == 'uni':
                avg_len.append(stats[k]['unique_words']/stats[k]['annotated'])
            else:
                avg_len.append(stats[k][st])
            f.append(stats[k][me])

        avg_len = np.array(avg_len)
        m, b = np.polyfit(avg_len, f, 1)
        corr = np.corrcoef(avg_len, f)
        print("Correlation of {} {}: {}".format(st, me, corr))

        fig, ax = plt.subplots()

        ax.plot(avg_len, f, '.')
        ax.plot(avg_len, m*avg_len + b, '-')

        ax.set_xlabel(st)
        ax.set_ylabel(me)
        fig.tight_layout()
        fig.savefig("graphs/{}_{}.png".format(st, me))
