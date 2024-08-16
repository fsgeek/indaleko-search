#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ExecutorBase(ABC):
    """
    Abstract base class for query executors.
    """

    @abstractmethod
    def execute(self, query: str, data_connector: Any) -> List[Dict[str, Any]]:
        """
        Execute the query using the provided data connector.

        Args:
            query (str): The query to execute
            data_connector (Any): The connector to the data source

        Returns:
            List[Dict[str, Any]]: The query results
        """
        pass

    @abstractmethod
    def validate_query(self, query: str) -> bool:
        """
        Validate the query before execution.

        Args:
            query (str): The query to validate

        Returns:
            bool: True if the query is valid, False otherwise
        """
        pass

    @abstractmethod
    def format_results(self, raw_results: Any) -> List[Dict[str, Any]]:
        """
        Format the raw query results into a standardized format.

        Args:
            raw_results (Any): The raw results from the query execution

        Returns:
            List[Dict[str, Any]]: The formatted results
        """
        pass
