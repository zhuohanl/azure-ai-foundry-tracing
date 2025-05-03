This is a repo to try [tracing with Azure AI Foundry project library](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/trace-local-sdk?tabs=python).


As of Mary 03, 2025, we are able to utilize two clients:
- Azure OpenAI Client
- Azure AI Inference Client

Azure AI Inference Client has Native OpenTelemetry hooks; can surface traces in Azure Monitor/Foundry UI as shown in [this page](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-inference-readme?view=azure-python-preview)

In the example `run.py` we use Azure OpenAI Client thus the tracing is not automatically showing input, output and prompt of the call. Instead, we added those details as part of the tracer span to visualize them.