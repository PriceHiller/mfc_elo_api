# How to use the API During Dry Run

## Authorization

### Credentials

A user will be created for you, details:

```
- Username: `marklar`
- Password: `lTL_vMnLV5iA_jEq`
```

### Logging in

- Post the endpoint at `/user/login/` with the required json below
  ```json
  {
    "username": "marklar",
    "password": "lTL_vMnLV5iA_jEq"
  }
  ```
- This will return something similar to the following json:
  ```json
  {
    "generated": "2021-04-06T11:41:03.340961+00:00",
    "message": null,
    "extra": null,
    "id": "11a0fb41-e6a6-4c36-bca9-beacb92af240",
    "creation": "2021-04-06T10:41:52.357639+00:00",
    "modification": null,
    "username": "John Smith",
    "token": {
      "generated": "2021-04-06T11:41:03.340915+00:00",
      "message": null,
      "extra": null,
      "id": "3cd58960-8132-4b66-b1a5-dfcd2c1ef08f",
      "creation": "2021-04-06T10:41:52.374658+00:00",
      "modification": null,
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTFhMGZiNDEtZTZhNi00YzM2LWJjYTktYmVhY2I5MmFmMjQwIiwiZXhwaXJlcyI6IjIwMjEtMTAtMDMgMTA6NDE6NTIuMzc0MTcyKzAwOjAwIn0.GwqAiqPm7Er0Y8fWSkyjAXJ4GviovoRP2mTXyWQC5f0"
    },
    "email": "jsmith@email.com",
    "is_active": true
  }
  ```
    - Access the `["token"]["token"]` key to get the authorization header. The API will also issue you a cookie, so if
      you'd like to use a cookie jar of some form and include it in all requests that will work too; otherwise, just
      include the token in your header as an `authorization` header.

## Handling a Match

Writing this down sequentially - as though a match was just started.

1. Firstly, the `.startmatch` command will likely need to be modified to accept team names.
2. Teams will be pre-created for you for all matches the night of the dry run.
    - The `.startmatch` command should take in two team names and send them to lowercase.
        - Ideally this `.startmatch` command will take the first team name in as the blue team and the second team in as
          the red team to properly align with team numbers in the RCON returns.
        - Once done, do a search for both teams by name
        - Endpoint: `/team/name`
        - Type: `GET`
        - Authentication: `no`
        - Example URL:
          ```
          https://ip:port/team/name?team_name=TEAM_NAME_HERE
          ```
        - Return data:
          ```json
          {
              "generated": "2021-04-06T12:22:32.402991+00:00",
              "message": null,
              "extra": null,
              "id": "7c82fbab-3a2f-4442-abf6-e11f7d096e2c",
              "creation": "2021-04-06T12:11:47.087113+00:00",
              "modification": null,
              "team_name": "Team1",
              "elo": 1500,
              "discord_id": null,
              "players": []
          } 
          ```
            - You will need the `id` key for each team as this will be used when creating matches.
3. Creating a match
    - This should be done after the `.startmatch` command has been issued
    - The match will require both team ids that you should have fetched from the API.
    - Endpoint `/match/create`
    - Type: `POST`
    - Authentication: `yes`
    - Example JSON:
        ```json
        {
          "team1_id": "7c82fbab-3a2f-4442-abf6-e11f7d096e2c",
          "team2_id": "6b6875c8-0dc1-4b21-9ac4-3f580cddb468"
        }
        ```
    - Return JSON:
        ```json
        {
          "generated": "2021-04-06T12:27:15.142362+00:00",
          "message": "Created match with id: 559811dc-3c4a-4c0c-91af-4b321e5eb5ce",
          "extra": [
            {
              "match id": "559811dc-3c4a-4c0c-91af-4b321e5eb5ce"
            }
          ]
        }
        ```
        - You will want to fetch the `match_id` key and store the id as it is required to create sets beneath the match
4. Creating a set
    - This should be done after creating a match as it requires a match id
    - Endpoint: `/set/create`
    - Type: `POST`
    - Authentication: 'yes'
    - Example JSON:
        ```json
        {
          "map": "skm_moshpit",
          "match_id": "559811dc-3c4a-4c0c-91af-4b321e5eb5ce"
        }
        ```
        - Note that to use this endpoint you will need the match id you received from creating the match
    - Return JSON:
        ```json
        {
          "generated": "2021-04-06T12:49:01.626800+00:00",
          "message": "Created a set 203315df-c659-4bd3-b9bd-9f021c8b6eb4 under match 559811dc-3c4a-4c0c-91af-4b321e5eb5ce",
          "extra": [
            {
              "set id": "203315df-c659-4bd3-b9bd-9f021c8b6eb4"
            }
          ]
        }
        ``` 
        - You will want to fetch the `set_id` key and store the id as it is required to create rounds beneath the set
5. Creating a round
    - This should be done after creating a set as it requires a set id
    - Endpoints `/round/create`
    - Type: `POST`
    - Authentication: `yes`
    - Example JSON:
        ```json
        {
          "set_id": "203315df-c659-4bd3-b9bd-9f021c8b6eb4",
          "team1_win": true,
          "team2_win": false
        }
        ```

        - Note that to use this endpoint you will need the set id you received from creating the set
    - Return JSON:
        ```json
        {
          "generated": "2021-04-06T12:52:06.023414+00:00",
          "message": "Created round with id d097f02d-4b2e-4e9d-a506-36481246f0f0",
          "extra": [
            {
              "round_id": "d097f02d-4b2e-4e9d-a506-36481246f0f0"
            }
          ]
        }
        ```
        - You will want to fetch the `round_id` key and store the id as it is required to add players to each round
6. Creating Players
    - Seeing as we can get the playfab-id and the playername it makes more sense to create the player the night of the
      game.
    - Endpoint: `/player/create`
    - Type: `POST`
    - Authentication: `yes`
    - Example JSON:
        ```json
        {
          "player_name": "Example Player Name",
          "playfab_id": "abcd12345"
        }
        ```
        - Where the `playfab_id` defines whatever PlayFab id they have according to RCON.
    - Return JSON:
        ```json
        {
           "generated": "2021-04-06T12:58:37.722539+00:00",
           "message": "Created player",
           "extra": [
             {
               "player_id": "a3daa6e7-ad86-4073-91d8-cde2b79f0191"
             }
           ]
         }
        ```
        - You will want to fetch the `player_id` key as it will be needed to add them to a round
    - A note: do not worry about adding players to a team, that will be done at a later date via a discord bot.
7. Adding Players to a Round
    - Ensure you have created the player first (above)
    - Endpoint: `/round/create-round-players`
    - Type: `POST`
    - Authentication: `yes`
    - Example JSON:
       ```json
       {
         "round_players": [
           {
             "round_id": "d097f02d-4b2e-4e9d-a506-36481246f0f0",
             "player_id": "a3daa6e7-ad86-4073-91d8-cde2b79f0191",
             "team_id": "7c82fbab-3a2f-4442-abf6-e11f7d096e2c",
             "team_number": 0,
             "score": 0,
             "kills": 0,
             "deaths": 0,
             "assists": 0
           }
         ]
       }
       ```
        - Take note, you can add ***multiple*** players within this single post. Each round player is a single json
          object defining round_id, etc. see the example json.
    - Return JSON:
        - If you need to worry about this something has likely gone wrong or I missed something, please let me know
          ASAP.

8. Concluding
   - For each new set you will go through steps 4 through 7 (you can skip 6 if a player has already been created)
     until the game is over at such a point take the match id and hit the following endpoint
   - Endpoint `/match/calculate-match-elo`
   - Type: `POST`
   - Example:
      ```
      https://0.0.0.0:5000/match/calculate-match-elo?match_id=559811dc-3c4a-4c0c-91af-4b321e5eb5ce
      ```
   - Return JSON:
      - Don't worry about it
   - This will calculate the resulting ELO and update accordingly.
      

