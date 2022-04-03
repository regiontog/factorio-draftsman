# factorio-draftsman

![A logo generated with 'examples/draftsman_logo.py'](docs/img/logo.png)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A 'draftsman' is a kind of artist that specializes in creating technical drawings across many engineering disciplines, including architectural, mechanical, and electrical.
Similarly, `factorio-draftsman` is a Python module for creating and editing blueprints for the game [Factorio](https://factorio.com/).

```python
import draftsman as factorio

blueprint = factorio.Blueprint()
blueprint.label = "Example"
blueprint.description = "A blueprint for the readme."
blueprint.version = (1, 0) # 1.0

# Create a alt-mode combinator string
test_string = "testing"
for i, c in enumerate(test_string):
    constant_combinator = factorio.ConstantCombinator()
    constant_combinator.tile_position = (i, 0)
    letter_signal = "signal-{}".format(c.upper())
    constant_combinator.set_signal(index = 0, signal = letter_signal, count = 0)
    blueprint.entities.append(constant_combinator)

# Create a simple clock and blinking light
constant = factorio.ConstantCombinator()
constant.tile_position = (-1, 3)
constant.direction = factorio.Direction.EAST
constant.set_signal(0, "signal-red", 1)
constant.id = "constant"
blueprint.entities.append(constant)

# Flexible ways to specify entities
blueprint.entities.append(
    "decider-combinator", id = "clock",
    tile_position = [0, 3],
    direction = factorio.Direction.EAST,
    control_behavior = {
        "decider_conditions": {
            "first_signal": "signal-red",
            "comparator": "<=",
            "constant": 60,
            "output_signal": "signal-red",
            "copy_count_from_input": True
        }
    }
)

# Use IDs to keep track of complex blueprints
blueprint.entities.append("small-lamp", id = "blinker", tile_position = (2, 3))
blinker = blueprint.entities["blinker"]
blinker.set_enabled_condition("signal-red", "=", 60)
blinker.use_colors = True

blueprint.add_circuit_connection("green", "constant", "clock")
blueprint.add_circuit_connection("red", "clock", "clock", 1, 2)
blueprint.add_circuit_connection("green", "clock", "blinker", 2, 1)

# Factorio API filter capabilities
ccs = blueprint.find_entities_filtered(name = "constant-combinator")
assert len(ccs) == len(test_string) + 1

blueprint_book = factorio.BlueprintBook()
blueprint_book.blueprints = [blueprint]

print(blueprint_book)               # Pretty printing using json
print(blueprint_book.to_string())   # Blueprint string to import into Factorio
```
--------------------------------------------------------------------------------

## Overview
Simply put, Draftsman attempts to provide a universal solution to the task of creating and manipulating Factorio blueprint strings, which are compressed text strings used by players to share their constructions easily with others.
Draftsman allows users to programmatically create these strings via script, allowing for designs that would normally be too tedius to design by hand, such as combinator computer compilers, image-to-blueprint converters, pumpjack placers, as well as any other complex or repetitive design better suited for a computer's touch.

For more information on what exactly Draftsman is and does, as well as its intended purpose and philosophy, [you can read the documentation here](https://github.com/redruin1/factorio-draftsman/tree/main/examples).

For more examples on what exactly you can do with draftsman, take a look at the [examples folder](https://github.com/redruin1/factorio-draftsman/tree/main/examples).

### Features
* Compatible with the latest versions of Python 2 and 3
* Compatible with the latest versions of Factorio (1.0+)
* Compatible with Factorio mods(!)
* Well documented
* Intuitive and flexible API
* Useful constructs for ease-of-use:
    * Give entities unique string IDs to make association between entities easier
    * Filter entities from blueprints by type, region and other parameters [just like Factorio's own API](https://lua-api.factorio.com/latest/LuaSurface.html#LuaSurface.find_entities_filtered)
    * Entities are categorized and organized by type within `draftsman.data` for easy and flexible iteration
* Verbose Errors and Warnings ("Factorio-safety" and "Factorio-correctness")
* Expansive and rigorous test suite

--------------------------------------------------------------------------------
## Usage

### Installation:
To install the module from PYPI:
```
pip install factorio-draftsman
```
Then, to perform first time setup run
```
draftsman-update
```
Or, if your Python 'Scripts' folder is not located on your PATH:
```
python -m factorio-draftsman draftsman-update
```
Note that the `draftsman-update` command must be run to ensure the module is ready for use.
Currently I'm looking into solutions to have this command automatically run on install, but for now it must be manually run.
--------------------------------------------------------------------------------
### Testing with [unittest](https://docs.python.org/3/library/unittest.html):
```
python -m unittest discover
```
--------------------------------------------------------------------------------
### Coverage with [coverage](https://coverage.readthedocs.io/en/6.3.2/):
```
coverage run
```

Note that testing currently is only *guaranteed* to work with a vanilla install
(no mods).

--------------------------------------------------------------------------------
### How to use mods:

1. Navigate to the package's installation location
2. Drop the mods you want into the `factorio-mods` folder
3. Run `draftsman-update` to reflect any changes made

`draftsman-update` can also be called in script via the method `draftsman.env:update()` if you want to change the mod list on the fly:
```python
# my_update_script.py
from draftsman.env import update
update() # equivalent to calling 'draftsman-update' from the command line
```

Both `mod-info.json` and `mod-settings.dat` are recognized by the script, so you
can also just change the settings in either of those and the loading process 
will adjust.

## TODO
* Clean and normalize `signatures.py`
* Ensure that all `collision_mask`s are `set`s
* Automatic power-pole connections for Blueprints
* Most of the data extracted from `data.raw` is sorted, but not all of it
* Groups (collect entities and manipulate them all as one object)
* RailPlanner (specify rail paths via pen-drawing or nodes)
* Maybe integrate defaults for more succinct blueprint strings?
* Look into lua bindings via backport to C