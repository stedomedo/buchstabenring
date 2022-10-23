import sys
import re

class Vocab:
    RE = re.compile("^[A-Za-zÄÖÜäöüß][a-zäöüß]{3,}$")

    def __init__(self, fname, cutoff=-1):
        self._vcb = {}
        with open(fname) as stream:
            for line in stream:
                sline = line.split()
                w = sline[0]
                if len(sline) != 2 or not Vocab.RE.search(w):
                    continue
                c = int(sline[1])
                if cutoff >= 0 and c < cutoff:
                    continue
                if w not in self._vcb:
                    self._vcb[w] = 0
                self._vcb[w] += c

    def __iter__(self):
        for k, _ in sorted(self._vcb.items(), key=lambda x: x[1], reverse=True):
            yield k

    def __len__(self):
        return len(self._vcb)

    def score(self, *args):
        s = 0
        for w in args:
            s += self._vcb.get(w, 0)
        return s

    def dump(self, outfile):
        with open(outfile, 'w') as stream:
            for k, v in self._vcb.items():
                print(f"{k} {v}", file=stream)

