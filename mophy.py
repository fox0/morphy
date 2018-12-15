# python3
import re
import logging
import pymorphy2
from yandex_speech import text_to_voice

log = logging.getLogger(__name__)


def main():
    m = pymorphy2.MorphAnalyzer()  # result_type=None)

    s = 'сь+ешь этих мягких франц+узких булок - да выпей чаю'
    for word in re.findall(r'\w+', s.replace('+', '')):
        for i in m.parse(word):
            print(i.tag.cyr_repr, i)
            if i.score > 0.33:
                break
        print()

    print(m.parse('стол')[0].inflect({m.cyr2lat('рд')}))
    text_to_voice(s)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s %(filename)s:%(lineno)d: %(message)s',
                        level=logging.DEBUG)
    main()
