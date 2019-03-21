from __future__ import annotations
from typing import no_type_check, get_type_hints

@no_type_check
def example(
        a: {color: 'blue', adapt: int},
        b: {color: 'red', adapt: float}
) -> {'print': True}:
    return (a, b)

if __name__ == '__main__':
    def adapt_int(val):
        try:
            return int(val)
        except ValueError:
            return 0

    def adapt_float(val):
        try:
            return float(val)
        except ValueError:
            return 0.0

    evaluated = {
        key: eval(value, {
            'int': adapt_int,
            'float': adapt_float,
            'color': 'color',
            'adapt': 'adapt'
        })
        for key, value in example.__annotations__.items()
    }

    print(evaluated)
