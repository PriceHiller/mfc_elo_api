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

## Logging

For logging to work you *must* define a `log_config.yaml` file within the `bot` directory based on the the python
logging [dictConfig](https://docs.python.org/3/library/logging.config.html#dictionary-schema-details) *or* set the 
appropriate log path in your environment, see **Environment Variables**. 

Within your own `log_config.yaml`, assuming you don't use the default, ensure you set `disable_existing_loggers` to
**false**, otherwise the log messages emitted by [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
will not be logged.

An example config in yaml, and the one that ships by default:

```yaml
version: 1
disable_existing_loggers: false # Important, otherwise the discord.py logs will not be logged. Keep this as false
formatters:
    standard:
        format: '[%(asctime)s][%(threadName)s][%(name)s.%(funcName)s:%(lineno)d][%(levelname)s] %(message)s'
handlers:
    default_stream_handler:
        class: logging.StreamHandler
        formatter: standard
        level: INFO
        stream: ext://sys.stdout
    default_file_handler:
        backupCount: 5
        class: logging.handlers.RotatingFileHandler
        filename: Bot.log
        formatter: standard
        level: DEBUG
    error_file_handler:
        backupCount: 5
        class: logging.handlers.RotatingFileHandler
        delay: true
        filename: bot_error.log
        formatter: standard
        level: ERROR
loggers:
    '': # The root logger, best to leave it undefined (don't enter a string)
        handlers:
            - default_stream_handler
            - default_file_handler
            - error_file_handler
        level: DEBUG
        propagate: false
```


# Environment Variables


All environment variables are entered in uppercase.
## Logging Variables

All logging variables are preceded by log_

| Key             | Example Value | Description
| :---            | :---          | :---
| LOG_CONFIG_PATH | /Users/user/MFC_Bot/bot/log_config.yaml | The path (including the name of the file) of your log config.

## JWT Variables

All jwt variables are preceded by `JWT_`

| Key           | Example Value                                                            | Description
| :---          | :---                                                                     | :---
| JWT_SECRET    | d18edfac5b16c1839a203aadc57df7c3303b9c76707398996da65dcb2797889f1ec4a2de | The JWT secret used to generate JWT tokens, ideally at least 32 characters long.
| JWT_ALGORITHM | HS256                                                                    | The algorithm that is used when generating JWT tokens

## SQL Variables

All sql variables are preceded by `sql_`

| Key        | Example Value                                 | Description
| :---       | :---                                          | :---
| SQL_DB_URL | `postgresql://username@0.0.0.0:5432/Database` | The database connection url, *only* supports postgresql due to the need for postgresql UUID functions


## Uvicorn Variables

See [uvicorn settings](https://www.uvicorn.org/settings/) as I sure shit ain't writin' all that bs out.

Effectively, take the name of each setting, append `UVICORN_` to the start of it in your environment and that's
how you pass arguments to uvicorn in this application.

For example, if you wanted to set the host that uvicorn runs on the host var would be `UVICORN_HOST`.