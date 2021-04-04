from API.ELO.team import Team


class ELO:

    def __init__(self, volatility: int = 150, gain_ceiling: int = 400):
        """

        Args:
            volatility: The maximum amount of elo a team could win/lose from a match
            gain_ceiling: The amount of elo difference two teams can be before a winning team that doesn't win all
                rounds against a losing team beings to lose small amounts of elo. Effectively the amount difference in
                ELO between two teams allowed before one of the two teams loses elo even when losing in a small amount.
        """

        self.volatility = volatility
        self.gain_ceiling = gain_ceiling

    @staticmethod
    def _calculate_rounds_ratio(team1_rounds: int, team2_rounds: int) -> float:
        """

        Args:
            team1_rounds: How many rounds team 1 won
            team2_rounds: How many rounds team 2 won

        Returns:
            A ratio used in the overall elo calculation
        """
        return team1_rounds / (team1_rounds + team2_rounds)

    @staticmethod
    def _calculate_baseline(team1_rounds: int, team2_rounds: int, multiplication_factor: int = 25) -> float:
        """

        Args:
            team1_rounds: How many rounds team 1 won
            team2_rounds: How many rounds team 2 won
            multiplication_factor: How much to enhance the baseline, changes how much elo is granted from a base value

        Returns:
            The baseline for winners winning and the minimum deficit for losers losing.
        """
        return multiplication_factor * ((team1_rounds - team2_rounds) / (abs(team1_rounds - team2_rounds)))

    def _calculate_expected_score(self, team1_elo: int, team2_elo: int) -> float:
        """
        Effected by the gain ceiling

        Args:
            team1_elo: The amount of elo, in points, that team 1 currently has
            team2_elo: The amount of elo, in points, that team 2 currently has

        Returns:
            The predicted score of the teams
        """
        return 1 / (1 + (10 ** ((team2_elo - team1_elo) / self.gain_ceiling)))

    def calculate(self, team1: Team, team2: Team) -> dict[str, float]:
        """
        Args:
            team1: A team with all elo-related data needed for calculations
            team2: A team with all elo-related data needed for calculations
        Returns:
            A dict with keys "team1" and "team2" which both have a value integer with the calculated elo gain/loss.
        """

        rounds_ratio = self._calculate_rounds_ratio(team1.rounds_won, team2.rounds_won)
        expected_score = self._calculate_expected_score(team1.elo, team2.elo)
        baseline = self._calculate_baseline(team1.rounds_won, team2.rounds_won)

        print(baseline)
        team1_new_elo = team1.elo + (self.volatility * (rounds_ratio - expected_score)) + baseline
        elo_change = abs(team1_new_elo - team1.elo)

        if team1_new_elo > team1.elo:
            team2_new_elo = team2.elo - elo_change
        else:
            team2_new_elo = team2.elo + elo_change

        elo_result_dict = {
            "team1": team1_new_elo,
            "team2": team2_new_elo
        }

        return elo_result_dict


if __name__ == "__main__":
    team1 = Team(elo=1500, rounds_won=3)
    team2 = Team(elo=1400, rounds_won=1)

    print(ELO().calculate(team1, team2))
