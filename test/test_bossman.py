from bossman.algorithm.ucb1 import UCB1
from bossman.bossman import BossMan
import unittest


class TestBossman(unittest.TestCase):
    def test_decide_explore_after_win(self):
        boss_man = BossMan(random_distribution=False, success_probability_algorithm=UCB1())
        build1, _ = boss_man.decide("build", ["FourRax", "FiveRax"])
        boss_man.report_result(True, save_to_file=False)
        build2, _ = boss_man.decide("build", ["FourRax", "FiveRax"])
        self.assertNotEqual(build1, build2)

    def test_decide_explore_after_loss(self):
        boss_man = BossMan(random_distribution=False, success_probability_algorithm=UCB1())
        build1, _ = boss_man.decide("build", ["FourRax", "FiveRax"])
        boss_man.report_result(False, save_to_file=False)
        build2, _ = boss_man.decide("build", ["FourRax", "FiveRax"])
        self.assertNotEqual(build1, build2)

    def test_decide_consider_winrate(self):
        boss_man = BossMan(random_distribution=False, success_probability_algorithm=UCB1())
        build1, _ = boss_man.decide("build", ["FourRax", "FiveRax"])
        boss_man.report_result(True, save_to_file=False)
        boss_man.decide("build", ["FourRax", "FiveRax"])
        boss_man.report_result(False, save_to_file=False)
        build3, _ = boss_man.decide("build", ["FourRax", "FiveRax"])
        self.assertEqual(build1, build3)


if __name__ == "__main__":
    unittest.main()
