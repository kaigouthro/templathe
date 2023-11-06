# File System

LangChain provides tools for interacting with a local file system out of the box. This notebook walks through some of them.

**Note:** these tools are not recommended for use outside a sandboxed environment!

First, we'll import the tools.

```python
from langchain.tools.file\_management import (  
 ReadFileTool,  
 CopyFileTool,  
 DeleteFileTool,  
 MoveFileTool,  
 WriteFileTool,  
 ListDirectoryTool,  
)  
from langchain.agents.agent\_toolkits import FileManagementToolkit  
from tempfile import TemporaryDirectory  
  
# We'll make a temporary directory to avoid clutter  
working\_directory = TemporaryDirectory()  

```

## The FileManagementToolkit[​](#the-filemanagementtoolkit "Direct link to The FileManagementToolkit")

If you want to provide all the file tooling to your agent, it's easy to do so with the toolkit. We'll pass the temporary directory in as a root directory as a workspace for the LLM.

It's recommended to always pass in a root directory, since without one, it's easy for the LLM to pollute the working directory, and without one, there isn't any validation against
straightforward prompt injection.

```python
toolkit = FileManagementToolkit(  
 root\_dir=str(working\_directory.name)  
) # If you don't provide a root\_dir, operations will default to the current working directory  
toolkit.get\_tools()  

```

```text
 [CopyFileTool(name='copy\_file', description='Create a copy of a file in a specified location', args\_schema=<class 'langchain.tools.file\_management.copy.FileCopyInput'>, return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root\_dir='/var/folders/gf/6rnp\_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),  
 DeleteFileTool(name='file\_delete', description='Delete a file', args\_schema=<class 'langchain.tools.file\_management.delete.FileDeleteInput'>, return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root\_dir='/var/folders/gf/6rnp\_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),  
 FileSearchTool(name='file\_search', description='Recursively search for files in a subdirectory that match the regex pattern', args\_schema=<class 'langchain.tools.file\_management.file\_search.FileSearchInput'>, return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root\_dir='/var/folders/gf/6rnp\_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),  
 MoveFileTool(name='move\_file', description='Move or rename a file from one location to another', args\_schema=<class 'langchain.tools.file\_management.move.FileMoveInput'>, return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root\_dir='/var/folders/gf/6rnp\_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),  
 ReadFileTool(name='read\_file', description='Read file from disk', args\_schema=<class 'langchain.tools.file\_management.read.ReadFileInput'>, return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root\_dir='/var/folders/gf/6rnp\_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),  
 WriteFileTool(name='write\_file', description='Write file to disk', args\_schema=<class 'langchain.tools.file\_management.write.WriteFileInput'>, return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root\_dir='/var/folders/gf/6rnp\_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),  
 ListDirectoryTool(name='list\_directory', description='List files and directories in a specified folder', args\_schema=<class 'langchain.tools.file\_management.list\_dir.DirectoryListingInput'>, return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root\_dir='/var/folders/gf/6rnp\_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug')]  

```

### Selecting File System Tools[​](#selecting-file-system-tools "Direct link to Selecting File System Tools")

If you only want to select certain tools, you can pass them in as arguments when initializing the toolkit, or you can individually initialize the desired tools.

```python
tools = FileManagementToolkit(  
 root\_dir=str(working\_directory.name),  
 selected\_tools=["read\_file", "write\_file", "list\_directory"],  
).get\_tools()  
tools  

```

```text
 [ReadFileTool(name='read\_file', description='Read file from disk', args\_schema=<class 'langchain.tools.file\_management.read.ReadFileInput'>, return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root\_dir='/var/folders/gf/6rnp\_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),  
 WriteFileTool(name='write\_file', description='Write file to disk', args\_schema=<class 'langchain.tools.file\_management.write.WriteFileInput'>, return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root\_dir='/var/folders/gf/6rnp\_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug'),  
 ListDirectoryTool(name='list\_directory', description='List files and directories in a specified folder', args\_schema=<class 'langchain.tools.file\_management.list\_dir.DirectoryListingInput'>, return\_direct=False, verbose=False, callback\_manager=<langchain.callbacks.shared.SharedCallbackManager object at 0x1156f4350>, root\_dir='/var/folders/gf/6rnp\_mbx5914kx7qmmh7xzmw0000gn/T/tmpxb8c3aug')]  

```

```python
read\_tool, write\_tool, list\_tool = tools  
write\_tool.run({"file\_path": "example.txt", "text": "Hello World!"})  

```

```text
 'File written successfully to example.txt.'  

```

```python
# List files in the working directory  
list\_tool.run({})  

```

```text
 'example.txt'  

```

- [The FileManagementToolkit](#the-filemanagementtoolkit)

  - [Selecting File System Tools](#selecting-file-system-tools)

- [Selecting File System Tools](#selecting-file-system-tools)
