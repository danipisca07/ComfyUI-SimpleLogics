# SimpleLogics - ComfyUI node library for logic, math, and type conversion


# --- Type Conversion ---

class IntToFloat:
    DESCRIPTION = "Converts an integer to a float."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("INT", {"default": 0})}}
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (float(value),)


class FloatToInt:
    DESCRIPTION = "Converts a float to an integer by truncating the decimal part."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("FLOAT", {"default": 0.0})}}
    RETURN_TYPES = ("INT",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (int(value),)


class IntToString:
    DESCRIPTION = "Converts an integer to its string representation."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("INT", {"default": 0})}}
    RETURN_TYPES = ("STRING",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (str(value),)


class FloatToString:
    DESCRIPTION = "Converts a float to its string representation."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("FLOAT", {"default": 0.0})}}
    RETURN_TYPES = ("STRING",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (str(value),)


class StringToInt:
    DESCRIPTION = "Parses a string into an integer. Accepts decimal strings like '3.9' (truncated to 3)."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("STRING", {"default": "0"})}}
    RETURN_TYPES = ("INT",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (int(float(value)),)


class StringToFloat:
    DESCRIPTION = "Parses a string into a float."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("STRING", {"default": "0.0"})}}
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (float(value),)


class BoolToInt:
    DESCRIPTION = "Converts a boolean to an integer: True → 1, False → 0."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("BOOLEAN", {"default": False})}}
    RETURN_TYPES = ("INT",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (1 if value else 0,)


class IntToBool:
    DESCRIPTION = "Converts an integer to a boolean: 0 → False, any other value → True."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("INT", {"default": 0})}}
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (value != 0,)


# --- Logic Operators ---

class LogicAND:
    DESCRIPTION = "Returns True only if both inputs are True."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"a": ("BOOLEAN", {"default": False}), "b": ("BOOLEAN", {"default": False})}}
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Logic"

    def op(self, a, b):
        return (a and b,)


class LogicOR:
    DESCRIPTION = "Returns True if at least one input is True."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"a": ("BOOLEAN", {"default": False}), "b": ("BOOLEAN", {"default": False})}}
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Logic"

    def op(self, a, b):
        return (a or b,)


class LogicNOT:
    DESCRIPTION = "Returns the opposite boolean value of the input."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"a": ("BOOLEAN", {"default": False})}}
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Logic"

    def op(self, a):
        return (not a,)


class LogicXOR:
    DESCRIPTION = "Returns True if exactly one of the two inputs is True."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"a": ("BOOLEAN", {"default": False}), "b": ("BOOLEAN", {"default": False})}}
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Logic"

    def op(self, a, b):
        return (a ^ b,)


class LogicNAND:
    DESCRIPTION = "Returns False only if both inputs are True (NOT AND)."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"a": ("BOOLEAN", {"default": False}), "b": ("BOOLEAN", {"default": False})}}
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Logic"

    def op(self, a, b):
        return (not (a and b),)


class LogicNOR:
    DESCRIPTION = "Returns True only if both inputs are False (NOT OR)."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"a": ("BOOLEAN", {"default": False}), "b": ("BOOLEAN", {"default": False})}}
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Logic"

    def op(self, a, b):
        return (not (a or b),)


# --- Comparison ---

class CompareInt:
    DESCRIPTION = "Compares two integers using the selected operator and returns a boolean result."
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("INT", {"default": 0}),
                "b": ("INT", {"default": 0}),
                "op": (["==", "!=", ">", "<", ">=", "<="],),
            }
        }
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "compare"
    CATEGORY = "SimpleLogics/Compare"

    def compare(self, a, b, op):
        result = {"==": a == b, "!=": a != b, ">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[op]
        return (result,)


class CompareFloat:
    DESCRIPTION = "Compares two floats using the selected operator and returns a boolean result."
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("FLOAT", {"default": 0.0}),
                "b": ("FLOAT", {"default": 0.0}),
                "op": (["==", "!=", ">", "<", ">=", "<="],),
            }
        }
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "compare"
    CATEGORY = "SimpleLogics/Compare"

    def compare(self, a, b, op):
        result = {"==": a == b, "!=": a != b, ">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[op]
        return (result,)


# --- Math ---

class MathMaxInt:
    DESCRIPTION = "Returns the larger of two integers."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"a": ("INT", {"default": 0}), "b": ("INT", {"default": 0})}}
    RETURN_TYPES = ("INT",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Math"

    def op(self, a, b):
        return (max(a, b),)


class MathMinInt:
    DESCRIPTION = "Returns the smaller of two integers."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"a": ("INT", {"default": 0}), "b": ("INT", {"default": 0})}}
    RETURN_TYPES = ("INT",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Math"

    def op(self, a, b):
        return (min(a, b),)


class MathMaxFloat:
    DESCRIPTION = "Returns the larger of two floats."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"a": ("FLOAT", {"default": 0.0}), "b": ("FLOAT", {"default": 0.0})}}
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Math"

    def op(self, a, b):
        return (max(a, b),)


class MathMinFloat:
    DESCRIPTION = "Returns the smaller of two floats."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"a": ("FLOAT", {"default": 0.0}), "b": ("FLOAT", {"default": 0.0})}}
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Math"

    def op(self, a, b):
        return (min(a, b),)


class MathClampInt:
    DESCRIPTION = "Clamps an integer between a minimum and maximum value."
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("INT", {"default": 0}),
                "min_val": ("INT", {"default": 0}),
                "max_val": ("INT", {"default": 100}),
            }
        }
    RETURN_TYPES = ("INT",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Math"

    def op(self, value, min_val, max_val):
        return (max(min_val, min(max_val, value)),)


class MathClampFloat:
    DESCRIPTION = "Clamps a float between a minimum and maximum value."
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {"default": 0.0}),
                "min_val": ("FLOAT", {"default": 0.0}),
                "max_val": ("FLOAT", {"default": 1.0}),
            }
        }
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "op"
    CATEGORY = "SimpleLogics/Math"

    def op(self, value, min_val, max_val):
        return (max(min_val, min(max_val, value)),)


# --- Number Conversion ---

class IntToNumber:
    DESCRIPTION = "Converts an integer to a NUMBER (generic numeric type)."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("INT", {"default": 0})}}
    RETURN_TYPES = ("NUMBER",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (float(value),)


class FloatToNumber:
    DESCRIPTION = "Converts a float to a NUMBER (generic numeric type)."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("FLOAT", {"default": 0.0})}}
    RETURN_TYPES = ("NUMBER",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (float(value),)


class NumberToInt:
    DESCRIPTION = "Converts a NUMBER to an integer by truncating the decimal part."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("NUMBER", {"default": 0.0})}}
    RETURN_TYPES = ("INT",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (int(value),)


class NumberToFloat:
    DESCRIPTION = "Converts a NUMBER to a float."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("NUMBER", {"default": 0.0})}}
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (float(value),)


class StringToNumber:
    DESCRIPTION = "Parses a string into a NUMBER."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("STRING", {"default": "0"})}}
    RETURN_TYPES = ("NUMBER",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (float(value),)


class NumberToString:
    DESCRIPTION = "Converts a NUMBER to its string representation."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("NUMBER", {"default": 0.0})}}
    RETURN_TYPES = ("STRING",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (str(value),)


class BoolToNumber:
    DESCRIPTION = "Converts a boolean to a NUMBER: True → 1.0, False → 0.0."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("BOOLEAN", {"default": False})}}
    RETURN_TYPES = ("NUMBER",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (1.0 if value else 0.0,)


class NumberToBool:
    DESCRIPTION = "Converts a NUMBER to a boolean: 0 → False, any other value → True."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"value": ("NUMBER", {"default": 0.0})}}
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "convert"
    CATEGORY = "SimpleLogics/Convert"

    def convert(self, value):
        return (value != 0,)


# --- Switch Nodes ---

class SwitchInt:
    DESCRIPTION = "Returns if_true when condition is True, otherwise returns if_false. Works with integers."
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "condition": ("BOOLEAN", {"default": False}),
                "if_true": ("INT", {"default": 0}),
                "if_false": ("INT", {"default": 0}),
            }
        }
    RETURN_TYPES = ("INT",)
    FUNCTION = "switch"
    CATEGORY = "SimpleLogics/Switch"

    def switch(self, condition, if_true, if_false):
        return (if_true if condition else if_false,)


class SwitchFloat:
    DESCRIPTION = "Returns if_true when condition is True, otherwise returns if_false. Works with floats."
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "condition": ("BOOLEAN", {"default": False}),
                "if_true": ("FLOAT", {"default": 0.0}),
                "if_false": ("FLOAT", {"default": 0.0}),
            }
        }
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "switch"
    CATEGORY = "SimpleLogics/Switch"

    def switch(self, condition, if_true, if_false):
        return (if_true if condition else if_false,)


class SwitchString:
    DESCRIPTION = "Returns if_true when condition is True, otherwise returns if_false. Works with strings."
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "condition": ("BOOLEAN", {"default": False}),
                "if_true": ("STRING", {"default": ""}),
                "if_false": ("STRING", {"default": ""}),
            }
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "switch"
    CATEGORY = "SimpleLogics/Switch"

    def switch(self, condition, if_true, if_false):
        return (if_true if condition else if_false,)


class SwitchAny:
    DESCRIPTION = "Returns if_true when condition is True, otherwise returns if_false. Works with any type."
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "condition": ("BOOLEAN", {"default": False}),
                "if_true": ("*",),
                "if_false": ("*",),
            }
        }
    RETURN_TYPES = ("*",)
    FUNCTION = "switch"
    CATEGORY = "SimpleLogics/Switch"

    def switch(self, condition, if_true, if_false):
        return (if_true if condition else if_false,)


# --- Null Check ---

class IsNotNullText:
    DESCRIPTION = "Returns True if the input string is not null, False otherwise."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"text": ("STRING", {"default": ""})}}
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "check"
    CATEGORY = "SimpleLogics/Logic"

    def check(self, text):
        return (text is not None,)


class IsNotNullImage:
    DESCRIPTION = "Returns True if the input image is not null, False otherwise."
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"image": ("IMAGE",)}}
    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "check"
    CATEGORY = "SimpleLogics/Logic"

    def check(self, image):
        return (image is not None,)


# --- Mappings ---

NODE_CLASS_MAPPINGS = {
    # Convert
    "SL_IntToFloat": IntToFloat,
    "SL_FloatToInt": FloatToInt,
    "SL_IntToString": IntToString,
    "SL_FloatToString": FloatToString,
    "SL_StringToInt": StringToInt,
    "SL_StringToFloat": StringToFloat,
    "SL_BoolToInt": BoolToInt,
    "SL_IntToBool": IntToBool,
    # Number
    "SL_IntToNumber": IntToNumber,
    "SL_FloatToNumber": FloatToNumber,
    "SL_NumberToInt": NumberToInt,
    "SL_NumberToFloat": NumberToFloat,
    "SL_StringToNumber": StringToNumber,
    "SL_NumberToString": NumberToString,
    "SL_BoolToNumber": BoolToNumber,
    "SL_NumberToBool": NumberToBool,
    # Logic
    "SL_AND": LogicAND,
    "SL_OR": LogicOR,
    "SL_NOT": LogicNOT,
    "SL_XOR": LogicXOR,
    "SL_NAND": LogicNAND,
    "SL_NOR": LogicNOR,
    # Compare
    "SL_CompareInt": CompareInt,
    "SL_CompareFloat": CompareFloat,
    # Math
    "SL_MaxInt": MathMaxInt,
    "SL_MinInt": MathMinInt,
    "SL_MaxFloat": MathMaxFloat,
    "SL_MinFloat": MathMinFloat,
    "SL_ClampInt": MathClampInt,
    "SL_ClampFloat": MathClampFloat,
    # Switch
    "SL_SwitchInt": SwitchInt,
    "SL_SwitchFloat": SwitchFloat,
    "SL_SwitchString": SwitchString,
    "SL_SwitchAny": SwitchAny,
    # Null Check
    "SL_IsNotNullText": IsNotNullText,
    "SL_IsNotNullImage": IsNotNullImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # Convert
    "SL_IntToFloat": "Int → Float",
    "SL_FloatToInt": "Float → Int",
    "SL_IntToString": "Int → String",
    "SL_FloatToString": "Float → String",
    "SL_StringToInt": "String → Int",
    "SL_StringToFloat": "String → Float",
    "SL_BoolToInt": "Bool → Int",
    "SL_IntToBool": "Int → Bool",
    # Number
    "SL_IntToNumber": "Int → Number",
    "SL_FloatToNumber": "Float → Number",
    "SL_NumberToInt": "Number → Int",
    "SL_NumberToFloat": "Number → Float",
    "SL_StringToNumber": "String → Number",
    "SL_NumberToString": "Number → String",
    "SL_BoolToNumber": "Bool → Number",
    "SL_NumberToBool": "Number → Bool",
    # Logic
    "SL_AND": "AND",
    "SL_OR": "OR",
    "SL_NOT": "NOT",
    "SL_XOR": "XOR",
    "SL_NAND": "NAND",
    "SL_NOR": "NOR",
    # Compare
    "SL_CompareInt": "Compare Int",
    "SL_CompareFloat": "Compare Float",
    # Math
    "SL_MaxInt": "Max Int",
    "SL_MinInt": "Min Int",
    "SL_MaxFloat": "Max Float",
    "SL_MinFloat": "Min Float",
    "SL_ClampInt": "Clamp Int",
    "SL_ClampFloat": "Clamp Float",
    # Switch
    "SL_SwitchInt": "Switch Int",
    "SL_SwitchFloat": "Switch Float",
    "SL_SwitchString": "Switch String",
    "SL_SwitchAny": "Switch Any",
    # Null Check
    "SL_IsNotNullText": "Is Not Null (Text)",
    "SL_IsNotNullImage": "Is Not Null (Image)",
}
