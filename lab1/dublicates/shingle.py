import binascii


def canonize(text):
    stop_symbols = '.,!?:;-\n\r()"\'[]{}|'

    stop_words = ('це', 'як', 'так',
                  'і', 'в', 'над',
                  'до', 'не', 'ні',
                  'на', 'але', 'за',
                  'то', 'з', 'чи',
                  'а', 'у', 'від',
                  'із', 'для', 'о',
                  'же', 'ну', 'ви',
                  'б', 'що', 'хто',
                  'він', 'вона', 'би')

    return [x for x in
            [y.strip(stop_symbols)
             for y in text.lower().split()] if x and (x not in stop_words)]


def get_shingles(words, shingle_len=10):
    shingles = []
    for i in range(len(words) - (shingle_len - 1)):
        shingles.append(binascii.crc32(
            ' '.join([x for x in words[i:i + shingle_len]]).encode()))

    return shingles


def get_shingles_similarity(hashes1, hashes2):
    same = 0
    for i in range(len(hashes1)):
        if hashes1[i] in hashes2:
            same += 1

    return same * 2 / float((len(hashes1) + len(hashes2)) or 1)


def get_texts_similarity(text1, text2):
    return get_shingles_similarity(
        get_shingles(canonize(text1)), get_shingles(canonize(text2)))
