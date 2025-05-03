import os
import json
from opentelemetry import trace
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from config import get_logger, enable_telemetry


load_dotenv()

ai_project_connection_string = os.environ["AIPROJECT_CONNECTION_STRING"]
azure_openai_connection_name = os.environ["AZURE_OPENAI_CONNECTION_NAME"]
azure_openai_deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
azure_openai_api_version = os.environ["AZURE_OPENAI_API_VERSION"]

# Initialize logging and tracing objects
logger = get_logger(__name__)
tracer = trace.get_tracer(__name__)

# Use DefaultAzureCredential but exclude managed identity to avoid IMDS calls
credential = DefaultAzureCredential(exclude_managed_identity_credential=True, logging_enable=True)

# Create project client and enable console tracing
project_client = AIProjectClient.from_connection_string(
    credential=credential,
    conn_str=ai_project_connection_string,
)

# Enable console tracing to see all traces including content
# project_client.telemetry.enable(destination=sys.stdout)
    
# Get an authenticated Azure OpenAI client with the correct connection name
client = project_client.inference.get_azure_openai_client(
    api_version=azure_openai_api_version,
    connection_name=azure_openai_connection_name
)

@tracer.start_as_current_span(name="chat_with_llm")
def chat_with_llm(messages:list):
    # Get the current span
    current_span = trace.get_current_span()
    
    # Add input message as an attribute
    if messages and len(messages) > 0:
        current_span.set_attribute("input.user_message", messages[-1].get("content", ""))
    
    # Add full prompt (all messages) as an attribute
    current_span.set_attribute("prompt.messages", json.dumps(messages))
    
    # Use the OpenAI client to create a completion
    response = client.chat.completions.create(
        model=azure_openai_deployment_name,
        messages=messages
    )

    response_content = response.choices[0].message.content
    
    # Add output response as an attribute
    current_span.set_attribute("output.content", response_content)
    
    return response_content


if __name__ == "__main__":

    # Enable telemetry but without Application Insights since it's not configured
    enable_telemetry(True)

    messages=[
            {
                "role": "user",
                "content": "How many feet are in a mile?",
            },
        ]
    
    response = chat_with_llm(messages)
    print(response)