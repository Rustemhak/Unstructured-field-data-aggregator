from yargy.tokenizer import (
    Tokenizer,
    MorphTokenizer,
    EOL
)

# Стандартный токенизатор. Удаляем правило для переводом строк.
# Обычно токены с '\n' только мешаются.
TOKENIZER = MorphTokenizer().remove_types(EOL)


class IdTokenizer(Tokenizer):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    # Используется при инициализации morph_pipeline, caseless_pipeline.
    # Строки-аргументы pipeline нужно разделить на слова. Как разделить,
    # например, "кейс| |dvd-диска" или "кейс| |dvd|-|диска"? Используем стандартный токенизатор.
    def split(self, text):
        return self.tokenizer.split(text)

    # Используется при инициализации предикатов. Например, есть предикат type('INT').
    # Поддерживает ли токенизатор тип INT?
    def check_type(self, type):
        return self.tokenizer.check_type(type)

    @property
    def morph(self):
        return self.tokenizer.morph

    def __call__(self, tokens):
        return tokens


