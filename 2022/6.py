from tools import get_data
from aocd import submit

indata = get_data(6, 2022)

def detect_start(data, charcount):
    data = list(data[0])
    for offset in range(len(data) - charcount):
        buffer = data[offset:offset+charcount]
        if len(set(buffer)) == charcount:
            return offset+charcount

assert(detect_start(indata, 4) == 10)
assert(detect_start(indata, 14) == 29)

indata = get_data(6,2022, True)

answer_a = detect_start(indata, 4)
answer_b = detect_start(indata, 14)

submit(answer_a, part='a', day=6, year=2022)
submit(answer_b, part='b', day=6, year=2022)