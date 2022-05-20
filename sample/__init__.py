from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'sample'
    PLAYERS_PER_GROUP = None
    TASKS = ['preference', 'preference1']
    NUM_ROUNDS = 1
    show_up = 8
    multiplier = 0.2

    lottery_1_payoff_1 = cu(28)
    lottery_2_payoff_1 = cu(36)
    lottery_1_payoff_2 = cu(25)
    lottery_2_payoff_2 = cu(24)



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    preference = models.StringField(
        choices=[
            [1, "Lottery 1: You have 50% chance to win £28 and £25 otherwise"],
            [2, "Lottery 2: You have 60% chance to win £26 and £36 otherwise"]],
        doc='Players decision', widget=widgets.RadioSelect
    )
    preference1 = models.StringField(
        choices=[[1, 'You have 80% chance to win 2, 10% chance to win 20 and 0 otherwise'],
                 [2, 'You have 100% chance to win 2.8.']
                 ],
        doc='Players decision', widget=widgets.RadioSelect,
    )
    choice_in_round = models.StringField(initial=0)
    choice = models.StringField(initial=0)


# FUNCTIONS

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            round_number = list(range(1, C.NUM_ROUNDS))
            task_rounds = dict(zip(C.TASKS, round_number))
            p.participant.task_rounds = task_rounds


# def set_payoffs(player: Player):
#     if player.in_rounds(1, C.NUM_ROUNDS):
#         if player.preference == 1:
#             payoff = C.lottery_1_payoff_1
#         else:
#             payoff = C.lottery_1_payoff_2
#     else:
#         if player.preference == 2:
#             payoff = C.lottery_2_payoff_1
#         else:
#             payoff = C.lottery_2_payoff_2
#     player.payoff = payoff


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['preference']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(player_in_rounds = player.in_rounds(1,C.NUM_ROUNDS))


class PreferencePage(Page):
    form_model = 'player'
    form_fields = ['preference1']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(player_in_rounds=player.in_rounds(1, C.NUM_ROUNDS))

    def before_next_page(player: Player, timeout_happened):
        if player.in_rounds(1,C.NUM_ROUNDS):
            if player.choice == 1:
                payoff = C.lottery_1_payoff_1
            else:
                payoff = C.lottery_1_payoff_2
        else:
            if player.choice == 2:
                payoff = C.lottery_2_payoff_1
            else:
                payoff = C.lottery_2_payoff_2
        player.payoff = payoff


class Results(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
#
#     @staticmethod
#     def vars_for_template(player: Player):
#         if player.round_number == C.NUM_ROUNDS:
#             return player.payoff


page_sequence = [MyPage, PreferencePage, Results ]
