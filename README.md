# Configuration
It is *highly* recommended that a `.env` file is created within the `API` directory, otherwise all of your environment
variables will need to be exported by default into your environment

## Postgresql Configuration

### Database URL
To set the database URL set in your `.env` or environment: `sql_db_url=YOUR URL HERE`, see **Environment Variables**

### OSSP Extension Installation
Connect and execute to your database:

```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

We use this extension for UUID generation purposes

### Config File
Change your timezone in `postgresql.conf` to `UTC`.

#### Locations
`postgresql.conf` on M1 Mac is located at `/Users/user/Library/Application Support/Postgres/var-13`

#Environment Variables

## JWT Variables

All jwt variables are preceded by `jwt_`

| Key           | Example Value                                                            | Description
| :---          | :---                                                                     | :---
| jwt_secret    | d18edfac5b16c1839a203aadc57df7c3303b9c76707398996da65dcb2797889f1ec4a2de | The JWT secret used to generate JWT tokens, ideally at least 32 characters long.
| jwt_algorithm | HS256                                                                    | The algorithm that is used when generating JWT tokens

## SQL Variables

All sql variables are preceded by `sql_`

| Key  | Example Value | Description
| :--- | :---          | :---
| sql_db_url | `postgresql://username@0.0.0.0:5432/Database` | The database connection url, *only* supports postgresql due to the need for postgresql UUID functions
