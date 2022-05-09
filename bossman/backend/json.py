import json
import os

from bossman.backend import Backend
from bossman.utl import save_json_to_file


class JsonBackend(Backend):

    def __init__(self, file="./data/bossman.json",
                 create_file_on_missing=True,
                 ):
        self.file = file

        self.save_file_cache: dict = {
            "decision_stats": {},
            "decision_history": [],
        }

        if create_file_on_missing and not os.path.isfile(file):
            save_json_to_file(file, self.save_file_cache)

        with open(file) as f:
            self.save_file_cache: dict = json.load(f)
            # TODO: sanity check wins aren't more than times chosen

    def load_decision_stats(self) -> dict:
        return self.save_file_cache["decision_stats"]

    def save(self, decision_stats, match_decision_history):
        """
        Saves the current state to file.
        """

        self.save_file_cache["decision_stats"] = decision_stats
        self.save_file_cache["decision_history"].append(match_decision_history)

        save_json_to_file(self.file, self.save_file_cache)
