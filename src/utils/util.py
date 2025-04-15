import os
import requests


# option to remove temporary files
def remove_temporary_file(file_path: str) -> None:
    """remove the temporary file

    Args:
        file_path (str): file path as string
    """
    try:
        if os.path.isfile(file_path):
            os.remove(path=file_path)
    except Exception as ex:
        print(ex)


def perform_get_api_call(api_url: str, query_params: dict = None) -> dict:
    """
    This tool sends a GET request to the given API endpoint with the provided query parameters.
    Returns the API response, which contains the result of the SQL query or other data.

    Input:
    - api_endpoint: The API URL to send the request to.
    - query_params: Optional query parameters to send with the GET request.

    Output:
    - The API response as a dictionary.
    """
    headers = {"Content-Type": "application/json"}

    # Make a GET request with query parameters
    print("Calling GET API", api_url, query_params)
    response = requests.get(api_url, params=query_params, timeout=30)

    # Convert the response to a JSON dictionary
    data = response.json()
    return data


def perform_post_api_call(api_url: str, query_params: dict = None):
    """
    This tool sends a POST request to the given API endpoint with the provided query parameters.
    Returns the API response, which contains the result.

    Input:
    - api_endpoint: The API URL to send the request to.
    - query_params: query parameters to send with the POST request.

    Output:
    - The API response.
    """
    headers = {"Content-Type": "application/json"}

    # Make a POST request with query parameters
    print("Calling POST API", api_url, query_params)
    response = requests.post(api_url, json=query_params, timeout=30)

    return response

