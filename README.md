# BossMan

You are weak and indecisive.  

Let the BossMan decide. 

# What is BossMan?

BossMan is a simple library made for SC2 AI bot development that will help select from a list of choices for you. 

BossMan prioritizes choices that experience high win rates as well as prioritizing choices with low sample sizes.

BossMan is currently used in the SC2 bot [Chance](https://github.com/lladdy/chance-sc2), which plays on the [SC2 AI Arena Ladder](https://aiarena.net/bots/117/)  
Here it is used for selecting strategies at the start of the match.


# Example Usage:
```python

available_builds = ['FourRax', '2BaseTankPush', 'BansheeHarass']
boss_man = BossMan(file='optional/path/to/file.json')  # default file path is ./data/bossman.json
selected_build = boss_man.decide(f'build', available_builds)
... # later, after the match is done
boss_man.register_result(True) # automaticaly saved to file here



```


# Extra Options

### Don't automatically save file
Usually when you register a result, all data is automatically saved to file.  
To avoid this, you can provide the `save_to_file` parameter like so:
```
boss_man.register_result(True, save_to_file=False)
```
