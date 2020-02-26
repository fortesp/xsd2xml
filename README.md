# xsd2xml
## Generates XML based on XSD schema

### Dependencies

* `rstr`
* `xmlschema`

### Usage:
```
xmlgenerator = XMLGenerator('resources/pain.001.001.09.xsd', True, DataFacet())
print(xmlgenerator.execute()) # Output to console
xmlgenerator.write('filename.xml') # Output to file
```

### File output:
```
<?xml version='1.0' encoding='utf-8'?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09"><CstmrCdtTrfInitn><GrpHdr><MsgId>AAZ77RS1SXTE</MsgId>
<CreDtTm>2020-02-26T22:30:58.344547</CreDtTm><NbOfTxs>464</NbOfTxs><InitgPty /></GrpHdr><PmtInf><PmtInfId>KA4EF9</PmtInfId>
<PmtMtd>CHK</PmtMtd><ReqdExctnDt><Dt>2020-02-26</Dt></ReqdExctnDt><Dbtr /><DbtrAcct><Id><IBAN>TN32RZ</IBAN></Id></DbtrAcct>
<DbtrAgt><FinInstnId /></DbtrAgt><CdtTrfTxInf><PmtId><EndToEndId>VJWELM</EndToEndId></PmtId><Amt><InstdAmt 
Ccy="AWR">5379.9</InstdAmt></Amt></CdtTrfTxInf></PmtInf></CstmrCdtTrfInitn></Document>
```
