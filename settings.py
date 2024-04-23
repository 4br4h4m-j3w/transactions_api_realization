from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    base_url: str
    app_id: str
    api_secret: str
    crypt_key: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")