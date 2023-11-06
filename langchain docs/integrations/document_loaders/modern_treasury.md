# Modern Treasury

[Modern Treasury](https://www.moderntreasury.com/) simplifies complex payment operations. It is a unified platform to power products and processes that move money.

- Connect to banks and payment systems
- Track transactions and balances in real-time
- Automate payment operations for scale

This notebook covers how to load data from the `Modern Treasury REST API` into a format that can be ingested into LangChain, along with example usage for vectorization.

```python
import os  
  
  
from langchain.document\_loaders import ModernTreasuryLoader  
from langchain.indexes import VectorstoreIndexCreator  

```

The Modern Treasury API requires an organization ID and API key, which can be found in the Modern Treasury dashboard within developer settings.

This document loader also requires a `resource` option which defines what data you want to load.

Following resources are available:

`payment_orders` [Documentation](https://docs.moderntreasury.com/reference/payment-order-object)

`expected_payments` [Documentation](https://docs.moderntreasury.com/reference/expected-payment-object)

`returns` [Documentation](https://docs.moderntreasury.com/reference/return-object)

`incoming_payment_details` [Documentation](https://docs.moderntreasury.com/reference/incoming-payment-detail-object)

`counterparties` [Documentation](https://docs.moderntreasury.com/reference/counterparty-object)

`internal_accounts` [Documentation](https://docs.moderntreasury.com/reference/internal-account-object)

`external_accounts` [Documentation](https://docs.moderntreasury.com/reference/external-account-object)

`transactions` [Documentation](https://docs.moderntreasury.com/reference/transaction-object)

`ledgers` [Documentation](https://docs.moderntreasury.com/reference/ledger-object)

`ledger_accounts` [Documentation](https://docs.moderntreasury.com/reference/ledger-account-object)

`ledger_transactions` [Documentation](https://docs.moderntreasury.com/reference/ledger-transaction-object)

`events` [Documentation](https://docs.moderntreasury.com/reference/events)

`invoices` [Documentation](https://docs.moderntreasury.com/reference/invoices)

```python
modern\_treasury\_loader = ModernTreasuryLoader("payment\_orders")  

```

```python
# Create a vectorstore retriever from the loader  
# see https://python.langchain.com/en/latest/modules/data\_connection/getting\_started.html for more details  
  
index = VectorstoreIndexCreator().from\_loaders([modern\_treasury\_loader])  
modern\_treasury\_doc\_retriever = index.vectorstore.as\_retriever()  

```
