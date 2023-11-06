# Microsoft Excel

The `UnstructuredExcelLoader` is used to load `Microsoft Excel` files. The loader works with both `.xlsx` and `.xls` files. The page content will be the raw text of the Excel file. If you use the loader in `"elements"` mode, an HTML representation of the Excel file will be available in the document metadata under the `text_as_html` key.

```python
from langchain.document\_loaders import UnstructuredExcelLoader  

```

```python
loader = UnstructuredExcelLoader("example\_data/stanley-cups.xlsx", mode="elements")  
docs = loader.load()  
docs[0]  

```

```text
 Document(page\_content='\n \n \n Team\n Location\n Stanley Cups\n \n \n Blues\n STL\n 1\n \n \n Flyers\n PHI\n 2\n \n \n Maple Leafs\n TOR\n 13\n \n \n', metadata={'source': 'example\_data/stanley-cups.xlsx', 'filename': 'stanley-cups.xlsx', 'file\_directory': 'example\_data', 'filetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'page\_number': 1, 'page\_name': 'Stanley Cups', 'text\_as\_html': '<table border="1" class="dataframe">\n <tbody>\n <tr>\n <td>Team</td>\n <td>Location</td>\n <td>Stanley Cups</td>\n </tr>\n <tr>\n <td>Blues</td>\n <td>STL</td>\n <td>1</td>\n </tr>\n <tr>\n <td>Flyers</td>\n <td>PHI</td>\n <td>2</td>\n </tr>\n <tr>\n <td>Maple Leafs</td>\n <td>TOR</td>\n <td>13</td>\n </tr>\n </tbody>\n</table>', 'category': 'Table'})  

```
