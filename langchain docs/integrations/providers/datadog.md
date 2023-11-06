# Datadog Tracing

[ddtrace](https://github.com/DataDog/dd-trace-py) is a Datadog application performance monitoring (APM) library which provides an integration to monitor your LangChain application.

Key features of the ddtrace integration for LangChain:

- Traces: Capture LangChain requests, parameters, prompt-completions, and help visualize LangChain operations.
- Metrics: Capture LangChain request latency, errors, and token/cost usage (for OpenAI LLMs and chat models).
- Logs: Store prompt completion data for each LangChain operation.
- Dashboard: Combine metrics, logs, and trace data into a single plane to monitor LangChain requests.
- Monitors: Provide alerts in response to spikes in LangChain request latency or error rate.

Note: The ddtrace LangChain integration currently provides tracing for LLMs, chat models, Text Embedding Models, Chains, and Vectorstores.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

1. Enable APM and StatsD in your Datadog Agent, along with a Datadog API key. For example, in Docker:

```text
docker run -d --cgroupns host \  
 --pid host \  
 -v /var/run/docker.sock:/var/run/docker.sock:ro \  
 -v /proc/:/host/proc/:ro \  
 -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \  
 -e DD\_API\_KEY=<DATADOG\_API\_KEY> \  
 -p 127.0.0.1:8126:8126/tcp \  
 -p 127.0.0.1:8125:8125/udp \  
 -e DD\_DOGSTATSD\_NON\_LOCAL\_TRAFFIC=true \  
 -e DD\_APM\_ENABLED=true \  
 gcr.io/datadoghq/agent:latest  

```

2. Install the Datadog APM Python library.

```text
pip install ddtrace>=1.17  

```

3. The LangChain integration can be enabled automatically when you prefix your LangChain Python application command with `ddtrace-run`:

```text
DD\_SERVICE="my-service" DD\_ENV="staging" DD\_API\_KEY=<DATADOG\_API\_KEY> ddtrace-run python <your-app>.py  

```

**Note**: If the Agent is using a non-default hostname or port, be sure to also set `DD_AGENT_HOST`, `DD_TRACE_AGENT_PORT`, or `DD_DOGSTATSD_PORT`.

Additionally, the LangChain integration can be enabled programmatically by adding `patch_all()` or `patch(langchain=True)` before the first import of `langchain` in your application.

Note that using `ddtrace-run` or `patch_all()` will also enable the `requests` and `aiohttp` integrations which trace HTTP requests to LLM providers, as well as the `openai` integration which traces requests to the OpenAI library.

```python
from ddtrace import config, patch  
  
# Note: be sure to configure the integration before calling ``patch()``!  
# e.g. config.langchain["logs\_enabled"] = True  
  
patch(langchain=True)  
  
# to trace synchronous HTTP requests  
# patch(langchain=True, requests=True)  
  
# to trace asynchronous HTTP requests (to the OpenAI library)  
# patch(langchain=True, aiohttp=True)  
  
# to include underlying OpenAI spans from the OpenAI integration  
# patch(langchain=True, openai=True)patch\_all  

```

See the \[APM Python library documentation\]\[https://ddtrace.readthedocs.io/en/stable/installation_quickstart.html\] for more advanced usage.

## Configuration[​](#configuration "Direct link to Configuration")

See the \[APM Python library documentation\]\[https://ddtrace.readthedocs.io/en/stable/integrations.html#langchain\] for all the available configuration options.

### Log Prompt & Completion Sampling[​](#log-prompt--completion-sampling "Direct link to Log Prompt & Completion Sampling")

To enable log prompt and completion sampling, set the `DD_LANGCHAIN_LOGS_ENABLED=1` environment variable. By default, 10% of traced requests will emit logs containing the prompts and completions.

To adjust the log sample rate, see the \[APM library documentation\]\[https://ddtrace.readthedocs.io/en/stable/integrations.html#langchain\].

**Note**: Logs submission requires `DD_API_KEY` to be specified when running `ddtrace-run`.

## Troubleshooting[​](#troubleshooting "Direct link to Troubleshooting")

Need help? Create an issue on [ddtrace](https://github.com/DataDog/dd-trace-py) or contact \[Datadog support\]\[https://docs.datadoghq.com/help/\].

- [Installation and Setup](#installation-and-setup)

- [Configuration](#configuration)

  - [Log Prompt & Completion Sampling](#log-prompt--completion-sampling)

- [Troubleshooting](#troubleshooting)

- [Log Prompt & Completion Sampling](#log-prompt--completion-sampling)
