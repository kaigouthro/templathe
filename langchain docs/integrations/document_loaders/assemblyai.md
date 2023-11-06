# AssemblyAI Audio Transcripts

The `AssemblyAIAudioTranscriptLoader` allows to transcribe audio files with the [AssemblyAI API](https://www.assemblyai.com) and loads the transcribed text into documents.

To use it, you should have the `assemblyai` python package installed, and the
environment variable `ASSEMBLYAI_API_KEY` set with your API key. Alternatively, the API key can also be passed as an argument.

More info about AssemblyAI:

- [Website](https://www.assemblyai.com/)
- [Get a Free API key](https://www.assemblyai.com/dashboard/signup)
- [AssemblyAI API Docs](https://www.assemblyai.com/docs)

## Installation[​](#installation "Direct link to Installation")

First, you need to install the `assemblyai` python package.

You can find more info about it inside the [assemblyai-python-sdk GitHub repo](https://github.com/AssemblyAI/assemblyai-python-sdk).

```python
#!pip install assemblyai  

```

## Example[​](#example "Direct link to Example")

The `AssemblyAIAudioTranscriptLoader` needs at least the `file_path` argument. Audio files can be specified as an URL or a local file path.

```python
from langchain.document\_loaders import AssemblyAIAudioTranscriptLoader  
  
audio\_file = "https://storage.googleapis.com/aai-docs-samples/nbc.mp3"  
# or a local file path: audio\_file = "./nbc.mp3"  
  
loader = AssemblyAIAudioTranscriptLoader(file\_path=audio\_file)  
  
docs = loader.load()  

```

Note: Calling `loader.load()` blocks until the transcription is finished.

The transcribed text is available in the `page_content`:

```python
docs[0].page\_content  

```

```text
"Load time, a new president and new congressional makeup. Same old ..."  

```

The `metadata` contains the full JSON response with more meta information:

```python
docs[0].metadata  

```

```text
{'language\_code': <LanguageCode.en\_us: 'en\_us'>,  
 'audio\_url': 'https://storage.googleapis.com/aai-docs-samples/nbc.mp3',  
 'punctuate': True,  
 'format\_text': True,  
 ...  
}  

```

## Transcript Formats[​](#transcript-formats "Direct link to Transcript Formats")

You can specify the `transcript_format` argument for different formats.

Depending on the format, one or more documents are returned. These are the different `TranscriptFormat` options:

- `TEXT`: One document with the transcription text
- `SENTENCES`: Multiple documents, splits the transcription by each sentence
- `PARAGRAPHS`: Multiple documents, splits the transcription by each paragraph
- `SUBTITLES_SRT`: One document with the transcript exported in SRT subtitles format
- `SUBTITLES_VTT`: One document with the transcript exported in VTT subtitles format

```python
from langchain.document\_loaders.assemblyai import TranscriptFormat  
  
loader = AssemblyAIAudioTranscriptLoader(  
 file\_path="./your\_file.mp3",  
 transcript\_format=TranscriptFormat.SENTENCES,  
)  
  
docs = loader.load()  

```

## Transcription Config[​](#transcription-config "Direct link to Transcription Config")

You can also specify the `config` argument to use different audio intelligence models.

Visit the [AssemblyAI API Documentation](https://www.assemblyai.com/docs) to get an overview of all available models!

```python
import assemblyai as aai  
  
config = aai.TranscriptionConfig(speaker\_labels=True,  
 auto\_chapters=True,  
 entity\_detection=True  
)  
  
loader = AssemblyAIAudioTranscriptLoader(  
 file\_path="./your\_file.mp3",  
 config=config  
)  

```

## Pass the API Key as argument[​](#pass-the-api-key-as-argument "Direct link to Pass the API Key as argument")

Next to setting the API key as environment variable `ASSEMBLYAI_API_KEY`, it is also possible to pass it as argument.

```python
loader = AssemblyAIAudioTranscriptLoader(  
 file\_path="./your\_file.mp3",  
 api\_key="YOUR\_KEY"  
)  

```

- [Installation](#installation)
- [Example](#example)
- [Transcript Formats](#transcript-formats)
- [Transcription Config](#transcription-config)
- [Pass the API Key as argument](#pass-the-api-key-as-argument)
