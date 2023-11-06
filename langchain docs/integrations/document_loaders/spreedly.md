# Spreedly

[Spreedly](https://docs.spreedly.com/) is a service that allows you to securely store credit cards and use them to transact against any number of payment gateways and third party APIs. It does this by simultaneously providing a card tokenization/vault service as well as a gateway and receiver integration service. Payment methods tokenized by Spreedly are stored at `Spreedly`, allowing you to independently store a card and then pass that card to different end points based on your business requirements.

This notebook covers how to load data from the [Spreedly REST API](https://docs.spreedly.com/reference/api/v1/) into a format that can be ingested into LangChain, along with example usage for vectorization.

Note: this notebook assumes the following packages are installed: `openai`, `chromadb`, and `tiktoken`.

```python
import os  
  
from langchain.document\_loaders import SpreedlyLoader  
from langchain.indexes import VectorstoreIndexCreator  

```

Spreedly API requires an access token, which can be found inside the Spreedly Admin Console.

This document loader does not currently support pagination, nor access to more complex objects which require additional parameters. It also requires a `resource` option which defines what objects you want to load.

Following resources are available:

- `gateways_options`: [Documentation](https://docs.spreedly.com/reference/api/v1/#list-supported-gateways)
- `gateways`: [Documentation](https://docs.spreedly.com/reference/api/v1/#list-created-gateways)
- `receivers_options`: [Documentation](https://docs.spreedly.com/reference/api/v1/#list-supported-receivers)
- `receivers`: [Documentation](https://docs.spreedly.com/reference/api/v1/#list-created-receivers)
- `payment_methods`: [Documentation](https://docs.spreedly.com/reference/api/v1/#list)
- `certificates`: [Documentation](https://docs.spreedly.com/reference/api/v1/#list-certificates)
- `transactions`: [Documentation](https://docs.spreedly.com/reference/api/v1/#list49)
- `environments`: [Documentation](https://docs.spreedly.com/reference/api/v1/#list-environments)

```python
spreedly\_loader = SpreedlyLoader(  
 os.environ["SPREEDLY\_ACCESS\_TOKEN"], "gateways\_options"  
)  

```

```python
# Create a vectorstore retriever from the loader  
# see https://python.langchain.com/en/latest/modules/data\_connection/getting\_started.html for more details  
  
index = VectorstoreIndexCreator().from\_loaders([spreedly\_loader])  
spreedly\_doc\_retriever = index.vectorstore.as\_retriever()  

```

```text
 Using embedded DuckDB without persistence: data will be transient  

```

```python
# Test the retriever  
spreedly\_doc\_retriever.get\_relevant\_documents("CRC")  

```

```text
 [Document(page\_content='installment\_grace\_period\_duration\nreference\_data\_code\ninvoice\_number\ntax\_management\_indicator\noriginal\_amount\ninvoice\_amount\nvat\_tax\_rate\nmobile\_remote\_payment\_type\ngratuity\_amount\nmdd\_field\_1\nmdd\_field\_2\nmdd\_field\_3\nmdd\_field\_4\nmdd\_field\_5\nmdd\_field\_6\nmdd\_field\_7\nmdd\_field\_8\nmdd\_field\_9\nmdd\_field\_10\nmdd\_field\_11\nmdd\_field\_12\nmdd\_field\_13\nmdd\_field\_14\nmdd\_field\_15\nmdd\_field\_16\nmdd\_field\_17\nmdd\_field\_18\nmdd\_field\_19\nmdd\_field\_20\nsupported\_countries: US\nAE\nBR\nCA\nCN\nDK\nFI\nFR\nDE\nIN\nJP\nMX\nNO\nSE\nGB\nSG\nLB\nPK\nsupported\_cardtypes: visa\nmaster\namerican\_express\ndiscover\ndiners\_club\njcb\ndankort\nmaestro\nelo\nregions: asia\_pacific\neurope\nlatin\_america\nnorth\_america\nhomepage: http://www.cybersource.com\ndisplay\_api\_url: https://ics2wsa.ic3.com/commerce/1.x/transactionProcessor\ncompany\_name: CyberSource', metadata={'source': 'https://core.spreedly.com/v1/gateways\_options.json'}),  
 Document(page\_content='BG\nBH\nBI\nBJ\nBM\nBN\nBO\nBR\nBS\nBT\nBW\nBY\nBZ\nCA\nCC\nCF\nCH\nCK\nCL\nCM\nCN\nCO\nCR\nCV\nCX\nCY\nCZ\nDE\nDJ\nDK\nDO\nDZ\nEC\nEE\nEG\nEH\nES\nET\nFI\nFJ\nFK\nFM\nFO\nFR\nGA\nGB\nGD\nGE\nGF\nGG\nGH\nGI\nGL\nGM\nGN\nGP\nGQ\nGR\nGT\nGU\nGW\nGY\nHK\nHM\nHN\nHR\nHT\nHU\nID\nIE\nIL\nIM\nIN\nIO\nIS\nIT\nJE\nJM\nJO\nJP\nKE\nKG\nKH\nKI\nKM\nKN\nKR\nKW\nKY\nKZ\nLA\nLC\nLI\nLK\nLS\nLT\nLU\nLV\nMA\nMC\nMD\nME\nMG\nMH\nMK\nML\nMN\nMO\nMP\nMQ\nMR\nMS\nMT\nMU\nMV\nMW\nMX\nMY\nMZ\nNA\nNC\nNE\nNF\nNG\nNI\nNL\nNO\nNP\nNR\nNU\nNZ\nOM\nPA\nPE\nPF\nPH\nPK\nPL\nPN\nPR\nPT\nPW\nPY\nQA\nRE\nRO\nRS\nRU\nRW\nSA\nSB\nSC\nSE\nSG\nSI\nSK\nSL\nSM\nSN\nST\nSV\nSZ\nTC\nTD\nTF\nTG\nTH\nTJ\nTK\nTM\nTO\nTR\nTT\nTV\nTW\nTZ\nUA\nUG\nUS\nUY\nUZ\nVA\nVC\nVE\nVI\nVN\nVU\nWF\nWS\nYE\nYT\nZA\nZM\nsupported\_cardtypes: visa\nmaster\namerican\_express\ndiscover\njcb\nmaestro\nelo\nnaranja\ncabal\nunionpay\nregions: asia\_pacific\neurope\nmiddle\_east\nnorth\_america\nhomepage: http://worldpay.com\ndisplay\_api\_url: https://secure.worldpay.com/jsp/merchant/xml/paymentService.jsp\ncompany\_name: WorldPay', metadata={'source': 'https://core.spreedly.com/v1/gateways\_options.json'}),  
 Document(page\_content='gateway\_specific\_fields: receipt\_email\nradar\_session\_id\nskip\_radar\_rules\napplication\_fee\nstripe\_account\nmetadata\nidempotency\_key\nreason\nrefund\_application\_fee\nrefund\_fee\_amount\nreverse\_transfer\naccount\_id\ncustomer\_id\nvalidate\nmake\_default\ncancellation\_reason\ncapture\_method\nconfirm\nconfirmation\_method\ncustomer\ndescription\nmoto\noff\_session\non\_behalf\_of\npayment\_method\_types\nreturn\_email\nreturn\_url\nsave\_payment\_method\nsetup\_future\_usage\nstatement\_descriptor\nstatement\_descriptor\_suffix\ntransfer\_amount\ntransfer\_destination\ntransfer\_group\napplication\_fee\_amount\nrequest\_three\_d\_secure\nerror\_on\_requires\_action\nnetwork\_transaction\_id\nclaim\_without\_transaction\_id\nfulfillment\_date\nevent\_type\nmodal\_challenge\nidempotent\_request\nmerchant\_reference\ncustomer\_reference\nshipping\_address\_zip\nshipping\_from\_zip\nshipping\_amount\nline\_items\nsupported\_countries: AE\nAT\nAU\nBE\nBG\nBR\nCA\nCH\nCY\nCZ\nDE\nDK\nEE\nES\nFI\nFR\nGB\nGR\nHK\nHU\nIE\nIN\nIT\nJP\nLT\nLU\nLV\nMT\nMX\nMY\nNL\nNO\nNZ\nPL\nPT\nRO\nSE\nSG\nSI\nSK\nUS\nsupported\_cardtypes: visa', metadata={'source': 'https://core.spreedly.com/v1/gateways\_options.json'}),  
 Document(page\_content='mdd\_field\_57\nmdd\_field\_58\nmdd\_field\_59\nmdd\_field\_60\nmdd\_field\_61\nmdd\_field\_62\nmdd\_field\_63\nmdd\_field\_64\nmdd\_field\_65\nmdd\_field\_66\nmdd\_field\_67\nmdd\_field\_68\nmdd\_field\_69\nmdd\_field\_70\nmdd\_field\_71\nmdd\_field\_72\nmdd\_field\_73\nmdd\_field\_74\nmdd\_field\_75\nmdd\_field\_76\nmdd\_field\_77\nmdd\_field\_78\nmdd\_field\_79\nmdd\_field\_80\nmdd\_field\_81\nmdd\_field\_82\nmdd\_field\_83\nmdd\_field\_84\nmdd\_field\_85\nmdd\_field\_86\nmdd\_field\_87\nmdd\_field\_88\nmdd\_field\_89\nmdd\_field\_90\nmdd\_field\_91\nmdd\_field\_92\nmdd\_field\_93\nmdd\_field\_94\nmdd\_field\_95\nmdd\_field\_96\nmdd\_field\_97\nmdd\_field\_98\nmdd\_field\_99\nmdd\_field\_100\nsupported\_countries: US\nAE\nBR\nCA\nCN\nDK\nFI\nFR\nDE\nIN\nJP\nMX\nNO\nSE\nGB\nSG\nLB\nPK\nsupported\_cardtypes: visa\nmaster\namerican\_express\ndiscover\ndiners\_club\njcb\nmaestro\nelo\nunion\_pay\ncartes\_bancaires\nmada\nregions: asia\_pacific\neurope\nlatin\_america\nnorth\_america\nhomepage: http://www.cybersource.com\ndisplay\_api\_url: https://api.cybersource.com\ncompany\_name: CyberSource REST', metadata={'source': 'https://core.spreedly.com/v1/gateways\_options.json'})]  

```
