from natasha import Segmenter, Doc


def segment_to_sent(text: str) -> list:
    '''
    Сегментирует текст на предложения
    :param text: исходный текст
    :return: список предложений
    '''
    segmenter = Segmenter()
    doc = Doc(text)
    doc.segment(segmenter)
    sentences = [_.text for _ in doc.sents]
    # пока отключим подсегментацию для лучшего поддержания контекста
    # sentences = [sent.split(';') if ';' in sent and ':' in sent else sent for sent in sentences ]
    return sentences
