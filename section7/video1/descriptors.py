class RuntimeValidated:
    def __init__(self, validator):
        self.validator = validator

    def __set_name__(self, owner, name):
        self.attr_name = f"_runtimevalidated_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.attr_name)

    def __set__(self, instance, value):
        if self.validator(value):
            return setattr(instance, self.attr_name, value)
        raise AttributeError(f"Validation failed: {value}")

    def __delete__(self, instance):
        return delattr(instance, self.attr_name)


def acceptable_url(value):
    if not isinstance(value, str):
        return False

    val = value.lower()

    if not (val.startswith("http://") or val.startswith("https://")):
        return False

    return True


class ArbitraryThing:
    home_page = RuntimeValidated(acceptable_url)
    news_page = RuntimeValidated(acceptable_url)


if __name__ == '__main__':
    arb = ArbitraryThing()

    arb.home_page = 'https://scistarter.org/'
    arb.news_page = 'http://slashdot.org/'

    print('Home page is', arb.home_page)

    try:
        arb.home_page = 'gopher://nope'
    except AttributeError:
        print("Couldn't use a Gopher home page (which is correct)")
    else:
        print("Gopher home page accepted")
