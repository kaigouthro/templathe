# Doctran

[Doctran](https://github.com/psychic-api/doctran) is a python package. It uses LLMs and open-source
NLP libraries to transform raw text into clean, structured, information-dense documents
that are optimized for vector space retrieval. You can think of `Doctran` as a black box where
messy strings go in and nice, clean, labelled strings come out.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

```bash
pip install doctran  

```

## Document Transformers[​](#document-transformers "Direct link to Document Transformers")

### Document Interrogator[​](#document-interrogator "Direct link to Document Interrogator")

See a [usage example for DoctranQATransformer](/docs/integrations/document_transformers/doctran_interrogate_document).

```python
from langchain.document\_loaders import DoctranQATransformer  

```

### Property Extractor[​](#property-extractor "Direct link to Property Extractor")

See a [usage example for DoctranPropertyExtractor](/docs/integrations/document_transformers/doctran_extract_properties).

```python
from langchain.document\_loaders import DoctranPropertyExtractor  

```

### Document Translator[​](#document-translator "Direct link to Document Translator")

See a [usage example for DoctranTextTranslator](/docs/integrations/document_transformers/doctran_translate_document).

```python
from langchain.document\_loaders import DoctranTextTranslator  

```

- [Installation and Setup](#installation-and-setup)

- [Document Transformers](#document-transformers)

  - [Document Interrogator](#document-interrogator)
  - [Property Extractor](#property-extractor)
  - [Document Translator](#document-translator)

- [Document Interrogator](#document-interrogator)

- [Property Extractor](#property-extractor)

- [Document Translator](#document-translator)
