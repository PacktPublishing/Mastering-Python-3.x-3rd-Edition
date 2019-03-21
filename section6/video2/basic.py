from typing import no_type_check, get_type_hints

@no_type_check
def example(
        a: {'color': 'blue', 'adapt': int},
        b: {'color': 'red', 'adapt': float}
) -> {'print': True}:
    return (a, b)

if __name__ == '__main__':
    print('type hints:', get_type_hints(example))
    print('annotations:', example.__annotations__)
