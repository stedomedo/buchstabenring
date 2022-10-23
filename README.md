# Buchstabenring

This is a solver to [Buchstabenring](https://www.sueddeutsche.de/raetsel/buchstabenring/), 
a puzzle by Süddeutschen Zeitung.

Here are the rules (translated from the website):

- Words must consist of at least 4 letters.
- Letters can be used multiple times, however, the previously used letter and its neighbors in the ring are prohibited.
- The next word starts with the same letter as the previous one ends.
- There is always a 2-word solution.
- All words in the Duden are allowed, incl. names and abbreviations.
- Conjugated or plural forms of words are prohibited, except when they are an actual keyword in the Duden.
- Words that contain a punctuation mark are prohibited.

This solver treats the puzzle similarly to a search problem.
A vocabulary is filtered by letter-bigrams that serve as some kind of index to extract candidate words
that can be created within the ring.
Those candidates are then combined and checked for the remaining rules by the puzzle.


### Solution with simple vocabulary

If you have a German vocabulary file at hand, this one is quick and simple.
I used a parsed ispell dictionary, which is pretty old but serves the purpose.
Plural forms or conjugated verbs may be in the list of solutions and you will need to filter out those manually.

```
usage: buchstabenring.py [-h] [-w FILE] STR [STR ...]

Buchstabenringloeser

positional arguments:
  STR

optional arguments:
  -h, --help            show this help message and exit
  -w FILE, --wordfile FILE
                        file w/ words
```

Example with a vocabulary file `ngerman` and 4 rings:
```
python3 buchstabenring.py -w ngerman purlifäbenmg hilckpotnras msbuktnoficl tnyfhipmsagj
```

### Solution with vocabulary & frequencies

In case you don't have a vocabulary file at hand, you can create one from large texts.
Count the word frequencies which will help later with filtering out rare, nonsense or misspelled words.
The algorithm is the same as above but in addition by lemmatized from (using `spacy`)
and word frequencies are used to sort and return top n results instead of all.

```
usage: buchstabenring_ext.py [-h] [-w FILE] [-c N] [-n N] [-o FILE]
                             STR [STR ...]

Buchstabenringloeser

positional arguments:
  STR

optional arguments:
  -h, --help            show this help message and exit
  -w FILE, --wordfile FILE
                        file w/ words (1st token) and frequencies (2nd token)
  -c N, --cutoff N      words w/ count below this threshold will be dropped
                        (default: 10)
  -n N, --nbest N       only show N best results (default: 10)
  -o FILE, --outfile FILE
                        write filtered dictionary to output file (for future
                        faster load)
```

Example with a vocab file `de.all.vocf.min20-filt` and 4 rings:
```
python buchstabenring_ext.py -w de.all.vocf.min20-filt purlifäbenmg hilckpotnras msbuktnoficl bhünsekcirfl
```

