import os
import boto3
import pytest
import requests

class TestApiGateway:

    @pytest.fixture()
    def viewcount_api_url(self):
        """ Get the API Gateway URL for the View Count function from CloudFormation Stack outputs """
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError('Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack')

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n"
                f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        
        # Use the correct output key for the View Count API you want to test
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "ViewCountApi"]

        if not api_outputs:
            raise KeyError(f"ViewCountApi not found in stack {stack_name}")

        return api_outputs[0]["OutputValue"]  # Extract URL from stack outputs

    @pytest.fixture()
    def updatecount_api_url(self):
        """ Get the API Gateway URL for the Update Count function from CloudFormation Stack outputs """
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError('Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack')

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n"
                f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        
        # Use the correct output key for the Update Count API you want to test
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "UpdateCountApi"]

        if not api_outputs:
            raise KeyError(f"UpdateCountApi not found in stack {stack_name}")

        return api_outputs[0]["OutputValue"]  # Extract URL from stack outputs

    def test_viewcount_api(self, viewcount_api_url):
        """ Call the View Count API Gateway endpoint and check the response """
        headers = {'origin': 'https://andrewdavis.link'}
        response = requests.get(viewcount_api_url, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert data["count"].isdigit()  # Check if 'count' is a string that represents a digit
        assert isinstance(int(data["count"]), int)  # Convert to integer to confirm the value is numeric

    def test_updatecount_api(self, updatecount_api_url):
        """ Call the Update Count API Gateway endpoint and check the response """
        headers = {'origin': 'https://andrewdavis.link'}
        response = requests.put(updatecount_api_url, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Visitor count updated successfully."
