import json
import os

import numpy as np
from scipy.special import expit

from utl import fix_p, floor, insert_decision_context, populate_missing_decision_context_keys, read_decision_context


class BossMan:
    def __init__(self, file='./data/bossman.json', create_file_on_missing=True, rounding_precision: int = 4,
                 autosave=True):
        self.save_file_cache: dict = {'decision_stats': {}, 'decision_history': [], }
        self.decision_stats: dict = {}
        self.match_decision_history: dict = {"decisions": []}
        self.file = file
        self.rounding_precision = rounding_precision
        self.autosave = autosave

        if create_file_on_missing and not os.path.isfile(file):
            with open(file, 'w') as f:
                json.dump(self.save_file_cache, f)

        with open(file) as f:
            self.save_file_cache: dict = json.load(f)
            # TODO: sanity check wins aren't more than times chosen
        self.decision_stats = self.save_file_cache['decision_stats']

    def decide(self, options, decision_type: str, **context) -> (str, float):
        """
        Makes a decision between choices, taking into account match history.

        TODO: allow for decision scopes where the caller can register things like their opponent/race/etc in the decision
        TODO: have decisions with a similar (but not the same) set of scopes influence other decisions.
        """
        if 'choices' in context:  # we reserve this keyword
            raise "You cannot use 'choices' as part of your context - it is a reserved keyword."

        context = dict(sorted(context.items()))  # keep a consistent key order

        # Retrieve percentage win for each option from
        chosen_count: list = []
        won_count: list = []

        if decision_type in self.decision_stats:
            populate_missing_decision_context_keys(self.decision_stats[decision_type], context)
            tmp_decision_context = read_decision_context(self.decision_stats[decision_type], context)

            if 'choices' not in tmp_decision_context:
                tmp_decision_context['choices'] = {}

            decision_context = tmp_decision_context['choices']

            # Intialize missing values
            for option in options:
                if option not in decision_context:
                    decision_context[option] = {'chosen_count': 0, 'won_count': 0}

            # Prepare data for call to probabilities calc
            for key, decision in decision_context.items():
                # # omit missing historical options
                if key in options:
                    won_count.append(decision['won_count'])
                    chosen_count.append(decision['chosen_count'])

        else:
            # Intialize missing values
            self.decision_stats[decision_type] = {}

            option_stats = {}
            for option in options:
                option_stats[option] = {'chosen_count': 0, 'won_count': 0}
                won_count.append(0)
                chosen_count.append(0)

            insert_decision_context(self.decision_stats[decision_type],
                                    context,
                                    option_stats)

        p = self._calc_choice_probabilities(np.array(chosen_count), np.array(won_count))
        choice = np.random.choice(options, p=fix_p(p))

        decision_context = read_decision_context(self.decision_stats[decision_type], context)
        decision_context['choices'][choice]['chosen_count'] += 1
        self._record_match_decision(decision_type, context, options, choice)
        return choice, p[options.index(choice)]

    def _record_match_decision(self, decision_type, context, options, choice):
        self.match_decision_history['decisions'].append({
            "type": decision_type,
            "context": context,
            "options": options,
            "choice": choice
        })

    def report_result(self, win: bool, save_to_file: bool = None, purge_match_decision_history: bool = True):
        """
        Registers the outcome of the current match.
        """
        if win:
            self.match_decision_history['outcome'] = 1

            for decision in self.match_decision_history['decisions']:
                decision_context = read_decision_context(self.decision_stats[decision['type']], decision['context'])
                decision_context['choices'][decision['choice']]['won_count'] += 1

        if save_to_file is not None:  # override autosave behaviour
            if save_to_file:
                self._save_state_to_file(purge_match_decision_history=purge_match_decision_history)
            # else don't save (do nothing)
        elif self.autosave:
            self._save_state_to_file(purge_match_decision_history=purge_match_decision_history)

    def _save_state_to_file(self, file_override: str = None, purge_match_decision_history: bool = True):
        """
        Saves the current state to file.
        """

        file_to_use = self.file
        if file_override is not None:
            file_to_use = file_override

        self.save_file_cache['decision_stats'] = self.decision_stats
        self.save_file_cache['decision_history'].append(self.match_decision_history)
        with open(file_to_use, 'w') as f:
            json.dump(self.save_file_cache, f)

        if purge_match_decision_history:
            self.match_decision_history = {"decisions": []}

    def _calc_choice_probabilities(self, chosen_count: np.array, won_count: np.array) -> np.array:
        """
        Determines the weighted probabilities for each choice.
        """
        win_perc = self._calc_win_perc(chosen_count, won_count)

        """
        mod: The higher this value, the quicker the weight fall off as chosen_count climbs
        """
        mod = 1.0
        # calculate a weight that will make low sample size choices more likely
        probability_weight = 1 - (expit(chosen_count * mod) - 0.5) * 2

        # Apply that weight to each choice's win percentage
        weighted_probabilities = win_perc + probability_weight

        # Scale probabilities back down so they sum to 1.0 again.
        prob_sum = np.sum(weighted_probabilities)
        scaled_probs = weighted_probabilities / prob_sum

        # Avoid rounding errors by taking the rounding error difference
        # scaled_probs = scaled_probs / scaled_probs.sum(axis=0, keepdims=1)
        scaled_probs = self._round_probabilities_sum(scaled_probs)

        # Sanity check in case of bug
        # prob_check_sum = np.sum(scaled_probs)
        # assert prob_check_sum == 1.0, f'Is there a bug? prob_check_sum was {prob_check_sum}'

        # print(f'Samples: {samples}')
        # print(f'Wins: {wins}')
        # print(f'Win %: {win_perc}')
        # print(f'probability_weight: {probability_weight}')
        # print(f'Prob Inv: {probability_weight}')
        # print(f'Actual Prob: {weighted_probabilities}')
        # print(f'Prob Sum: {prob_sum}')
        # print(f'chosen_count: {chosen_count}')
        # print(f'won_count Prob: {won_count}')
        # print(f'Scaled Prob: {scaled_probs}')
        # print(f'Prob Check Sum: {prob_check_sum}')

        return scaled_probs

    def _calc_win_perc(self, chosen_count, won_count):
        return np.divide(won_count, chosen_count, out=np.zeros_like(won_count, dtype=float), where=won_count != 0)

    def _round_probabilities_sum(self, probabilities: np.array) -> np.array:
        probabilities = floor(probabilities, self.rounding_precision)
        round_amount = 1.0 - np.sum(probabilities)
        probabilities[0] += round_amount  # chuck it on the first one
        return probabilities

    def calc_analytics(self) -> dict:
        analytics = {}
        for scope_name, choices in self.decision_stats.items():
            analytics[scope_name] = {}
            analytics[scope_name]['times_considered'] = 0
            analytics[scope_name]['choices'] = {}
            for choice_name, choice in choices.items():
                analytics[scope_name]['times_considered'] += choice['chosen_count']

                analytics[scope_name]['choices'][choice_name] = {}
                analytics[scope_name]['choices'][choice_name]['win_perc'] = np.asscalar(
                    self._calc_win_perc(choice['chosen_count'],
                                        choice['won_count']))
                analytics[scope_name]['choices'][choice_name]['chosen_count'] = choice['chosen_count']
                analytics[scope_name]['choices'][choice_name]['won_count'] = choice['won_count']

        # sort
        analytics = dict(reversed(sorted(analytics.items(), key=lambda item: item[1]['times_considered'])))
        for scope_name, values in analytics.items():
            values['choices'] = dict(reversed(
                sorted(values['choices'].items(), key=lambda item: (item[1]['win_perc'], -item[1]['chosen_count']))))

        return analytics

    def print_analytics(self):
        analytics = self.calc_analytics()
        for scope_name, values in analytics.items():
            print(f'{scope_name} - {values["times_considered"]} times considered')

            for choice in values['choices']:
                print(f"{choice:<30} "
                      f"Win %: {values['choices'][choice]['win_perc']:.2f} "
                      f"Chosen: {values['choices'][choice]['chosen_count']:>3} "
                      f"Won: {values['choices'][choice]['won_count']:>3}")
