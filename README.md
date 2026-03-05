# ComfyUI-SimpleLogics

A lightweight ComfyUI node library providing logic operators, type conversions, math utilities, and switch nodes.

No extra dependencies

## Installation

Clone into your `ComfyUI/custom_nodes/` folder:

```bash
git clone https://github.com/danipisca07/ComfyUI-SimpleLogics
```

## Nodes

### Convert (`SimpleLogics/Convert`)
| Node | Description |
|------|-------------|
| Int → Float | Cast integer to float |
| Float → Int | Truncate float to integer |
| Int / Float → String | Numeric to text |
| String → Int / Float | Parse text to number |
| Bool → Int | `True` → `1`, `False` → `0` |
| Int → Bool | `0` → `False`, anything else → `True` |

### Logic (`SimpleLogics/Logic`)
AND, OR, NOT, XOR, NAND, NOR — all take `BOOLEAN` inputs and return `BOOLEAN`.

### Compare (`SimpleLogics/Compare`)
**Compare Int / Compare Float** — pick an operator (`==` `!=` `>` `<` `>=` `<=`), returns `BOOLEAN`.

### Math (`SimpleLogics/Math`)
| Node | Description |
|------|-------------|
| Max / Min Int | Larger / smaller of two integers |
| Max / Min Float | Larger / smaller of two floats |
| Clamp Int / Float | Constrain a value between `min` and `max` |

### Switch (`SimpleLogics/Switch`)
All switch nodes take a `condition` (BOOLEAN) and return `if_true` or `if_false`.

| Node | Input types |
|------|-------------|
| Switch Int | INT |
| Switch Float | FLOAT |
| Switch String | STRING |
| Switch Any | Any type |

## Running Tests

```bash
pip install pytest
pytest tests/
```

## Contributions?

Welcome