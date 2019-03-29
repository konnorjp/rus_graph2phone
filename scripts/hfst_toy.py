import csv
from pathlib import Path
import sys

import hfst


def read_from_csv():
    datafile = open('test.csv', 'r')
    datareader = csv.reader(datafile, delimiter=',')
    data = []
    for row in datareader:
        data.append((row[0], row[1]))
    return data


def get_fst():
    src = Path('g2p.twolc')
    tmp = Path('g2p_from_py.tmp.hfst')
    final = Path('g2p_from_py.hfstol')
    if (not tmp.exists()) or (src.stat().st_mtime > tmp.stat().st_mtime):
        print('Compiling twolc rules...', file=sys.stderr)
        hfst.compile_twolc_file(src.name, tmp.name,
                                resolve_left_conflicts=True)
    if (not final.exists()) or not (src.stat().st_mtime <
                                    tmp.stat().st_mtime <
                                    final.stat().st_mtime):
        print('Preparing rule transducers for composition...', file=sys.stderr)
        rule_fsts_stream = hfst.HfstInputStream(tmp.name)
        rule_fsts = [t for t in rule_fsts_stream]
        print('Creating universal language FST...', file=sys.stderr)
        output = hfst.regex('?* ;')
        print('Compose-intersecting rules with universal FST...',
              file=sys.stderr)
        output.compose_intersect(rule_fsts)
        print('Optimizing for fast lookup...', file=sys.stderr)
        output.lookup_optimize()
        print('Writing out final FST...', file=sys.stderr)
        output.write_to_file(final.name)
    else:
        ol_fst_stream = hfst.HfstInputStream(final.name)
        output = next(ol_fst_stream)
    return output


def test_RPT(words):
    fst = get_fst()
    output = []
    print('Processing test words...', file=sys.stderr)
    for inword in words:  # for inword, outword in words:
        print('.', end='', flush=True, file=sys.stderr)
        outwords = fst.lookup(inword)
        output.append(f'{inword}\n{", ".join([w for w, wt in outwords])}\n\n')
    return output


if __name__ == '__main__':
    in_file = Path('/tmp/g2p_lex-test.txt')
    with in_file.open() as f:
        test_words = [line.strip() for line in f]
    text = ['ся́ду', 'твёрдый', 'ю́бка', 'ба́юшки', 'опя́ть', 'съе́сть', 'жи́ть']
    out_file = Path('/tmp/output_g2p_hfst_from_py.txt')
    with out_file.open('w') as f:
        print(''.join(test_RPT(test_words)), file=f)
    print(f'Output can be viewed using...\nless {out_file}')
