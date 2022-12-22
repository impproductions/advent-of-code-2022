from pathlib import Path

path = Path(__file__).parent / "example.txt"
with path.open() as file:
    input = file.read().splitlines()

jobs = {job.split(": ")[0]: job.split(": ")[1] for job in input}
UNKNOWN = "X"
ROOT_ID, HUMAN_ID = "root", "humn"


def get_full_formula(actor, jobs, unknown_actor=None):
    job = jobs[actor]
    l, r, op = job[:4], job[7:], job[4:7]

    if actor == unknown_actor:
        return actor
    if job.isdigit():
        return job

    l = get_full_formula(l, jobs, unknown_actor) if not l.isdigit() else l
    r = get_full_formula(r, jobs, unknown_actor) if not r.isdigit() else r

    return "(" + l + op + r + ")"


def invert_formula(l, r, op):
    known = l if r == UNKNOWN else r
    if op == "*":
        return UNKNOWN + " / " + known
    if op == "+":
        return UNKNOWN + " - " + known
    if op == "-":
        return UNKNOWN + " + " + r if r == known else known + " - " + UNKNOWN
    if op == "/":
        return UNKNOWN + " * " + r if r == known else known + " / " + UNKNOWN


def get_inverse_formula(actor, jobs, unknown_actor=None):
    parent = actor
    pipeline = {}
    while parent != ROOT_ID:
        for candidate in jobs:
            if parent in jobs[candidate]:
                a, b, op = jobs[candidate][:4], jobs[candidate][7:], jobs[candidate][5]
                a = str(eval(get_full_formula(a, jobs, unknown_actor))
                        ) if not a in pipeline and not a == unknown_actor else UNKNOWN
                b = str(eval(get_full_formula(b, jobs, unknown_actor))
                        ) if not b in pipeline and not b == unknown_actor else UNKNOWN

                pipeline[candidate] = invert_formula(a, b, op)
                parent = candidate
                break

    del (pipeline[ROOT_ID])

    whole = ROOT_ID
    for key in reversed(pipeline.keys()):
        whole = "(" + pipeline[key].replace("X", whole) + ")"

    return whole


def part1():
    return eval(get_full_formula(ROOT_ID, jobs))


def part2():
    left_formula = get_full_formula(jobs[ROOT_ID][:4], jobs, HUMAN_ID)
    right_formula = get_full_formula(jobs[ROOT_ID][7:], jobs, HUMAN_ID)
    known = right_formula if HUMAN_ID in left_formula else left_formula

    x = get_inverse_formula(HUMAN_ID, jobs, HUMAN_ID).replace(ROOT_ID, known)

    return eval(x)


print(part1())
print(part2())
