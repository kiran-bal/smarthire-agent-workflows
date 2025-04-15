import io
import os
from uuid import uuid1

import pandas as pd
from crewai.tools import tool

from constants import TEMP_FOLDER
# from constants import *
from src.utils.util import perform_get_api_call, perform_post_api_call
# from utils.pdf_report.report_generator import PdfReportGenerator


class APITools:
    """Contains the API tools"""

    @staticmethod
    @tool("Calls the API with request data and returns the response")
    def sequence_recipe_api_tool(request_data: dict) -> str:
        """
        This tool is used for calling given endpoint based on the request data
        and return the responses.

        Input:
        - request_data (dict): contains the body for sending the request
            the body should contain following parameters name, startTime, endTime, type
            - name: recipe sequence name eg:- DicingRecipeSequence. currently only available option is DicingRecipeSequence
            - startTime: start time represented in this format eg:- 2024-11-25T23:57:32.953Z
            - endTime: end time represented in this format eg:- 2024-11-25T23:57:32.953Z
            - type: type of the request. eg:- Sequence

        Output:
        - path of the file.
        """

        errors = False
        csv_file = ""
        try:
            end_point = "http://ec2-13-126-218-159.ap-south-1.compute.amazonaws.com:8008/report/generate"
            response = perform_post_api_call(
                api_url=end_point, query_params=request_data
            )
            content = response.content.decode("utf-8")
            df = pd.read_csv(io.StringIO(content))
            os.makedirs(TEMP_FOLDER, exist_ok=True)
            # Save to a local CSV file
            csv_file = f"temp/recipe_{uuid1()}.csv"
            df.to_csv(csv_file, index=False)
            print("Response:", content)
        except Exception as ex:
            raise Exception(f"Unable to call the API, error:{ex}")

        return csv_file

def sequence_recipe_api_tool():
    api_tool = APITools.sequence_recipe_api_tool
    return api_tool