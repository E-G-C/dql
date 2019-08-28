from dictwax import WaxOn, waxoff, RepWax, RemWax

source = {
        "a":      1,
        "b":      2,
        "c":      [
                {
                        "d0": 5,
                        "d1": 10,
                        "d2": 15
                        },
                {
                        "d4": 4,
                        "d5": 20,
                        "d6": 50
                        }
                ],
        "nested": {
                "e": 5,
                "f": "6",
                "g": {"k": 100, "l": 200, "m": 300}
                },
        "j":      [1, 2, 3, 4, 5, 6, 7, 8, 9]
        }

waxed_dict = {
        'a': WaxOn(1, RepWax({1: 2})),
        'b': WaxOn(None, RemWax([None]))
        }


c = waxoff(source, waxed_dict)
print(c)
