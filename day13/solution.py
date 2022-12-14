from pathlib import Path
from functools import cmp_to_key


path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read()

# replace all numbers with letters
input = input.replace("10", "K").replace(",", "")
pairs = [pair.split("\n") for pair in input.split("\n\n")]
pairs = [["".join([chr(int(c) + 65) if c not in "[]K" else c
    for c in signal])
    for signal in pair]
    for pair in pairs]


def sign(n):
    if n < 0:
        return -1
    if n > 0:
        return 1
    return 0


def compare_signals(left, right):
    return compare_chars([left, right], 0)


def compare_chars(pair, index=0):
    l, r = pair[0][index], pair[1][index]

    # skip to next pair of characters if the characters are the same
    if l == r:
        return compare_chars(pair, index+1)

    if not "[" in (l, r) and not "]" in (l, r):
        # compare numbers (A-K)
        return sign(ord(l) - ord(r))
    elif "]" in (l, r):
        # chars A-K are smaller than ]
        return -sign(ord(l) - ord(r))
    else:
        # shift the main signal forward by 1,
        # add a ] next to the int on the other signal
        # and restart comparing from current index
        # ie [A[C]]   -> A][C]]
        #    [[A][B]] -> A][B]]
        new_pair = pair[:]
        main = (l, r).index("[")
        other = 1-main
        new_pair[other] = new_pair[other][index] + "]" + new_pair[other][index+1:]
        new_pair[main] = new_pair[main][index+1:]
        return compare_chars(new_pair, 0)


def part1():
    differences = [i+1 for i, pair in enumerate(pairs) if compare_signals(*pair) < 0]
    return sum(differences)


def part2():
    divider_signals = ["[[C]]", "[[G]]"]
    all_signals = [signal for pair in pairs for signal in pair] + divider_signals
    all_signals.sort(key=cmp_to_key(compare_signals))

    return (all_signals.index(divider_signals[0])+1) * (all_signals.index(divider_signals[1])+1)


print(part1())
print(part2())
