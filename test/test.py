import json
import os
from typing import List

from bossman.backend import JsonBackend
from bossman.bossman import BossMan
from bossman.utl import insert_decision_context, read_decision_context


def is_empty_save_file(file: str):
    with open(file) as f:
        file_contents: dict = json.load(f)
    return len(file_contents['decision_stats']) == 0 and len(file_contents['decision_history']) == 0


def test_standard_usage():
    boss_man = BossMan()
    boss_man.decide('build', ['FourRax', "FiveRax"])
    boss_man.report_result(True, save_to_file=False)
    boss_man.decide('build', ['FourRax', "FiveRax"])
    boss_man.report_result(False, save_to_file=False)


def test_context_usage():
    boss_man = BossMan()
    boss_man.decide('build', ['FourRax', "FiveRax"], my_race='Zerg', opponent_id='123')
    boss_man.report_result(True, save_to_file=False)
    boss_man.decide('build', ['FourRax', "FiveRax", "SixRax"], my_race='Zerg', opponent_id='123')
    boss_man.report_result(False, save_to_file=False)


def test_context_sorting():
    pass  # todo: check the context key sorting works


def test_deep_dict_insert():
    dict = {}
    dict = insert_decision_context(dict, {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}, 'value')
    assert dict == {'key1': {'key2': {'key3': 'value'}}}
    assert read_decision_context(dict, {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}) == 'value'


def test_autosave_on():
    file = './data/autosave_on.json'
    if os.path.isfile(file):
        os.remove(file)

    boss_man = BossMan(backend=JsonBackend(file=file), autosave=True)
    boss_man.decide('build', ['FourRax', "FiveRax"])
    boss_man.report_result(True, save_to_file=False)

    assert is_empty_save_file(file)

    boss_man.report_result(True)
    assert not is_empty_save_file(file)


def test_autosave_off():
    file = './data/autosave_off.json'
    if os.path.isfile(file):
        os.remove(file)

    boss_man = BossMan(backend=JsonBackend(file=file), autosave=False)
    boss_man.decide('build', ['FourRax', "FiveRax"])

    boss_man.report_result(True)
    assert is_empty_save_file(file)

    boss_man.report_result(True, save_to_file=True)
    assert not is_empty_save_file(file)


def test_keyword_clash():
    pass  # todo: check choices keyword clash avoidance


def ladder_crash_scenario(filename: str, type: str, options: List[str], result: bool = True,
                          save_to_file: bool = False):
    boss_man = BossMan(backend=JsonBackend(file=filename))
    boss_man.decide(type, options)
    boss_man.report_result(result, save_to_file=save_to_file)


def ladder_crash_scenario_1():
    ladder_crash_scenario("ladder_crash_scenario_1.json",
                          "build",
                          ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"])


def omit_missing_historial_options():
    ladder_crash_scenario("omit_missing_historial_options.json",
                          "build",
                          ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"])


def analytics():
    boss_man = BossMan(backend=JsonBackend(file='analytics.json'), autosave=False)
    boss_man.print_analytics()


test_standard_usage()
test_autosave_on()
test_autosave_off()
test_keyword_clash()
ladder_crash_scenario_1()
omit_missing_historial_options()
analytics()


def convert_cache(file_name):
    with open(file_name) as f:
        save_file_cache: dict = json.load(f)
    new_file_cache: dict = {'decision_stats': {}, 'decision_history': [], }
    for key, val in save_file_cache['global_decision_history'].items():
        strings = key.split('_')
        type = strings[0]
        context = {'opponent_id': strings[1], 'my_race': strings[2], }
        if type not in new_file_cache['decision_stats']:
            new_file_cache['decision_stats'][type] = {}
        insert_decision_context(new_file_cache['decision_stats'][type], context, val)
    with open('e_' + file_name, 'w') as f:
        json.dump(new_file_cache, f)

# convert_cache('analytics.json')
