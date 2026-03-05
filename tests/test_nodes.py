import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from nodes import (
    IntToFloat, FloatToInt, IntToString, FloatToString,
    StringToInt, StringToFloat, BoolToInt, IntToBool,
    LogicAND, LogicOR, LogicNOT, LogicXOR, LogicNAND, LogicNOR,
    CompareInt, CompareFloat,
    MathMaxInt, MathMinInt, MathMaxFloat, MathMinFloat, MathClampInt, MathClampFloat,
    SwitchInt, SwitchFloat, SwitchString, SwitchAny,
)


# --- Convert ---

def test_int_to_float():
    assert IntToFloat().convert(3) == (3.0,)

def test_float_to_int():
    assert FloatToInt().convert(3.9) == (3,)

def test_int_to_string():
    assert IntToString().convert(42) == ("42",)

def test_float_to_string():
    assert FloatToString().convert(1.5) == ("1.5",)

def test_string_to_int():
    assert StringToInt().convert("7") == (7,)

def test_string_to_float():
    assert StringToFloat().convert("2.5") == (2.5,)

def test_bool_to_int():
    assert BoolToInt().convert(True) == (1,)

def test_int_to_bool():
    assert IntToBool().convert(1) == (True,)


# --- Logic ---

def test_and():
    assert LogicAND().op(True, True) == (True,)

def test_or():
    assert LogicOR().op(False, True) == (True,)

def test_not():
    assert LogicNOT().op(False) == (True,)

def test_xor():
    assert LogicXOR().op(True, False) == (True,)

def test_nand():
    assert LogicNAND().op(True, True) == (False,)

def test_nor():
    assert LogicNOR().op(False, False) == (True,)


# --- Compare ---

def test_compare_int():
    assert CompareInt().compare(5, 3, ">") == (True,)

def test_compare_float():
    assert CompareFloat().compare(1.0, 1.0, "==") == (True,)


# --- Math ---

def test_max_int():
    assert MathMaxInt().op(3, 7) == (7,)

def test_min_int():
    assert MathMinInt().op(3, 7) == (3,)

def test_max_float():
    assert MathMaxFloat().op(1.5, 2.5) == (2.5,)

def test_min_float():
    assert MathMinFloat().op(1.5, 2.5) == (1.5,)

def test_clamp_int():
    assert MathClampInt().op(150, 0, 100) == (100,)

def test_clamp_float():
    assert MathClampFloat().op(-0.5, 0.0, 1.0) == (0.0,)


# --- Switch ---

def test_switch_int():
    assert SwitchInt().switch(True, 10, 20) == (10,)

def test_switch_float():
    assert SwitchFloat().switch(False, 1.0, 2.0) == (2.0,)

def test_switch_string():
    assert SwitchString().switch(True, "yes", "no") == ("yes",)

def test_switch_any():
    assert SwitchAny().switch(False, "a", "b") == ("b",)
