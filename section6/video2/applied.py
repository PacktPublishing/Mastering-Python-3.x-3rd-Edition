from __future__ import annotations

import colorama
from typing import no_type_check_decorator

RESET = colorama.Fore.RESET
COLORS = {
    "red": colorama.Fore.RED + colorama.Style.BRIGHT,
    "green": colorama.Fore.GREEN + colorama.Style.BRIGHT,
    "yellow": colorama.Fore.YELLOW + colorama.Style.BRIGHT,
    "blue": colorama.Fore.BLUE + colorama.Style.BRIGHT,
    "magenta": colorama.Fore.MAGENTA + colorama.Style.BRIGHT,
    "cyan": colorama.Fore.CYAN + colorama.Style.BRIGHT,
    "white": colorama.Fore.WHITE + colorama.Style.BRIGHT,
    "standard": RESET,
}

colorama.init()

available = {}


class AdaptionRetry(Exception):
    pass


def adapt_int(val):
    try:
        return int(val)
    except:
        raise AdaptionRetry from None


def adapt_float(val):
    try:
        return float(val)
    except:
        raise AdaptionRetry from None


@no_type_check_decorator
def interface(func):
    annotations = {
        key: eval(value, {
            "int": adapt_int,
            "float": adapt_float,
            'color': 'color',
            'adapt': 'adapt',
            'print': 'print'
        })
        for key, value in func.__annotations__.items()
    }

    if "return" not in annotations:
        annotations["return"] = {}

    # Get a name value from the annotations, or fall back to the
    # function's original name in the code
    name = annotations["return"].get("name", func.__name__)

    def invoker():
        args = {}

        for param, notes in annotations.items():
            if param == "return":
                continue

            adapt = notes.get("adapt", (lambda x: x))
            color = COLORS.get(notes.get("color", "standard"), RESET)

            while param not in args:
                try:
                    args[param] = adapt(input(f"{color}{param}{RESET}: "))
                except AdaptionRetry:
                    pass

        result = func(**args)

        if annotations["return"].get("print", False):
            print(result)

        return result

    available[name] = invoker
    func.invoker = invoker

    return func


@interface
def annual(
    year: {color: "blue", adapt: int},
    mean: {color: "red", adapt: float}
) -> {print: True}:
    return (year, mean)


@interface
def current(price: {color: "green", adapt: float}) -> {print: True}:
    return price * 27.312


@interface
def help() -> {print: True}:
    return ", ".join(available.keys())

@interface
def quit():
    pass

def main():
    cmd = "noop"

    while cmd != "quit":
        cmd = input("> ")
        if cmd in available:
            available[cmd]()


if __name__ == "__main__":
    main()
