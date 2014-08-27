invoices
========

Generates invoices to be used according to the latest (2012-2013) tax regulations.
Based on https://github.com/louridas/invoices, with the following changes:
- added an archive file to store the invoice number, date and amount. This way, every invoice takes the next number from the last one.
- added some questions to the script, so the user chooses if he/she wants to input the info while running the script, or take them from the .xml file.
- line 299 in invoice.py calls okular to open the newly generated invoice. If you do not use okular, change it to meet your needs.

Usage
=====

    python invoice.py invoice.xml
    xelatex invoice_<num>.tex

where `invoice.xml` is a file containing the data to be entered in a particular invoice. The data are contained in
the following elements:

* num: the invoice number; this number will be used to produce the output filename `invoice_<num>.tex` and to number
  the invoice itself
* date: the invoice date
* stamp: the boilerplate that is usually present in the traditional invoice stamps
* client: the client name
* occupation: the client occupation
* taxoffice: the client tax office
* address: the client address
* taxnumber: the client taxnumber
* description: the description of the work performed
* value: the value of the work performed; this is the only amount that needs to be entered, as the withholding tax,  
  the VAT, as well the string representation of the amount are produced automatically
* vat_rate: if present, the VAT rate to be applied; default is 0.23
* tax_rate: if present, the withholding tax rate to be applied; default is 0.20

A sample `invoice.xml` is included in the repo, as is an [example output](https://github.com/louridas/invoices/blob/master/invoice_1.pdf).
