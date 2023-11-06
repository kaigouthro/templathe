# Nuclia

[Nuclia](https://nuclia.com) automatically indexes your unstructured data from any internal
and external source, providing optimized search results and generative answers.
It can handle video and audio transcription, image content extraction, and document parsing.

`Nuclia Understanding API` document transformer splits text into paragraphs and sentences,
identifies entities, provides a summary of the text and generates embeddings for all the sentences.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

We need to install the `nucliadb-protos` package to use the `Nuclia Understanding API`.

```bash
pip install nucliadb-protos  

```

To use the `Nuclia Understanding API`, we need to have a `Nuclia account`.
We can create one for free at <https://nuclia.cloud>,
and then [create a NUA key](https://docs.nuclia.dev/docs/docs/using/understanding/intro).

To use the Nuclia document transformer, we need to instantiate a `NucliaUnderstandingAPI`
tool with `enable_ml` set to `True`:

```python
from langchain.tools.nuclia import NucliaUnderstandingAPI  
  
nua = NucliaUnderstandingAPI(enable\_ml=True)  

```

## Document Transformer[​](#document-transformer "Direct link to Document Transformer")

See a [usage example](/docs/integrations/document_transformers/nuclia_transformer).

```python
from langchain.document\_transformers.nuclia\_text\_transform import NucliaTextTransformer  

```

- [Installation and Setup](#installation-and-setup)
- [Document Transformer](#document-transformer)
