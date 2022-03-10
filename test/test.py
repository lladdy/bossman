import os
from typing import List

from bossman import BossMan

EMPTY_JSON_FILE_SIZE = 2  # 2 for the JSON brackets


def is_empty_json_file(file: str):
    return os.path.getsize(file) == EMPTY_JSON_FILE_SIZE


def test_standard_usage():
    boss_man = BossMan()
    boss_man.decide(['FourRax', "FiveRax"], scope='build')
    boss_man.report_result(True, save_to_file=False)


def test_autosave_on():
    file = './data/autosave_on.json'
    if os.path.isfile(file):
        os.remove(file)

    boss_man = BossMan(file=file, autosave=True)
    boss_man.decide(['FourRax', "FiveRax"], scope='build')
    boss_man.report_result(True, save_to_file=False)

    assert is_empty_json_file(file)

    boss_man.report_result(True)
    assert not is_empty_json_file(file)


def test_autosave_off():
    file = './data/autosave_off.json'
    if os.path.isfile(file):
        os.remove(file)

    boss_man = BossMan(file=file, autosave=False)
    boss_man.decide(['FourRax', "FiveRax"], scope='build')

    boss_man.report_result(True)
    assert is_empty_json_file(file)

    boss_man.report_result(True, save_to_file=True)
    assert not is_empty_json_file(file)


def ladder_crash_scenario(filename: str, scopes: str, options: List[str], result: bool = True,
                          save_to_file: bool = False):
    boss_man = BossMan(file=filename)
    boss_man.decide(options, scope=scopes)
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
    boss_man = BossMan(file='analytics.json', autosave=False)
    boss_man.print_analytics()


test_standard_usage()
test_autosave_on()
test_autosave_off()
ladder_crash_scenario_1()
omit_missing_historial_options()
analytics()
