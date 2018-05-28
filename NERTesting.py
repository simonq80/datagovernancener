import sys
import re
import subprocess
import os
import configparser
import random
import shutil
import csv
import collections
import numpy
import pickle


cfg = configparser.ConfigParser()
cfg.read('test_config.cfg')
beta = float(cfg['MAIN']['f-beta'])

def test(lines, config, testsize=0.4, offset=0, name=0):
    # Start and end points of test and train splits
    ll = len(lines)
    train0start = 0
    teststart = int(offset * ll)
    train1start = int((offset + testsize) * ll)
    train1end = ll
    train = lines[train0start:teststart] + lines[train1start:train1end]
    test = lines[teststart:train1start]
    return run_ner(train, test, config, name)

def crossval(data, folds, config):
    # Runs test with incrementing offsets and averages results
    p = []
    r = []
    f1 =[]
    for i in range(0, folds):
        (a, b, c) = test(data, config, testsize=1/folds, offset=i/folds, name=i)
        print("Fold {}\n  P:{} R:{} F{}:{}".format(i+1, a, b, beta, c))
        p.append(a)
        r.append(b)
        f1.append(c)
    print("Average\n  P:{} R:{} F{}:{}".format(numpy.mean(p), numpy.mean(r), beta, numpy.mean(f1)))
    print("Standard Deviation\n  P:{} R:{} F{}:{}".format(numpy.std(p), numpy.std(r), beta, numpy.std(f1)))
    return (numpy.std(p), numpy.std(r), numpy.std(f1))


def bootstrap(data, config):
    n = len(data)
    train = []
    for i in range(0, n):
        train.append(data[random.randint(0, n-1)])
    test = [d for d in data if d not in train]

    return run_ner(train, test, config)

def run_ner(train, test, config, name=0):

    with open("trainfile.txt", "w") as output:
        output.writelines(train)
    with open("testfile.txt", "w") as output:
        output.writelines(test)

    # Train and test via command line
    nertestcommand = "java -cp stanford-ner/stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -trainFile trainfile.txt -prop {} -testFile testfile.txt".format(config)
    out = subprocess.run(nertestcommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    '''try:
        os.remove('trainfile.txt')
        os.remove('testfile.txt')
    except:
        pass'''

    with open("NEROutput/NEROutput{}.tok".format(name), "w") as output:
        output.write(str(out.stdout, 'utf-8'))

    out = str(out.stderr, 'utf-8')
    pattern = r'Totals\t(......)\t(......)\t(......)'
    # Extract results from stderr with regex
    reg = re.search(pattern, str(out), re.M|re.I)
    p = float(reg.group(1))
    r = float(reg.group(2))
    return (p, r, f_beta(p, r))

def f_beta(p, r):
    if p == 0 or r == 0:
        return 0
    return ((p * r) / ((beta * beta * p) + r)) * (1.0 + (beta * beta))

def entity_stats(folder_name='NEROutput', default_other='O'):
    pairs = []
    for filename in os.listdir(folder_name):
        with open(os.path.join(folder_name, filename)) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                if len(row) == 3:
                    pairs.append((row[1], row[2]))
    def arr():
        # correct | relevant | returned
        return [0,0,0]
    d = collections.defaultdict(arr)
    for pair in pairs:
        d[pair[0]][1] += 1
        d[pair[1]][2] += 1
        if pair[0] == pair[1]:
            d[pair[0]][0] += 1

    complexity = entity_complexity(folder_name)

    to_return = {}

    for k in sorted(d.keys()):
        if k != default_other:
            p = 0 if d[k][2] == 0 else d[k][0]/d[k][2]
            r = 0 if d[k][1] == 0 else d[k][0]/d[k][1]
            f = f_beta(p, r)
            unique_words = complexity[k]['unique_words']
            avg_len = complexity[k]['avg_len']
            len_std = complexity[k]['len_std']
            s = '''{}

Annotated: {}
Unique Word Count: {}
Average Length: {}
Length Standard Deviation: {}

Predicted: {}
Precision: {}
Recall: {}
F-{}: {}
            '''
            s = s.format(k, d[k][1], unique_words, avg_len, len_std, d[k][2], p, r, beta, f)
            to_return[k] = {
                'annotated': d[k][1],
                'unique_words': unique_words,
                'avg_len': avg_len,
                'len_std': len_std,
                'predicted': d[k][2],
                'precision': p,
                'recall': r,
                'beta': beta,
                'f-measure': f
            }
            print(s)

    return to_return

def entity_complexity(folder_name='NEROutput'):
    ents = []
    for filename in os.listdir(folder_name):
        with open(os.path.join(folder_name, filename)) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                if len(row) == 3:
                    ents.append((row[1], row[0]))

    def arr():
        return []
    avg_len = collections.defaultdict(arr)

    l = 1
    for i in range(1, len(ents)):
        if ents[i-1][0] == ents[i][0]:
            l += 1
        else:
            avg_len[ents[i-1][0]].append(l)
            l = 1

    for k in avg_len:
        avg_len[k] = (numpy.mean(avg_len[k]), numpy.std(avg_len[k]))

    def a():
        return set()
    unique_words = collections.defaultdict(a)

    for x in ents:
        unique_words[x[0]].add(x[1])

    for k in unique_words:
        unique_words[k] = len(unique_words[k])

    to_return = dict()
    for k in avg_len:
        to_return[k] = {'unique_words': unique_words[k], 'avg_len': avg_len[k][0], 'len_std': avg_len[k][1]}

    return to_return





if __name__ == "__main__":
    c = configparser.ConfigParser()
    c.read('test_config.cfg')
    c = c['MAIN']
    configs = c['ner_configs'].split('\n')
    files = c['test_data'].split('\n')
    if c['test_type'] == 'cross_validation':
        print('{} FOLD CROSS VALIDATION'.format(c['folds']))
    if c['test_type'] == 'bootstrap':
        print('BOOTSTRAP')
    if c['test_type'] == 'split':
        print('{}:{} SPLIT TESTING'.format(c['split'], 100-int(c['split'])))
    print('\nTEST FILES:')
    [print('  {}'.format(f)) for f in files]
    print('\nCONFIG FILES:')
    [print('  {}'.format(f)) for f in configs]

    data = []
    for file in files:
        with open(file, "r") as input:
            for line in input:
                data.append(line)

    shutil.rmtree('NEROutput')
    os.makedirs('NEROutput')

    for config in configs:

        if c['test_type'] == 'cross_validation':
            print("\nCONFIG : {}".format(config))
            crossval(data, int(c['folds']), config)

        if c['test_type'] == 'split':
            print("\nCONFIG : {}".format(config))
            (p, r, f1) = test(data, config, 1.0 - int(c['split'])/100)
            print("P:{} R:{} F1:{}".format(p, r, f1))

        if c['test_type'] == 'bootstrap':
            print("\nCONFIG : {}".format(config))
            (p, r, f1) = bootstrap(data, config)
            print("P:{} R:{} F1:{}".format(p, r, f1))

        print('\nEntity Statistics\n')
        stats = entity_stats()
        pickle.dump(stats, open('stats.pkl', 'wb'))
