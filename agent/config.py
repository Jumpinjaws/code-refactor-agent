from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    model: str = "gpt-4o"
    max_iterations: int = 10
    output_dir: str = "output"

    class Config:
        env_file = ".env"


settings = Settings()
