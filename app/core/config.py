from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env", ".env.local", ".env.development", ".env.production"],
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    # 服务名称
    SERVICE_PROJECT_NAME: str
    # 接口前缀
    SERVICE_API_PREFIX: str
    # 服务端口
    SERVICE_PORT: int

    # postgres数据库地址
    POSTGRES_ADDRESS: str
    # postgres数据库端口
    POSTGRES_PORT: int
    # postgres数据库名称
    POSTGRES_DB: str
    # postgres数据库用户名
    POSTGRES_USER: str
    # postgres数据库密码
    POSTGRES_PASSWORD: str


settings = Settings()
