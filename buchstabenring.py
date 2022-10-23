import sys
from argparse import ArgumentParser

def candidates(vocab, letters, bigrams):
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

def find_solution(vcb, letters):
    letters_set = set(letters)
    # encode the ring in form of bigrams
    bigrams = create_bigrams(letters)
    # add bigrams from both directions of the ring
    bigrams.update(create_bigrams(letters[::-1]))
    # filter candidates from dictionary
    cands = candidates(vcb, letters_set, bigrams)
    print(f"created {len(bigrams)} bigrams, {len(cands)} candidates")

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
                print(cand1, cand2)


if __name__ == "__main__":
    parser = ArgumentParser(description="Buchstabenringloeser")
    parser.add_argument("lettersets", metavar="STR", type=str, nargs='+')
    parser.add_argument("-w", "--wordfile", type=str, dest="wordfile", metavar="FILE",
                        help="file w/ words")
    options = parser.parse_args()

    vcb = set()
    with open(options.wordfile) as stream:
        for line in stream:
            vcb.add(line.strip())
    print(f"loaded {len(vcb)} words")

    for letters in options.lettersets:
        letters = letters.lower()
        print(f"letters: {letters}")
        find_solution(vcb, letters)
        print("="*32)
