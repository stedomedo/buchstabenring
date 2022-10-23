import sys
from argparse import ArgumentParser
import spacy
from vocab import Vocab

def candidates(vocab, letters, bigrams, nlp):
    cands = set()
    # read German dictionary
    for word in vocab:
        word_lc = word.lower()
        # check for length >= 4, no consecutive same chars, only allowed chars
        if (len(word) >= 4 and
                not any(c == cn for c, cn in zip(word_lc, word_lc[1:])) and
                set(list(word_lc)).issubset(letters)):
            word_bigrams = create_bigrams(word_lc, is_ring=False)
            # check for no neighboring chars in the ring
            if not word_bigrams.intersection(bigrams):
                # analyze word with spacy
                word_analyzed = nlp(word)
                if len(word_analyzed) > 0:
                    # check if word is lemma to get rid of conjugated verbs, plural nouns, etc.
                    if word == word_analyzed[0].lemma_:
                        cands.add(word)
    return list(cands)

def create_bigrams(letters, is_ring=True):
    bigrams = set()
    # for the ring also combine first and last char
    if is_ring:
        bigrams.add(f"{letters[-1]}{letters[0]}")
    pos = 0
    while pos < len(letters)-1:
        bigram = letters[pos:pos+2]
        bigrams.add(bigram)
        pos += 1
    return bigrams

def find_solution(vcb, letters, nlp, nbest=1000):
    letters_set = set(letters)
    # encode the ring in form of bigrams
    bigrams = create_bigrams(letters)
    # add bigrams from both directions of the ring
    bigrams.update(create_bigrams(letters[::-1]))
    # filter candidates from dictionary
    cands = candidates(vcb, letters_set, bigrams, nlp)
    print(f"created {len(bigrams)} bigrams, {len(cands)} candidates")

    # collect all candidate pairs
    result = []
    for i in range(len(cands)-1):
        for j in range(i+1, len(cands)):
            cand1 = cands[i]
            cand2 = cands[j]
            # second candidate word starts with same letter as the first one ends
            if cand2[-1].lower() == cand1[0].lower():
                # symmetric: swap if cand2 is first and cand1 second
                cand1, cand2 = cand2, cand1
            # both words must cover all chars in the ring
            if cand1[-1].lower() == cand2[0].lower() and set(list(f"{cand1.lower()}{cand2.lower()}")) == letters_set:
                # score candidates with they vocab frequency
                result.append((vcb.score(cand1, cand2), cand1, cand2))

    # print n-best results according to scores
    if result:
        result_str = []
        i = 1
        covered = set()  # store lowercase most-frequent representatives
        for c, cand1, cand2 in sorted(result, reverse=True):
            key = f"{cand1.lower()} {cand2.lower()}"
            if key in covered:
                continue
            result_str.append(f"{i:2d}. {cand1} {cand2} ({c})")
            covered.add(key)
            i += 1
            if i > nbest:
                break
        print(f"showing {len(result_str)}/{len(result)} solutions:")
        print('\n'.join(result_str))
    else:
        print("no results found! all {len(cands)} sorted candidates:")
        print(sorted(cands))



if __name__ == "__main__":
    parser = ArgumentParser(description="Buchstabenringloeser")
    parser.add_argument("lettersets", metavar="STR", type=str, nargs='+')
    parser.add_argument("-w", "--wordfile", type=str, dest="wordfile", metavar="FILE",
                        help="file w/ words (1st token) and frequencies (2nd token)")
    parser.add_argument("-c", "--cutoff", type=int, dest="cutoff", metavar="N", default=10,
                        help="words w/ count below this threshold will be dropped (default: %(default)s)")
    parser.add_argument("-n", "--nbest", type=int, dest="nbest", metavar="N", default=10,
                        help="only show N best results (default: %(default)s)")
    parser.add_argument("-o", "--outfile", type=str, dest="outfile", metavar="FILE",
                        help="write filtered dictionary to output file (for future faster load)")
    options = parser.parse_args()

    nlp = spacy.load('de_core_news_md')
    vcb = Vocab(options.wordfile, options.cutoff)
    print(f"loaded {len(vcb)} words [cutoff={options.cutoff}]")

    for letters in options.lettersets:
        letters = letters.lower()
        print(f"letters: {letters}")
        find_solution(vcb, letters, nlp, options.nbest)
        print("="*32)
    if options.outfile:
        vcb.dump(options.outfile)
        print(f"wrote filtered vocab: {options.outfile}")
