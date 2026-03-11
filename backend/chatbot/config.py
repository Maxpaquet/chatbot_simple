import os
from threading import Lock
from typing import Dict, Literal, Optional, cast

import yaml
from dotenv import load_dotenv
from langfuse import Langfuse # , get_client
# from langfuse.langchain import CallbackHandler
from pydantic import BaseModel, ConfigDict

LLM_SERVICES = ["gemini", "ollama"]
LLM_MODEL_NAMES = [
    "gemini",
    "gemini-pro",
    "gemini-flash-lite",
    "qwen3:8b",
]


class LLMModelConfig(BaseModel):
    service: Literal["gemini", "ollama"]
    model_name: Literal["gemini", "gemini-pro", "gemini-flash-lite", "qwen3:8b"]
    temperature: float
    seed: int | None = None

    def __str__(self):
        return f"LLMModelConfig(service={self.service}, model_name={self.model_name}, temperature={self.temperature}, seed={self.seed})"


class LLM(BaseModel):
    models: Dict[str, LLMModelConfig]
    default_model: str

    def default(self) -> LLMModelConfig:
        return self.models[self.default_model]

    def __str__(self):
        return f"LLM(default_model={self.default_model}, models={self.models})"

class LangfuseConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    langfuse: Langfuse
    # langfuse_handler: CallbackHandler


class Config:
    _instance = None
    _lock = Lock()

    mock: bool
    verbose: bool
    langfuse_bool: bool
    llm: LLM
    langfuse_config: Optional[LangfuseConfig]

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                # Another thread could have created the instance
                # before this one acquired the lock.
                if not cls._instance:
                    cls._instance = super(Config, cls).__new__(cls)
                    cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Loads the configuration from the YAML file."""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "resources", "config.yaml"
        )
        try:
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f)
            if config_data:
                # Load mock boolean
                self.mock = config_data.get("mock", False)
                # Load verbose boolean
                self.verbose = config_data.get("verbose", False)
                # Langfuse bool
                self.langfuse_bool = config_data.get("langfuse_bool", False)
                # Load LLM models configuration
                llm_models = {}
                llm: Dict = config_data.get("llm", {})

                llm_models_data: Dict[str, Dict[str, str | float | int]] = llm.get(
                    "llm_models", {}
                )
                for model_name, model_config in llm_models_data.items():
                    service_: Literal["gemini", "ollama"] = cast(
                        Literal["gemini", "ollama"], model_config.get("service")
                    )
                    model_name_: Literal[
                        "gemini", "gemini-pro", "gemini-flash-lite", "qwen3:8b"
                    ] = cast(
                        Literal[
                            "gemini", "gemini-pro", "gemini-flash-lite", "qwen3:8b"
                        ],
                        model_config.get("model_name"),
                    )

                    llm_models[model_name] = LLMModelConfig(
                        service=service_,
                        model_name=model_name_,
                        temperature=float(model_config["temperature"]),
                        seed=(
                            int(model_config["seed"])
                            if isinstance(model_config.get("seed"), int)
                            else None
                        ),
                    )
                default_model: str | None = llm.get("default_model", None)
                if default_model is None:
                    raise ValueError("Default model not specified in config.yaml")
                self.llm = LLM(models=llm_models, default_model=default_model)

                # Langfuse configuration can be added here similarly
                if self.langfuse_bool:
                    load_dotenv()
                    langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
                    langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
                    langfuse_base_url = os.getenv("LANGFUSE_BASE_URL")
                    Langfuse(
                        public_key=langfuse_public_key,
                        secret_key=langfuse_secret_key,
                        host=langfuse_base_url,
                    )
                    # self.langfuse_config = LangfuseConfig(
                    #     langfuse=get_client(),
                    #     langfuse_handler=CallbackHandler(),
                    # )
                else:
                    self.langfuse_config = None
            else:
                self.mock = False
        except FileNotFoundError:
            # Handle the case where the config file doesn't exist
            print(f"Warning: Config file not found at {config_path}")
            self.mock = False
        except yaml.YAMLError as e:
            # Handle errors during YAML parsing
            print(f"Error parsing YAML file: {e}")
            self.mock = False

    def __str__(self):
        return f"Config(mock={self.mock}, llm={self.llm})"


# To be used as a singleton instance across the application
config = Config()
