# Stripe

[Stripe](https://stripe.com/en-ca) is an Irish-American financial services and software as a service (SaaS) company. It offers payment-processing software and application programming interfaces for e-commerce websites and mobile applications.

This notebook covers how to load data from the `Stripe REST API` into a format that can be ingested into LangChain, along with example usage for vectorization.

```python
import os  
  
  
from langchain.document\_loaders import StripeLoader  
from langchain.indexes import VectorstoreIndexCreator  

```

The Stripe API requires an access token, which can be found inside of the Stripe dashboard.

This document loader also requires a `resource` option which defines what data you want to load.

Following resources are available:

`balance_transations` [Documentation](https://stripe.com/docs/api/balance_transactions/list)

`charges` [Documentation](https://stripe.com/docs/api/charges/list)

`customers` [Documentation](https://stripe.com/docs/api/customers/list)

`events` [Documentation](https://stripe.com/docs/api/events/list)

`refunds` [Documentation](https://stripe.com/docs/api/refunds/list)

`disputes` [Documentation](https://stripe.com/docs/api/disputes/list)

```python
stripe\_loader = StripeLoader("charges")  

```

```python
# Create a vectorstore retriever from the loader  
# see https://python.langchain.com/en/latest/modules/data\_connection/getting\_started.html for more details  
  
index = VectorstoreIndexCreator().from\_loaders([stripe\_loader])  
stripe\_doc\_retriever = index.vectorstore.as\_retriever()  

```
