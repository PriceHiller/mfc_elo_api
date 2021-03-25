On your postgres DB esnure you are at version 13+.

Then install the ossp extension via the console:
```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

# Postgresql Configuration
Version = 13+

## OSSP Extension Installation
Connect and execute to your database:

```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

We use this extension for UUID generation purposes

## Config File
Change your timezone in `postgresql.conf` to `UTC`.

### Locations
`postgresql.conf` on M1 Mac is located at `/Users/user/Library/Application Support/Postgres/var-13`

#Environment Variables

- jwt_secret
    - Ideally at least 32 characters long
    - Example
        - `d18edfac5b16c1839a203aadc57df7c3303b9c76707398996da65dcb2797889f1ec4a2de`
- jwt_algorithm
    - The algorithm that will be used
    - Example
        - `HS256`
    - Recommended
        - `HS256`
- sql_db_url
    - The connection link to a database
    - Supports *only* postgresql
    - Example
        - `postgresql://username@0.0.0.0:5432/Database`