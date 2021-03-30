import textwrap


class BaseProcedure:

    @classmethod
    def get_procedures(cls):
        procedures = []

        for subcls in cls.__subclasses__():
            print(subcls)
            print(vars(subcls))
            procedures.append(subcls.procedure)

        return procedures


class UpdateMatchScores(BaseProcedure):
    procedure = textwrap.dedent("""
        -- Update both team1 and team2 with new scores calculated from the sets against a divisior
        
        CREATE or REPLACE PROCEDURE update_match_scores(
            _match_id uuid,
            _set_id uuid,
            divisor int
        )
        
        
        
        LANGUAGE plpgsql AS $$
            DECLARE
                team1_rounds int := 0;
                team2_rounds int := 0;
        
            BEGIN
                SELECT SUM(team1_win::int) INTO team1_rounds FROM mfc_rounds WHERE set_id = _set_id;
                SELECT SUM(team2_win::int) INTO team2_rounds FROM mfc_rounds WHERE set_id = _set_id;
        
                -- Update mfc_matches sets won based on the rounds divided by some number, should result in a whole number (int)
        
                UPDATE
                    mfc_matches
                SET
                    team1_sets_won = (team1_rounds / divisor),
                    team2_sets_won = (team2_rounds / divisor)
                WHERE
                      id = _match_id;
        
                COMMIT;
            END;
        $$;
        """)


procedures = BaseProcedure().get_procedures()
