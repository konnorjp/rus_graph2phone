from pathlib import Path
import sys

import hfst
import csv

def get_fst(src):
    tmp = Path('../res/g2p.tmp.hfst')
    print('Compiling twolc rules...', file=sys.stderr)
    hfst.compile_twolc_file(src.name, tmp.name, resolve_left_conflicts=True)
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
    return output

def test(text, truth, src):
    fst = get_fst(src);
    output = []
    print('Processing test words...', file=sys.stderr)
    for index, word in enumerate(text):  # for inword, outword in words:
        outwords = fst.lookup(word)
        output = [w for w, wt in outwords][0]
        if (output != truth[index]):
            print("\n" + word + " => " + output + " != " + truth[index])
        else:
            print('.', end='', flush=True, file=sys.stderr)


def test_words():
    datafile = open('../res/test.csv', 'r')
    datareader = csv.reader(datafile, delimiter=',')
    text = []
    truth = []
    for row in datareader:
        text.append(row[0])
        truth.append(row[1])
    src = Path('../res/g2p.twolc')
    test(text, truth, src)

def test_softness():
    text =  ["ле́т", "зима́",  "я́рус", "све́т",  "питьё",  "бле́дный",  "включа́ть",  "где́",  "гря́зный",  "сле́дующий"]
    truth = ["л'э́т", "з'има́", "а́рус", "св'э́т", "п'ит'о́", "бл'э́дный", "вкл'уча́т'", "гд'э́", "гр'а́зный", "сл'э́дуущий"]
    src = Path('../res/rules_separate/g2ps_softness.twolc')
    test(text, truth, src)

def test_ee_kratkoye():
    text =  ["сле́дующий",   "чле́н",  "чьи́",  "извиня́юсь",    "я́рус",  "чуде́сный",  "мо́ю",  "я́щик",   "питьё",   "съе́л"]
    truth = ["сл'э́дуйущий", "чл'э́н", "ч'йи́", "изв'ин'а́йус'", "йа́рус", "чуд'э́сный", "мо́йу", "йа́щ'ик", "п'ит'йо", "сйэ́л"]
    src = Path('../res/rules_separate/g2ps_ee_kratkoye.twolc')
    test(text, truth, src)

def test_yeri():
    text =  ["живо́т", "щи́",  "сыгра́ть", "мы́шь","ци́кл", "лы́жи", "де́ньги",   "дружи́ть", "чи́щу",  "бо́льший"]
    truth = ["жыво́т", "щ'и́", "сыгра́т'", "мы́ш", "цы́кл", "лы́жы", "д'э́н'г'и", "дружы́т'", "ч'и́щу", "бо́л'шый"]
    src = Path('../res/rules_separate/g2ps_yeri.twolc')
    test(text, truth, src)

def test_akanje():
    text =  ["берегово́й",   "молокосо́с", "острова́", "ка́федра",  "го́лову", "обжо́ра", "ско́вороды", "го́родом", "магази́н",  "грома́дность"]
    truth = ["б'ер'егʌво́й", "мълъкʌсо́с", "ʌстрʌва́", "ка́ф'едръ", "го́лъву", "ʌбжо́ръ", "ско́въръды", "го́ръдъм", "мъгʌз'и́н", "грʌма́днъс'т'"]
    src = Path('../res/rules_separate/g2ps_akanje.twolc')
    test(text, truth, src)

def test_tense_ya_ye():
    text =  ["проче́сть",   "сове́тница",    "две́сти",    "боле́л",  "боле́ли",   "де́ле",   "све́тит",   "ча́сть",   "вычисля́ть",    "я́щик"]
    truth = ["проч'э̂с'т'", "сов'э̂т'н'ица", "дв'э̂с'т'и", "бол'э́л", "бол'э̂л'и", "д'э̂л'е", "св'э̂т'ит", "ч'а̂с'т'", "выч'ис'л'а̂т'", "йа̂щ'ик"]
    src = Path('../res/rules_separate/g2ps_tense_ya_ye.twolc')
    test(text, truth, src)
    # Depends on Softness Assimilation

def test_ikanje():
    text =  ["язы́к",  "ерунда́",  "еди́нственно",    "чепуха́",  "телефо́н",   "берегово́й",   "весна́",  "серебро́",   "о́череди",    "пятьдеся́т"]
    truth = ["йизы́к", "йьрунда́", "йид'и́нств'ьнно", "ч'ьпуха́", "т'ьл'ифо́н", "б'ьр'ьгово́й", "в'исна́", "с'ьр'ибро́", "о́ч'ьр'ьд'и", "п'ьт'д'ис'а́т"]
    src = Path('../res/rules_separate/g2ps_ikanje.twolc')
    test(text, truth, src)
    # Depends on EeKratkoye

def test_ykanje():
    text =  ["уценена́",  "жесто́кий",  "шелуха́", "шесто́й", "ше́рсть", "це́лый", "же́ртва", "шевели́ться",   "целико́м",  "кольцево́й"]
    truth = ["уцън'ена́", "жысто́к'ий", "шълуха́", "шысто́й", "шэ́рст'", "цэ́лый", "жэ́ртва", "шъв'ел'и́тс'я", "цъл'ико́м", "кол'цыво́й"]
    src = Path('../res/rules_separate/g2ps_ykanje.twolc')
    test(text, truth, src)

def test_final_devoicing():
    text =  ["пло́д", "гла́з", "зу́б", "но́ж", "дру́г", "сто́рож", "отре́жь",  "ся́дь",  "до́м", "ста́р"]
    truth = ["пло́т", "гла́с", "зу́п", "но́ш", "дру́к", "сто́рош", "от'р'э́ш", "с'а́т'", "до́м", "ста́р"]
    src = Path('../res/rules_separate/g2ps_final_devoicing.twolc')
    test(text, truth, src)

def test_cluster_unvoiced_assimilation():
    text =  ["тру́бка", "ло́дка", "вку́с", "коро́бка", "ска́зка", "второ́й"]
    truth = ["тру́пкъ", "ло́ткъ", "фку́с", "кʌро́пкъ", "ска́скъ", "фтʌро́й"]
    src = Path('../res/rules_separate/g2ps_cluster_unvoiced_assimilation.twolc')
    test(text, truth, src)

def test_cluster_voice_assimilation():
    text =  ["про́сьба", "вокза́л", "сгоре́л",  "све́т",  "сво́лочь", "сде́лал"]
    truth = ["про́з'бъ", "вʌгза́л", "згʌр'э́л", "св'э́т", "сво́лоч",  "зд'э́лал"]
    src = Path('../res/rules_separate/g2ps_cluster_voiced_assimilation.twolc')
    test(text, truth, src)

def test_softness_assimilation():
    text =  ["ча́сть",   "вперёд",    "две́рь",  "вме́сте",     "ски́дка",  "клева́ть",  "твёрдая",  "присе́сть",    "проче́сть",   "сове́тница"]
    truth = ["ч'а́с'т'", "в'п'ер'о́д", "дв'э́р'", "в'м'э́с'т'е", "ск'и́тка", "кл'ева́т'", "тв'о́рдая", "пр'ис'э́с'т'", "проч'э́с'т'", "сов'э́т'н'ица"]
    src = Path('../res/rules_separate/g2ps_softness_assimilation.twolc')
    test(text, truth, src)


def test_all_rules():
    test_softness()
    test_ee_kratkoye()
    test_yeri()
    test_akanje()
    test_tense_ya_ye()
    test_ikanje()
    test_ykanje()
    test_final_devoicing()
    test_cluster_unvoiced_assimilation()
    test_cluster_voice_assimilation()
    test_softness_assimilation()

if __name__ == '__main__':
    switcher = {
        "words": test_words,
        "all_rules": test_all_rules,
        "softness": test_softness,
        "ee_kratkoye": test_ee_kratkoye,
        "yeri": test_yeri,
        "akanje": test_akanje,
        "tense_ya_ye": test_tense_ya_ye,
        "ikanje": test_ikanje,
        "ykanje": test_ykanje,
        "final_devoicing": test_final_devoicing,
        "cluster_unvoiced_assimilation": test_cluster_unvoiced_assimilation,
        "cluster_voice_assimilation": test_cluster_voice_assimilation,
        "softness_assimilation": test_softness_assimilation
    }

    arg = "words"
    if len(sys.argv) > 1:
        arg = sys.argv[1]

    func = switcher.get(arg)
    func()
