import os
from typing import Any, Dict

import requests
import streamlit as st

from CONFIG import HASURA_GRAPHQL_URL


def execute_graphql_query(query: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Executes a GraphQL query against the Hasura endpoint.

    :param query: The GraphQL query string.
    :param variables: A dictionary of variables for the query.
    :return: The JSON response from the server as a dictionary.
    """

    if not HASURA_GRAPHQL_URL:
        st.error("Hasura URL or wss is not set. Please check your .env file.")
        return {}

    headers = {
        "Content-Type": "application/json",
        "isAnonymous": "True",
    }

    json_payload = {"query": query, "variables": variables}

    try:
        response = requests.post(HASURA_GRAPHQL_URL, json=json_payload, headers=headers)
        # Raise an exception for bad status codes
        response.raise_for_status()
        response_json = response.json()
        if "errors" in response_json:
            raise Exception(response_json["errors"][0]["message"])
        return response_json
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to Hasura endpoint: {e}")
        return {}
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return {}


@st.cache_data(ttl=60)  # Cache for 1 minute
def fetch_market_data(
    _base: str = "%GGEZ1%", _quote: str = "%USDT%", _exchange: str = "%", _exchange_type: str = "%"
) -> Dict[str, Any]:
    """
    Fetches market data from the Hasura endpoint using a specific query.
    """
    try:
        # Construct the absolute path to the GraphQL query file
        query_path = os.path.join(os.path.dirname(__file__), "gql", "get_market_data.graphql")

        # Read the GraphQL query from the file
        with open(query_path, "r") as f:
            get_market_data_query = f.read()

        variables = {"_base": f"%{_base}%", "_quote": f"%{_quote}%", "_exchange": _exchange, "_exchange_type": _exchange_type}
        result = execute_graphql_query(get_market_data_query, variables)
        return result.get("data", {})
    except FileNotFoundError:
        st.error(f"GraphQL query file not found at {query_path}")
        return {}
    except Exception as e:
        st.error(f"An unexpected error occurred in fetch_market_data: {e}")
        return {}


@st.cache_data(ttl=60)
def fetch_price_data(
    p_time_interval: str,
    p_trading_pair: str,
    p_start_time: str,
    p_end_time: str,
    p_exchange: str = None,
) -> Dict[str, Any]:
    """
    Fetches price data for a specific market and time range.
    """
    try:
        # Construct the absolute path to the GraphQL query file
        query_path = os.path.join(os.path.dirname(__file__), "gql", "get_market_candlestick_data.graphql")

        # Read the GraphQL query from the file
        with open(query_path, "r") as f:
            get_market_candlestick_data_query = f.read()

        variables = {
            "p_time_interval": p_time_interval,
            "p_trading_pair": p_trading_pair,
            "p_start_time": p_start_time,
            "p_end_time": p_end_time,
            "p_exchange": p_exchange,
        }
        result = execute_graphql_query(get_market_candlestick_data_query, variables)
        return result.get("data", {})
    except FileNotFoundError:
        st.error(f"GraphQL query file not found at {query_path}")
        return {}
    except Exception as e:
        st.error(f"An unexpected error occurred in fetch_price_data: {e}")
        return {}


@st.cache_data(ttl=60)
def fetch_price_change_summary(p_trading_pair: str) -> Dict[str, Any]:
    """
    Fetches price change summary for a specific trading pair.
    """
    try:
        # Construct the absolute path to the GraphQL query file
        query_path = os.path.join(os.path.dirname(__file__), "gql", "get_price_change_summary.graphql")

        # Read the GraphQL query from the file
        with open(query_path, "r") as f:
            get_price_change_summary_query = f.read()

        variables = {"p_trading_pair": p_trading_pair}
        result = execute_graphql_query(get_price_change_summary_query, variables)
        return result.get("data", {})
    except FileNotFoundError:
        st.error(f"GraphQL query file not found at {query_path}")
        return {}
    except Exception as e:
        st.error(f"An unexpected error occurred in fetch_price_change_summary: {e}")
        return {}
