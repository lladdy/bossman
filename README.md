# BossMan

You are weak and indecisive.

Let the BossMan decide.

# What is BossMan?

BossMan is a simple library made for SC2 AI bot development that will help select from a list of choices for you.

BossMan tracks choice history and prioritizes choices that experience high win rates. It also prioritizes choices it hasn't used much yet.

BossMan is currently used in the SC2 bot [Chance](https://github.com/lladdy/chance-sc2), which plays on
the [SC2 AI Arena Ladder](https://aiarena.net/bots/117/)  
Here it is used for selecting strategies at the start of the match.

# Example Usage:

Simplest usage:

```python
available_builds = ['FourRax', '2BaseTankPush', 'BansheeHarass']

boss_man = BossMan(file='optional/path/to/file.json')  # default file path is ./data/bossman.json

# Here 'strategy' is the decision type.
# Decision types keep different decisions seperate, so they don't interfere with each other.
selected_build = boss_man.decide('strategy', available_builds)

...  # later, after the match is done

boss_man.report_result(True)  # automaticaly saved to file here
```

### Using context

You can add context to each decision, by including each context item as a named argument.  
Each context item will be taken into account for decisions, and tracked in the choice history.  

```python
opponent_id = '12345'
available_builds = ['FourRax', '2BaseTankPush', 'BansheeHarass']

boss_man = BossMan()

# Add the opponent to the decision context.
selected_build = boss_man.decide('strategy', available_builds, opponent=opponent_id)
```

Note that, contextual arguments should be used sparingly (especially if each context has many variations), as they can significantly increase the time it takes for BossMan to learn. I recommend 1-3 context arguments at most. 

# Extra Options

### Control automatic file saving

Usually when you report a result, all data is automatically saved to file.  
To avoid this, you can either pass `autosave` as `False` when you create BossMan, or provide the `save_to_file`
parameter when reporting the result.

```python
boss_man = BossMan(autosave=False)  # Disable autosave permanently

# Alternatively, both these will override the autosave setting
boss_man.report_result(True, save_to_file=False)
boss_man.report_result(True, save_to_file=True)
```
