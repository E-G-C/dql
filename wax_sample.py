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

#  Rename the class as DWaxer?
#  add two kind o patches , a RemovePatch and a ReplacePatch
#  add them to the WaxOn call and decide based on the class type
#  it will look like this:
#
#      waxed_dict = { 'a': WaxOn([value], ReplacePatch(replacement dictionary)]
#      waxed_dict = { 'a' : WaxOn([value], RemovePatch([list of values to remove from dictionary)}
#
#
#
#
#


c = waxoff(source, waxed_dict)
print(c)
