from dataclasses import dataclass

@dataclass
class Animal:
    name: str
    environment: str
    mean_weight: float

if __name__ == '__main__':
    a = Animal(name = 'Giraffe', environment = 'savannah', mean_weight = 2628)
    b = Animal(name = 'Tiger', environment = 'wooded', mean_weight = 900)
    c = Animal(name = 'Giraffe', environment = 'savannah', mean_weight = 2628)
    print(a, '==', b, ':', a == b)
    print(a, '==', c, ':', a == c)
