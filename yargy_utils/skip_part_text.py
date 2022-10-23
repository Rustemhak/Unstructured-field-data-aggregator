# для пропуска части текста
def is_inside_span(token, span):
    token_span = token.span
    return span.start <= token_span.start and token_span.stop <= span.stop


def select_span_tokens(tokens, spans):
    for token in tokens:
        if any(is_inside_span(token, _) for _ in spans):
            yield token
