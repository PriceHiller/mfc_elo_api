import uvicorn
import fastapi


class UvicornConfiguration(uvicorn.config.Config):

    def __init__(self,
                 app: fastapi.FastAPI,
                 host: str = "0.0.0.0",
                 port: int = 5000,
                 log_config: dict = None,
                 reload: bool = True,
                 *args,
                 **kwargs):
        super().__init__(app, host=host, port=port, log_config=log_config, reload=reload, *args, **kwargs)
