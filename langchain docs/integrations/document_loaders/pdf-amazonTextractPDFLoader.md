# Amazon Textract

Amazon Textract is a machine learning (ML) service that automatically extracts text, handwriting, and data from scanned documents. It goes beyond simple optical character recognition (OCR) to identify, understand, and extract data from forms and tables. Today, many companies manually extract data from scanned documents such as PDFs, images, tables, and forms, or through simple OCR software that requires manual configuration (which often must be updated when the form changes). To overcome these manual and expensive processes, Textract uses ML to read and process any type of document, accurately extracting text, handwriting, tables, and other data with no manual effort. You can quickly automate document processing and act on the information extracted, whether you’re automating loans processing or extracting information from invoices and receipts. Textract can extract the data in minutes instead of hours or days.

This sample demonstrates the use of Amazon Textract in combination with LangChain as a DocumentLoader.

Textract supports PDF, TIFF, PNG and JPEG format.

Check <https://docs.aws.amazon.com/textract/latest/dg/limits-document.html> for supported document sizes, languages and characters.

```bash
pip install langchain boto3 openai tiktoken python-dotenv -q  

```

```text
   
 [notice] A new release of pip is available: 23.2 -> 23.2.1  
 [notice] To update, run: python -m pip install --upgrade pip  

```

## Sample 1[​](#sample-1 "Direct link to Sample 1")

The first example uses a local file, which internally will be send to Amazon Textract sync API [DetectDocumentText](https://docs.aws.amazon.com/textract/latest/dg/API_DetectDocumentText.html).

Local files or URL endpoints like HTTP:// are limited to one page documents for Textract.
Multi-page documents have to reside on S3. This sample file is a jpeg.

```python
from langchain.document\_loaders import AmazonTextractPDFLoader  
loader = AmazonTextractPDFLoader("example\_data/alejandro\_rosalez\_sample-small.jpeg")  
documents = loader.load()  

```

Output from the file

```python
documents  

```

```text
 [Document(page\_content='Patient Information First Name: ALEJANDRO Last Name: ROSALEZ Date of Birth: 10/10/1982 Sex: M Marital Status: MARRIED Email Address: Address: 123 ANY STREET City: ANYTOWN State: CA Zip Code: 12345 Phone: 646-555-0111 Emergency Contact 1: First Name: CARLOS Last Name: SALAZAR Phone: 212-555-0150 Relationship to Patient: BROTHER Emergency Contact 2: First Name: JANE Last Name: DOE Phone: 650-555-0123 Relationship FRIEND to Patient: Did you feel fever or feverish lately? Yes No Are you having shortness of breath? Yes No Do you have a cough? Yes No Did you experience loss of taste or smell? Yes No Where you in contact with any confirmed COVID-19 positive patients? Yes No Did you travel in the past 14 days to any regions affected by COVID-19? Yes No Patient Information First Name: ALEJANDRO Last Name: ROSALEZ Date of Birth: 10/10/1982 Sex: M Marital Status: MARRIED Email Address: Address: 123 ANY STREET City: ANYTOWN State: CA Zip Code: 12345 Phone: 646-555-0111 Emergency Contact 1: First Name: CARLOS Last Name: SALAZAR Phone: 212-555-0150 Relationship to Patient: BROTHER Emergency Contact 2: First Name: JANE Last Name: DOE Phone: 650-555-0123 Relationship FRIEND to Patient: Did you feel fever or feverish lately? Yes No Are you having shortness of breath? Yes No Do you have a cough? Yes No Did you experience loss of taste or smell? Yes No Where you in contact with any confirmed COVID-19 positive patients? Yes No Did you travel in the past 14 days to any regions affected by COVID-19? Yes No ', metadata={'source': 'example\_data/alejandro\_rosalez\_sample-small.jpeg', 'page': 1})]  

```

## Sample 2[​](#sample-2 "Direct link to Sample 2")

The next sample loads a file from an HTTPS endpoint.
It has to be single page, as Amazon Textract requires all multi-page documents to be stored on S3.

```python
from langchain.document\_loaders import AmazonTextractPDFLoader  
loader = AmazonTextractPDFLoader("https://amazon-textract-public-content.s3.us-east-2.amazonaws.com/langchain/alejandro\_rosalez\_sample\_1.jpg")  
documents = loader.load()  

```

```python
documents  

```

```text
 [Document(page\_content='Patient Information First Name: ALEJANDRO Last Name: ROSALEZ Date of Birth: 10/10/1982 Sex: M Marital Status: MARRIED Email Address: Address: 123 ANY STREET City: ANYTOWN State: CA Zip Code: 12345 Phone: 646-555-0111 Emergency Contact 1: First Name: CARLOS Last Name: SALAZAR Phone: 212-555-0150 Relationship to Patient: BROTHER Emergency Contact 2: First Name: JANE Last Name: DOE Phone: 650-555-0123 Relationship FRIEND to Patient: Did you feel fever or feverish lately? Yes No Are you having shortness of breath? Yes No Do you have a cough? Yes No Did you experience loss of taste or smell? Yes No Where you in contact with any confirmed COVID-19 positive patients? Yes No Did you travel in the past 14 days to any regions affected by COVID-19? Yes No Patient Information First Name: ALEJANDRO Last Name: ROSALEZ Date of Birth: 10/10/1982 Sex: M Marital Status: MARRIED Email Address: Address: 123 ANY STREET City: ANYTOWN State: CA Zip Code: 12345 Phone: 646-555-0111 Emergency Contact 1: First Name: CARLOS Last Name: SALAZAR Phone: 212-555-0150 Relationship to Patient: BROTHER Emergency Contact 2: First Name: JANE Last Name: DOE Phone: 650-555-0123 Relationship FRIEND to Patient: Did you feel fever or feverish lately? Yes No Are you having shortness of breath? Yes No Do you have a cough? Yes No Did you experience loss of taste or smell? Yes No Where you in contact with any confirmed COVID-19 positive patients? Yes No Did you travel in the past 14 days to any regions affected by COVID-19? Yes No ', metadata={'source': 'example\_data/alejandro\_rosalez\_sample-small.jpeg', 'page': 1})]  

```

## Sample 3[​](#sample-3 "Direct link to Sample 3")

Processing a multi-page document requires the document to be on S3. The sample document resides in a bucket in us-east-2 and Textract needs to be called in that same region to be successful, so we set the region_name on the client and pass that in to the loader to ensure Textract is called from us-east-2. You could also to have your notebook running in us-east-2, setting the AWS_DEFAULT_REGION set to us-east-2 or when running in a different environment, pass in a boto3 Textract client with that region name like in the cell below.

```python
import boto3  
textract\_client = boto3.client('textract', region\_name='us-east-2')  
  
file\_path = "s3://amazon-textract-public-content/langchain/layout-parser-paper.pdf"  
loader = AmazonTextractPDFLoader(file\_path, client=textract\_client)  
documents = loader.load()  

```

Now getting the number of pages to validate the response (printing out the full response would be quite long...). We expect 16 pages.

```python
len(documents)  

```

```text
 16  

```

## Using the AmazonTextractPDFLoader in an LangChain chain (e. g. OpenAI)[​](#using-the-amazontextractpdfloader-in-an-langchain-chain-e-g-openai "Direct link to Using the AmazonTextractPDFLoader in an LangChain chain (e. g. OpenAI)")

The AmazonTextractPDFLoader can be used in a chain the same way the other loaders are used.
Textract itself does have a [Query feature](https://docs.aws.amazon.com/textract/latest/dg/API_Query.html), which offers similar functionality to the QA chain in this sample, which is worth checking out as well.

```python
# You can store your OPENAI\_API\_KEY in a .env file as well  
# import os   
# from dotenv import load\_dotenv  
  
# load\_dotenv()  

```

```python
# Or set the OpenAI key in the environment directly  
import os   
os.environ["OPENAI\_API\_KEY"] = "your-OpenAI-API-key"  

```

```python
from langchain.llms import OpenAI  
from langchain.chains.question\_answering import load\_qa\_chain  
  
chain = load\_qa\_chain(llm=OpenAI(), chain\_type="map\_reduce")  
query = ["Who are the autors?"]  
  
chain.run(input\_documents=documents, question=query)  

```

```text
 ' The authors are Zejiang Shen, Ruochen Zhang, Melissa Dell, Benjamin Charles Germain Lee, Jacob Carlson, Weining Li, Gardner, M., Grus, J., Neumann, M., Tafjord, O., Dasigi, P., Liu, N., Peters, M., Schmitz, M., Zettlemoyer, L., Lukasz Garncarek, Powalski, R., Stanislawek, T., Topolski, B., Halama, P., Gralinski, F., Graves, A., Fernández, S., Gomez, F., Schmidhuber, J., Harley, A.W., Ufkes, A., Derpanis, K.G., He, K., Gkioxari, G., Dollár, P., Girshick, R., He, K., Zhang, X., Ren, S., Sun, J., Kay, A., Lamiroy, B., Lopresti, D., Mears, J., Jakeway, E., Ferriter, M., Adams, C., Yarasavage, N., Thomas, D., Zwaard, K., Li, M., Cui, L., Huang,'  

```

- [Sample 1](#sample-1)
- [Sample 2](#sample-2)
- [Sample 3](#sample-3)
- [Using the AmazonTextractPDFLoader in an LangChain chain (e. g. OpenAI)](#using-the-amazontextractpdfloader-in-an-langchain-chain-e-g-openai)
