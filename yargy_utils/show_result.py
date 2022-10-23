from ipymarkup import show_span_ascii_markup as show_markup
from yargy import (
    Parser,
    or_, rule,
    and_
)
import json


# подчёркивает конструкции, соответствующие правилу
def show_matches(rule, *lines):
    parser = Parser(rule)
    for line in lines:
        matches = parser.findall(line)
        spans = [_.span for _ in matches]
        show_markup(line, spans)


# выводит атрибуты сущности
def show_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))
