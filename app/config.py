from pydantic_settings import BaseSettings, SettingsConfigDict

# 使用 Pydantic 的配置类，自动从环境变量 / .env 文件读取配置
class Settings(BaseSettings):
    # ---- 数据库配置（默认值可以被 .env 覆盖） ----
    pguser: str = "contoso"               # 数据库用户名
    pgpassword: str = "contoso123"        # 数据库密码
    pgdatabase: str = "contoso_expense"   # 数据库名
    pghost: str = "localhost"             # 数据库主机
    pgport: int = 5432                    # 数据库端口
    database_url: str | None = None       # 可直接提供完整连接串（优先）

    # ---- JWT 认证配置 ----
    jwt_secret: str = "change-this-in-production"  # JWT 签名秘钥
    jwt_algorithm: str = "HS256"                   # JWT 加密算法
    access_token_expire_minutes: int = 60 * 24     # token 有效期（默认一天）

    # ---- 默认种子管理员账号 ----
    default_admin_email: str = "admin@contoso.com"
    default_admin_password: str = "admin123"

    # 指定配置来源：从 .env 文件加载
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # 拼接数据库连接 URL
    @property
    def db_url(self) -> str:
        if self.database_url:   # 若已直接提供完整 URL 就用它
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.pguser}:{self.pgpassword}"
            f"@{self.pghost}:{self.pgport}/{self.pgdatabase}"
        )

# 单例配置对象
settings = Settings()
