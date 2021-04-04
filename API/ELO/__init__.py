from API.ELO.team import Team


class ELO:

    def __init__(self, volatility: int = 150, gain_ceiling: int = 400):
        """

        Args:
            volatility: The maximum amount of elo a team could win/lose from a match
            gain_ceiling: The amount of elo difference two teams can be before a winning team that doesn't win all
                rounds against a losing team beings to lose small amounts of elo.
        """

        self.volatility = volatility
        self.gain_ceiling = gain_ceiling

    def calculate(self, team1: Team, team2: Team, ) -> dict:
        """
        Args:
            team1: A team with all elo-related data needed for calculations
            team2: A team with all elo-related data needed for calculations
        Returns:
            A dict with keys "team1" and "team2" which both have a value integer with the calculated elo gain/loss.
        """

    @staticmethod
    def _calculate_rounds_ratio(team1_rounds: int, team2_rounds: int):
        """

        Args:
            team1_rounds: How many rounds team 1 won
            team2_rounds: How many rounds team 2 won

        Returns:
            A ratio used in the overall elo calculation
        """
        return team1_rounds / (team1_rounds + team2_rounds)

    @staticmethod
    def _calculate_baseline(team1_rounds: int, team2_rounds: int, multiplication_factor: int = 25):
        """

        Args:
            team1_rounds: How many rounds team 1 won
            team2_rounds: How many rounds team 2 won
            multiplication_factor: How much to enhance the baseline, changes how much elo is granted from a base value

        Returns:
            The baseline for winners winning and the minimum deficit for losers losing.
        """
        return multiplication_factor * ((team1_rounds - team2_rounds) / (abs(team1_rounds / team2_rounds)))
