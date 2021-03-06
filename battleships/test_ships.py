"""
Unit tests running on battleshiplib.py
"""

from battleshiplib import run

def test_1():
    initinfo = [[2, 2, "w"]]
    rowclues = [4,0,2,1,2,1]
    colclues = [1,0,4,0,3,2]
    ships = [3,2,1]
    results, guesses = run(rowclues, colclues, initinfo, ships)
    assert len(results) == 1
    assert guesses == 0
    assert results[0].grid.tostring() == b'\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x01\x01\x02\x02\x02\x02\x02\x02\x01\x02\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02'

def test_2():
    initinfo = [
             [5, 0, "o"],
             [1, 2, "<"],
             [9, 4, "o"],
             [1, 5, "w"],
             [2, 9, "o"],
             [6, 9, "<"]
            ]
    rowclues = [2,1,3,0,2,3,1,3,0,5]
    colclues = [3,1,2,0,2,1,2,6,1,2]
    ships = [4, 3, 2, 1]
    results, guesses = run(rowclues, colclues, initinfo, ships)
    assert len(results) == 1
    assert results[0].grid.tostring() == b'\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x01\x01\x01\x01\x02\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01'

def test_3():
    initinfo = []
    rowclues = [2,2,1,7,2,1,2,2,0,4]
    colclues = [2,3,0,1,7,2,1,4,0,3]
    ships = [5, 4, 2, 1]
    results, guesses = run(rowclues, colclues, initinfo, ships)
    assert len(results) == 6
    strings = set()
    for i in results:
        strings.add(i.grid.tostring())
    s = ["" for i in range(6)]
    s[0] = b'\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x01\x02\x01\x02\x01\x01\x01\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x01\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x02\x02\x02\x02\x01'
    s[1] = b'\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x01\x02\x01\x02\x01\x01\x01\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x02\x02\x02\x02\x01'
    s[2] = b'\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x01\x02\x01\x02\x01\x01\x01\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x01\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x02\x02\x02\x02\x01'
    s[3] = b'\x02\x02\x02\x01\x02\x02\x02\x01\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x01\x02\x01\x02\x01\x01\x01\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x02\x02\x02\x02\x01'
    s[4] = b'\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x01\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x01\x02\x01\x02\x01\x01\x01\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x01\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x02\x02\x02\x02\x01'
    s[5] = b'\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x01\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x01\x02\x01\x02\x01\x01\x01\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x02\x02\x02\x02\x01'
    for i in s:
        assert i in strings

def test_4():
    initinfo = []
    rowclues = [3,0,2,3,0,2,5,4,2,2]
    colclues = [3,1,2,2,1,3,0,4,6,1]
    ships = [5, 4, 2, 1]
    results, guesses = run(rowclues, colclues, initinfo, ships)
    assert len(results) == 12
    strings = set()
    for i in results:
        strings.add(i.grid.tostring())
    s = ["" for i in range(12)]
    s[0] = b'\x01\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x01\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    s[1] = b'\x01\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x01\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    s[2] = b'\x01\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    s[3] = b'\x02\x02\x01\x02\x02\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    s[4] = b'\x02\x02\x02\x01\x02\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    s[5] = b'\x02\x02\x02\x01\x02\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    s[6] = b'\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    s[7] = b'\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x01\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x01\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    s[8] = b'\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    s[9] = b'\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x02\x02\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    s[10] = b'\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x01\x02\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x01\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    s[11] = b'\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x01\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x01\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x01\x02\x01\x01\x02\x01\x01\x02\x01\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02'
    for i in s:
        assert i in strings

def test_5():
    initinfo = []
    rowclues = [2,0,2,7,1,1,4,1,2,3]
    colclues = [2,5,0,1,3,1,5,2,0,4]
    ships = [5, 4, 2, 1]
    results, guesses = run(rowclues, colclues, initinfo, ships)
    assert len(results) == 5
    strings = set()
    for i in results:
        strings.add(i.grid.tostring())
    s = ["" for i in range(5)]
    s[0] = b'\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x01\x02\x01\x01\x02\x02\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x01\x02\x02\x02'
    s[1] = b'\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x01\x02\x02\x01\x02\x02\x01\x02\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x01\x01\x01\x02\x02\x02\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x02\x02\x02\x01'
    s[2] = b'\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x01\x01\x02\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x01\x01\x01\x02\x02\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x01\x02\x02\x02'
    s[3] = b'\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x01\x02\x02\x01\x02\x01\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x01\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x01\x01\x01\x02\x02\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x01\x02\x02\x02'
    s[4] = b'\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x01\x02\x02\x01\x02\x02\x01\x02\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x01\x02\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x01\x01\x01\x01\x02\x02\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x01\x01\x02\x01\x02\x02\x02'
    for i in s:
        assert i in strings

def test_5b():
    initinfo = []
    rowclues = [2,0,2,7,1,1,4,1,2,3,0]
    colclues = [2,5,0,1,3,1,5,2,0,4]
    ships = [5, 4, 2, 1]
    results, guesses = run(rowclues, colclues, initinfo, ships)
    assert len(results) == 5

    rowclues = [2,0,2,7,1,1,4,1,2,3]
    colclues = [2,5,0,1,3,1,5,2,0,4,0]
    results, guesses = run(rowclues, colclues, initinfo, ships)
    assert len(results) == 5

def test_6():
    initinfo = []
    rowclues = [3, None, 0, None, None]
    colclues = [1, None, 3]
    ships = [0, 1, 1]
    results, guesses = run(rowclues, colclues, initinfo, ships)
    assert len(results) == 1
    assert results[0].grid.tostring() == b'\x01\x02\x02\x02\x02\x01\x02\x02\x02\x02\x01\x02\x02\x01\x01'

def test_7():
    rowclues = [None] * 10
    colclues = [None] * 10
    initinfo = [
        [4, 0, "#"],
        [7, 1, ">"],
        [3, 2, "#"],
        [0, 3, "#"],
        [2, 4, "#"],
        [4, 4, "#"],
        [7, 3, "#"],
        [1, 6, "#"],
        [3, 6, "#"],
        [4, 6, "#"],
        [5, 6, "#"],
        [7, 6, "#"],
        [6, 8, ">"],
        [3, 9, "v"]
    ]
    ships = [4, 3, 2, 1]
    results, guesses = run(rowclues, colclues, initinfo, ships)
    assert len(results) == 1
    assert results[0].grid.tostring() == b'\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x02\x02\x02\x02\x02\x02\x01\x02\x01\x02\x01\x02\x01\x01\x01\x02\x02\x02\x01\x02\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x01\x02\x01\x02\x02\x01\x02\x02\x02\x02\x02\x02\x01\x02\x02\x01\x02\x01\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02'
