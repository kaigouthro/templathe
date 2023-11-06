# Multi-language anonymization

# Multi-language data anonymization with Microsoft Presidio

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/privacy/presidio_data_anonymization/multi_language.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

## Use case[​](#use-case "Direct link to Use case")

Multi-language support in data pseudonymization is essential due to differences in language structures and cultural contexts. Different languages may have varying formats for personal identifiers. For example, the structure of names, locations and dates can differ greatly between languages and regions. Furthermore, non-alphanumeric characters, accents, and the direction of writing can impact pseudonymization processes. Without multi-language support, data could remain identifiable or be misinterpreted, compromising data privacy and accuracy. Hence, it enables effective and precise pseudonymization suited for global operations.

## Overview[​](#overview "Direct link to Overview")

PII detection in Microsoft Presidio relies on several components - in addition to the usual pattern matching (e.g. using regex), the analyser uses a model for Named Entity Recognition (NER) to extract entities such as:

- `PERSON`
- `LOCATION`
- `DATE_TIME`
- `NRP`
- `ORGANIZATION`

[\[Source\]](https://github.com/microsoft/presidio/blob/main/presidio-analyzer/presidio_analyzer/predefined_recognizers/spacy_recognizer.py)

To handle NER in specific languages, we utilize unique models from the `spaCy` library, recognized for its extensive selection covering multiple languages and sizes. However, it's not restrictive, allowing for integration of alternative frameworks such as [Stanza](https://microsoft.github.io/presidio/analyzer/nlp_engines/spacy_stanza/) or [transformers](https://microsoft.github.io/presidio/analyzer/nlp_engines/transformers/) when necessary.

## Quickstart[​](#quickstart "Direct link to Quickstart")

```python
# Install necessary packages  
# ! pip install langchain langchain-experimental openai presidio-analyzer presidio-anonymizer spacy Faker  
# ! python -m spacy download en\_core\_web\_lg  

```

```python
from langchain\_experimental.data\_anonymizer import PresidioReversibleAnonymizer  
  
anonymizer = PresidioReversibleAnonymizer(  
 analyzed\_fields=["PERSON"],  
)  

```

By default, `PresidioAnonymizer` and `PresidioReversibleAnonymizer` use a model trained on English texts, so they handle other languages moderately well.

For example, here the model did not detect the person:

```python
anonymizer.anonymize("Me llamo Sofía") # "My name is Sofía" in Spanish  

```

```text
 'Me llamo Sofía'  

```

They may also take words from another language as actual entities. Here, both the word *'Yo'* (*'I'* in Spanish) and *Sofía* have been classified as `PERSON`:

```python
anonymizer.anonymize("Yo soy Sofía") # "I am Sofía" in Spanish  

```

```text
 'Kari Lopez soy Mary Walker'  

```

If you want to anonymise texts from other languages, you need to download other models and add them to the anonymiser configuration:

```python
# Download the models for the languages you want to use  
# ! python -m spacy download en\_core\_web\_md  
# ! python -m spacy download es\_core\_news\_md  

```

```python
nlp\_config = {  
 "nlp\_engine\_name": "spacy",  
 "models": [  
 {"lang\_code": "en", "model\_name": "en\_core\_web\_md"},  
 {"lang\_code": "es", "model\_name": "es\_core\_news\_md"},  
 ],  
}  

```

We have therefore added a Spanish language model. Note also that we have downloaded an alternative model for English as well - in this case we have replaced the large model `en_core_web_lg` (560MB) with its smaller version `en_core_web_md` (40MB) - the size is therefore reduced by 14 times! If you care about the speed of anonymisation, it is worth considering it.

All models for the different languages can be found in the [spaCy documentation](https://spacy.io/usage/models).

Now pass the configuration as the `languages_config` parameter to Anonymiser. As you can see, both previous examples work flawlessly:

```python
anonymizer = PresidioReversibleAnonymizer(  
 analyzed\_fields=["PERSON"],  
 languages\_config=nlp\_config,  
)  
  
print(  
 anonymizer.anonymize("Me llamo Sofía", language="es")  
) # "My name is Sofía" in Spanish  
print(anonymizer.anonymize("Yo soy Sofía", language="es")) # "I am Sofía" in Spanish  

```

```text
 Me llamo Christopher Smith  
 Yo soy Joseph Jenkins  

```

By default, the language indicated first in the configuration will be used when anonymising text (in this case English):

```python
print(anonymizer.anonymize("My name is John"))  

```

```text
 My name is Shawna Bennett  

```

## Usage with other frameworks[​](#usage-with-other-frameworks "Direct link to Usage with other frameworks")

### Language detection[​](#language-detection "Direct link to Language detection")

One of the drawbacks of the presented approach is that we have to pass the **language** of the input text directly. However, there is a remedy for that - *language detection* libraries.

We recommend using one of the following frameworks:

- fasttext (recommended)
- langdetect

From our experience *fasttext* performs a bit better, but you should verify it on your use case.

```python
# Install necessary packages  
# ! pip install fasttext langdetect  

```

### langdetect[​](#langdetect "Direct link to langdetect")

```python
import langdetect  
from langchain.schema import runnable  
  
  
def detect\_language(text: str) -> dict:  
 language = langdetect.detect(text)  
 print(language)  
 return {"text": text, "language": language}  
  
  
chain = runnable.RunnableLambda(detect\_language) | (  
 lambda x: anonymizer.anonymize(x["text"], language=x["language"])  
)  

```

```python
chain.invoke("Me llamo Sofía")  

```

```text
 es  
  
  
  
  
  
 'Me llamo Michael Perez III'  

```

```python
chain.invoke("My name is John Doe")  

```

```text
 en  
  
  
  
  
  
 'My name is Ronald Bennett'  

```

### fasttext[​](#fasttext "Direct link to fasttext")

You need to download the fasttext model first from <https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz>

```python
import fasttext  
  
model = fasttext.load\_model("lid.176.ftz")  
  
  
def detect\_language(text: str) -> dict:  
 language = model.predict(text)[0][0].replace("\_\_label\_\_", "")  
 print(language)  
 return {"text": text, "language": language}  
  
  
chain = runnable.RunnableLambda(detect\_language) | (  
 lambda x: anonymizer.anonymize(x["text"], language=x["language"])  
)  

```

```text
 Warning : `load\_model` does not return WordVectorModel or SupervisedModel any more, but a `FastText` object which is very similar.  

```

```python
chain.invoke("Yo soy Sofía")  

```

```text
 es  
  
  
  
  
  
 'Yo soy Angela Werner'  

```

```python
chain.invoke("My name is John Doe")  

```

```text
 en  
  
  
  
  
  
 'My name is Carlos Newton'  

```

This way you only need to initialize the model with the engines corresponding to the relevant languages, but using the tool is fully automated.

## Advanced usage[​](#advanced-usage "Direct link to Advanced usage")

### Custom labels in NER model[​](#custom-labels-in-ner-model "Direct link to Custom labels in NER model")

It may be that the spaCy model has different class names than those supported by the Microsoft Presidio by default. Take Polish, for example:

```python
# ! python -m spacy download pl\_core\_news\_md  
  
import spacy  
  
nlp = spacy.load("pl\_core\_news\_md")  
doc = nlp("Nazywam się Wiktoria") # "My name is Wiktoria" in Polish  
  
for ent in doc.ents:  
 print(  
 f"Text: {ent.text}, Start: {ent.start\_char}, End: {ent.end\_char}, Label: {ent.label\_}"  
 )  

```

```text
 Text: Wiktoria, Start: 12, End: 20, Label: persName  

```

The name *Victoria* was classified as `persName`, which does not correspond to the default class names `PERSON`/`PER` implemented in Microsoft Presidio (look for `CHECK_LABEL_GROUPS` in [SpacyRecognizer implementation](https://github.com/microsoft/presidio/blob/main/presidio-analyzer/presidio_analyzer/predefined_recognizers/spacy_recognizer.py)).

You can find out more about custom labels in spaCy models (including your own, trained ones) in [this thread](https://github.com/microsoft/presidio/issues/851).

That's why our sentence will not be anonymized:

```python
nlp\_config = {  
 "nlp\_engine\_name": "spacy",  
 "models": [  
 {"lang\_code": "en", "model\_name": "en\_core\_web\_md"},  
 {"lang\_code": "es", "model\_name": "es\_core\_news\_md"},  
 {"lang\_code": "pl", "model\_name": "pl\_core\_news\_md"},  
 ],  
}  
  
anonymizer = PresidioReversibleAnonymizer(  
 analyzed\_fields=["PERSON", "LOCATION", "DATE\_TIME"],  
 languages\_config=nlp\_config,  
)  
  
print(  
 anonymizer.anonymize("Nazywam się Wiktoria", language="pl")  
) # "My name is Wiktoria" in Polish  

```

```text
 Nazywam się Wiktoria  

```

To address this, create your own `SpacyRecognizer` with your own class mapping and add it to the anonymizer:

```python
from presidio\_analyzer.predefined\_recognizers import SpacyRecognizer  
  
polish\_check\_label\_groups = [  
 ({"LOCATION"}, {"placeName", "geogName"}),  
 ({"PERSON"}, {"persName"}),  
 ({"DATE\_TIME"}, {"date", "time"}),  
]  
  
spacy\_recognizer = SpacyRecognizer(  
 supported\_language="pl",  
 check\_label\_groups=polish\_check\_label\_groups,  
)  
  
anonymizer.add\_recognizer(spacy\_recognizer)  

```

Now everything works smoothly:

```python
print(  
 anonymizer.anonymize("Nazywam się Wiktoria", language="pl")  
) # "My name is Wiktoria" in Polish  

```

```text
 Nazywam się Morgan Walters  

```

Let's try on more complex example:

```python
print(  
 anonymizer.anonymize(  
 "Nazywam się Wiktoria. Płock to moje miasto rodzinne. Urodziłam się dnia 6 kwietnia 2001 roku",  
 language="pl",  
 )  
) # "My name is Wiktoria. Płock is my home town. I was born on 6 April 2001" in Polish  

```

```text
 Nazywam się Ernest Liu. New Taylorburgh to moje miasto rodzinne. Urodziłam się 1987-01-19  

```

As you can see, thanks to class mapping, the anonymiser can cope with different types of entities.

### Custom language-specific operators[​](#custom-language-specific-operators "Direct link to Custom language-specific operators")

In the example above, the sentence has been anonymised correctly, but the fake data does not fit the Polish language at all. Custom operators can therefore be added, which will resolve the issue:

```python
from faker import Faker  
from presidio\_anonymizer.entities import OperatorConfig  
  
fake = Faker(locale="pl\_PL") # Setting faker to provide Polish data  
  
new\_operators = {  
 "PERSON": OperatorConfig("custom", {"lambda": lambda \_: fake.first\_name\_female()}),  
 "LOCATION": OperatorConfig("custom", {"lambda": lambda \_: fake.city()}),  
}  
  
anonymizer.add\_operators(new\_operators)  

```

```python
print(  
 anonymizer.anonymize(  
 "Nazywam się Wiktoria. Płock to moje miasto rodzinne. Urodziłam się dnia 6 kwietnia 2001 roku",  
 language="pl",  
 )  
) # "My name is Wiktoria. Płock is my home town. I was born on 6 April 2001" in Polish  

```

```text
 Nazywam się Marianna. Szczecin to moje miasto rodzinne. Urodziłam się 1976-11-16  

```

### Limitations[​](#limitations "Direct link to Limitations")

Remember - results are as good as your recognizers and as your NER models!

Look at the example below - we downloaded the small model for Spanish (12MB) and it no longer performs as well as the medium version (40MB):

```python
# ! python -m spacy download es\_core\_news\_sm  
  
for model in ["es\_core\_news\_sm", "es\_core\_news\_md"]:  
 nlp\_config = {  
 "nlp\_engine\_name": "spacy",  
 "models": [  
 {"lang\_code": "es", "model\_name": model},  
 ],  
 }  
  
 anonymizer = PresidioReversibleAnonymizer(  
 analyzed\_fields=["PERSON"],  
 languages\_config=nlp\_config,  
 )  
  
 print(  
 f"Model: {model}. Result: {anonymizer.anonymize('Me llamo Sofía', language='es')}"  
 )  

```

```text
 Model: es\_core\_news\_sm. Result: Me llamo Sofía  
 Model: es\_core\_news\_md. Result: Me llamo Lawrence Davis  

```

In many cases, even the larger models from spaCy will not be sufficient - there are already other, more complex and better methods of detecting named entities, based on transformers. You can read more about this [here](https://microsoft.github.io/presidio/analyzer/nlp_engines/transformers/).

- [Use case](#use-case)

- [Overview](#overview)

- [Quickstart](#quickstart)

- [Usage with other frameworks](#usage-with-other-frameworks)

  - [Language detection](#language-detection)
  - [langdetect](#langdetect)
  - [fasttext](#fasttext)

- [Advanced usage](#advanced-usage)

  - [Custom labels in NER model](#custom-labels-in-ner-model)
  - [Custom language-specific operators](#custom-language-specific-operators)
  - [Limitations](#limitations)

- [Language detection](#language-detection)

- [langdetect](#langdetect)

- [fasttext](#fasttext)

- [Custom labels in NER model](#custom-labels-in-ner-model)

- [Custom language-specific operators](#custom-language-specific-operators)

- [Limitations](#limitations)
