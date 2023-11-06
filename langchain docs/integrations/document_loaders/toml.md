# TOML

[TOML](https://en.wikipedia.org/wiki/TOML) is a file format for configuration files. It is intended to be easy to read and write, and is designed to map unambiguously to a dictionary. Its specification is open-source. `TOML` is implemented in many programming languages. The name `TOML` is an acronym for "Tom's Obvious, Minimal Language" referring to its creator, Tom Preston-Werner.

If you need to load `Toml` files, use the `TomlLoader`.

```python
from langchain.document\_loaders import TomlLoader  

```

```python
loader = TomlLoader("example\_data/fake\_rule.toml")  

```

```python
rule = loader.load()  

```

```python
rule  

```

```text
 [Document(page\_content='{"internal": {"creation\_date": "2023-05-01", "updated\_date": "2022-05-01", "release": ["release\_type"], "min\_endpoint\_version": "some\_semantic\_version", "os\_list": ["operating\_system\_list"]}, "rule": {"uuid": "some\_uuid", "name": "Fake Rule Name", "description": "Fake description of rule", "query": "process where process.name : \\"somequery\\"\\n", "threat": [{"framework": "MITRE ATT&CK", "tactic": {"name": "Execution", "id": "TA0002", "reference": "https://attack.mitre.org/tactics/TA0002/"}}]}}', metadata={'source': 'example\_data/fake\_rule.toml'})]  

```
