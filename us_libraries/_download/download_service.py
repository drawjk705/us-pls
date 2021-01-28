# pyright: reportUnknownMemberType=false

import logging
import os
import zipfile
from pathlib import Path
from typing import Dict

import requests

from us_libraries._config import Config
from us_libraries._download.interface import IDownloadService
from us_libraries._download.models import DatafileType, DownloadType
from us_libraries._logger.interface import ILoggerFactory
from us_libraries._scraper.interface import IScrapingService

BASE_URL = "https://www.imls.gov"


class DownloadService(IDownloadService):
    _config: Config
    _scraper: IScrapingService
    _logger: logging.Logger

    _data_prefix: Path

    def __init__(
        self, config: Config, scraper: IScrapingService, logger_factory: ILoggerFactory
    ) -> None:
        self._config = config
        self._scraper = scraper
        self._logger = logger_factory.get_logger(__name__)

        self._setup_data_dir()

    def download(self) -> None:
        scraped_dict = self._scraper.scrape_files()

        scraped_dict_for_year = scraped_dict.get(str(self._config.year))

        if scraped_dict_for_year is None:
            self._logger.info(f"There is no data for {self._config.year}")
            return

        self._try_download_resource(
            scraped_dict_for_year, "Documentation", DownloadType.Documentation
        )

        self._try_download_resource(scraped_dict_for_year, "CSV", DownloadType.CsvZip)

        self._try_download_resource(
            scraped_dict_for_year,
            "Data Element Definitions",
            DownloadType.DataElementDefinitions,
        )

    def _try_download_resource(
        self, scraped_dict: Dict[str, str], resource: str, download_type: DownloadType
    ) -> None:
        route = scraped_dict.get(resource)

        if route is None:
            self._logger.info(
                f"The resource `{resource}` does not exist for {self._config.year}"
            )
            return

        if self._resource_already_exists(download_type):
            self._logger.debug(
                f"Resources have already been downloaded for {download_type}"
            )
            return

        url = f"{BASE_URL}/{route}"

        res = requests.get(url)

        if res.status_code != 200:
            msg = f"Received a non-200 status code for {url}: {res.status_code}"

            self._logger.exception(msg)
            raise Exception(msg)

        self._write_content(
            download_type,
            res.content,
            should_unzip=str(download_type.value).endswith(".zip"),
        )

    def _resource_already_exists(self, download_type: DownloadType) -> bool:
        if download_type in [
            DownloadType.Documentation,
            DownloadType.DataElementDefinitions,
        ]:
            return Path(f"{self._data_prefix}/{download_type.value}").exists()
        elif download_type == DownloadType.CsvZip:
            for datafile_type in DatafileType:
                if not Path(f"{self._data_prefix}/{datafile_type.value}").exists():
                    return False
            return True

        return False

    def _write_content(
        self, download_type: DownloadType, content: bytes, should_unzip: bool = False
    ) -> None:
        path = f"{self._data_prefix}/{download_type.value}"

        with open(path, "wb") as f:
            f.write(content)

        if should_unzip:
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(self._data_prefix)

            self._move_content()
            os.remove(path)

    def _move_content(self) -> None:
        for directory in self._data_prefix.iterdir():
            if not directory.is_dir():
                continue
            for sub_path in directory.iterdir():
                new_name: str = sub_path.name
                if "_ae_" in sub_path.name.lower():
                    new_name = DatafileType.SystemData.value
                elif "_outlet_" in sub_path.name.lower():
                    new_name = DatafileType.OutletData.value
                elif "_state_" in sub_path.name.lower():
                    new_name = DatafileType.StateSummaryAndCharacteristicData.value
                elif "readme" in sub_path.name.lower():
                    new_name = "README.txt"

                os.rename(sub_path, self._data_prefix / new_name)
            os.rmdir(directory)

    def _setup_data_dir(self) -> None:
        self._data_prefix = Path(f"{self._config.data_dir}/{self._config.year}")

        self._data_prefix.mkdir(parents=True, exist_ok=True)
