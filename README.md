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