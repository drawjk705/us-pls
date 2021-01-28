from dataclasses import dataclass, field

from us_libraries._logger.configure_logger import DEFAULT_LOG_FILE

DEFAULT_DATA_DIR = "data"


@dataclass(frozen=True)
class Config:
    year: int
    data_dir: str = field(default=DEFAULT_DATA_DIR)
    log_file: str = field(default=DEFAULT_LOG_FILE)
    should_overwrite_cached_urls: bool = field(default=False)
    should_overwrite_existing_cache: bool = field(default=False)
