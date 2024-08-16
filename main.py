#!/usr/bin/env python3

import argparse
from typing import Union

# Import interface modules
from interface.cli import CLI

# Import core modules
from query_processing.nl_parser import NLParser
from query_processing.query_translator.graphql_translator import GraphQLTranslator
from query_processing.query_history import QueryHistory
from search_execution.query_executor.graphql_executor import GraphQLExecutor
from result_analysis.metadata_analyzer import MetadataAnalyzer
from result_analysis.facet_generator import FacetGenerator
from result_analysis.result_ranker import ResultRanker
from data_access.upi_connector import UPIConnector
from utils.logging_service import LoggingService
from utils.llm_connector.openai_connector import OpenAIConnector

class SearchTool:
    def __init__(self, use_speech: bool = False):
        self.interface = CLI()
        self.nl_parser = NLParser()
        self.query_translator = GraphQLTranslator()
        self.query_history = QueryHistory()
        self.query_executor = GraphQLExecutor()
        self.metadata_analyzer = MetadataAnalyzer()
        self.facet_generator = FacetGenerator()
        self.result_ranker = ResultRanker()
        self.upi_connector = UPIConnector()
        self.logging_service = LoggingService()
        self.llm_connector = OpenAIConnector()

    def run(self):
        while True:
            # Get query from user
            user_query = self.interface.get_query()

            # Log the query
            self.logging_service.log_query(user_query)

            # Process the query
            parsed_query = self.nl_parser.parse(user_query)
            translated_query = self.query_translator.translate(parsed_query, self.llm_connector)

            # Execute the query
            raw_results = self.query_executor.execute(translated_query, self.upi_connector)

            # Analyze and refine results
            analyzed_results = self.metadata_analyzer.analyze(raw_results)
            facets = self.facet_generator.generate(analyzed_results)
            ranked_results = self.result_ranker.rank(analyzed_results)

            # Display results to user
            self.interface.display_results(ranked_results, facets)

            # Update query history
            self.query_history.add(user_query, ranked_results)

            # Check if user wants to continue
            if not self.interface.continue_session():
                break

        self.logging_service.log_session_end()

def main():
    parser = argparse.ArgumentParser(description="UPI Search Tool")
    parser.add_argument("--speech", action="store_true", help="Use speech interface")
    args = parser.parse_args()

    search_tool = SearchTool(use_speech=args.speech)
    search_tool.run()

if __name__ == "__main__":
    main()
