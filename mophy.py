# python3
import re
import pymorphy2


def main():
    m = pymorphy2.MorphAnalyzer()  # result_type=None)

    s = 'сьешь этих мягких французких булок да выпей чаю'
    for word in re.findall(r'\w+', s):
        for i in m.parse(word):
            print(i.tag.cyr_repr, i)
            if i.score > 0.33:
                break
        print()

    print(m.parse('стол')[0].inflect({m.cyr2lat('рд')}))


if __name__ == '__main__':
    main()
