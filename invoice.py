#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import with_statement
from datetime import datetime
from subprocess import call

import codecs
import sys
import xml.etree.ElementTree as ET

one_to_twenty_n = [
    'ένα',
    'δύο',
    'τρία',
    'τέσσερα',
    'πέντε',
    'έξι',
    'επτά',
    'οκτώ',
    'εννέα',
    'δέκα',
    'έντεκα',
    'δώδεκα',
    'δεκατρία',
    'δεκατέσσερα',
    'δεκαπέντε',
    'δεκαέξι',
    'δεκαεπτά',
    'δεκαοκτώ',
    'δεκαεννέα'
    ]

one_to_twenty_f = [
    'μία',
    'δύο',
    'τρεις',
    'τέσσερεις',
    'πέντε',
    'έξι',
    'επτά',
    'οκτώ',
    'εννέα',
    'δέκα',
    'έντεκα',
    'δώδεκα',
    'δεκατρείς',
    'δεκατέσσερεις',
    'δεκαπέντε',
    'δεκαέξι',
    'δεκαεπτά',
    'δεκαοκτώ',
    'δεκαεννέα'
    ]

tens = [
    'δέκα',
    'είκοσι',
    'τριάντα',
    'σαράντα',
    'πενήντα',
    'εξήντα',
    'εβδομήντα',
    'ογδόντα',
    'ενενήντα'
    ]

hundreds_n = [
    'εκατό',
    'διακόσια',
    'τριακόσια',
    'τετρακόσια',
    'πεντακόσια',
    'εξακόσια',
    'επτακόσια',
    'οκτακόσια',
    'εννιακόσια'
    ]

hundreds_f = [
    'εκατό',
    'διακόσιες',
    'τριακόσιες',
    'τετρακόσιες',
    'πεντακόσιες',
    'εξακόσιες',
    'επτακόσιες',
    'οκτακόσιες',
    'εννιακόσιες'
    ]

thousands = [
    'χίλια',
    'χιλιάδες'
    ]

millions = [
    'εκατομμύριο',
    'εκατομμύρια'
    ]

billions = [
    'δισεκατομμύριο',
    'δισεκατομμύρια'
    ]

def num_to_text_hundreds(number, f):
    parts = []
    h, mod100 = divmod(number, 100)
    t, mod10 = divmod(mod100, 10)
    if h > 0:
        if h == 1 and mod100 > 0:
            parts.append(hundreds_n[h - 1] + 'ν')
        else:
            if f == True:
                parts.append(hundreds_f[h - 1])
            else:
                parts.append(hundreds_n[h - 1])
    if t > 1:
        parts.append(tens[t - 1])
        if mod10 > 0:
            if f == True:
                parts.append(one_to_twenty_f[mod10 - 1])
            else:
                parts.append(one_to_twenty_n[mod10 - 1])
    elif t == 1:
        parts.append(one_to_twenty_n[10 + mod10 - 1])
    elif mod10 > 0:
        if f == True:
            parts.append(one_to_twenty_f[mod10 - 1])
        else:
            parts.append(one_to_twenty_n[mod10 - 1])
    return ' '.join(parts)

def num_to_text_thousands(number):
    th, r = divmod(number, 1000)
    if th > 1:
        return "{} {} {}".format(num_to_text_hundreds(th, True),
                                 thousands[1],
                                 num_to_text_hundreds(r, False))
    elif th == 1:
        return "{} {}".format(thousands[0], num_to_text_hundreds(r, False))
    else:
        return num_to_text_hundreds(r, False)

def num_to_text_millions(number):
    m, r = divmod(number, 1000000)
    if m > 1:
        return "{} {} {}".format(num_to_text_hundreds(m, False),
                              millions[1],
                              num_to_text_thousands(r))
    elif m == 1:
        return "{} {} {}".format(one_to_twenty_n[0],
                                 millions[0],
                                 num_to_text_thousands(r))
    else:
        return num_to_text_thousands(number)

def num_to_text_billions(number):
    m, r = divmod(number, 1000000000)
    if m > 1:
        return "{} {} {}".format(num_to_text_hundreds(m, False),
                                 billions[1],
                                 num_to_text_millions(r))
    elif m == 1:
        return "{} {} {}".format(one_to_twenty_n[0],
                                 billions[0],
                                 num_to_text_millions(r))
    else:
        return num_to_text_millions(number)
    
def num_to_text(number):
    return num_to_text_billions(number)


action = raw_input("Do you want to see previous invoices [P] or make a new one [N]? ")
if action == "P":
  with open("archive", "r") as f:
    f.seek (0, 2)           # Seek @ EOF
    fsize = f.tell()        # Get Size
    f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
    lines = f.readlines()       # Read to end

  tenLines = lines[-10:]    # Get last 10 lines

  for line in tenLines:
    print line
elif action == "N":
  
  with open("archive", "r") as f:
    f.seek (0, 2)           # Seek @ EOF
    fsize = f.tell()        # Get Size
    f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
    lines = f.readlines()       # Read to end

  max =0;
  for line in lines:
    number = line.split("\t")[0]
    if number > max:
      max = number

  print "Last invoice in archive is no {}. Creating invoice no {}...".format(str(max),str(int(max)+1))
  
  tree = ET.parse("invoice.xml")
  root = tree.getroot()

  num = int(max)+1
  theDate = datetime.now()
  date = str(theDate.day)+"/"+str(theDate.month)+"/"+str(theDate.year)
  date = raw_input("Input the date you want the invoice to have [DD/MM/YYYY] (hit enter if you want today's date): ")
  if date=="":
      date = str(theDate.day)+"/"+str(theDate.month)+"/"+str(theDate.year)
  stamp = root.find('stamp').text
  client = root.find('client').text
  occupation = root.find('occupation').text
  taxoffice = root.find('taxoffice').text
  address = root.find('address').text
  taxnumber = root.find('taxnumber').text
  description = root.find('description').text
  value_f_string = raw_input("Input the net amount (hit enter if you want the amount posed in the .xml file): ")
  if value_f_string=="": 
    value_f = float(root.find('value').text)
  else:
    value_f = float(value_f_string)
  tax_rate_el = root.find('tax_rate')
  
  
  
  print num 
  print date
  print client
  confirm = raw_input("Are the above correct? [Y/n]")
  if confirm == "Y" or confirm == "y":
    if tax_rate_el is not None:
      tax_rate = tax_rate_el.text
    else:
      tax_rate = "0.20" # default value
    tax_rate_f = float(tax_rate)
    tax_rate_prc = "{:.2f}".format(tax_rate_f * 100)
    if tax_rate_prc.endswith('.00'):
      tax_rate_prc = tax_rate_prc.replace('.00', '')
    vat_rate_el = root.find('vat_rate')
    if vat_rate_el is not None:
      vat_rate = vat_rate_el.text
    else:
      vat_rate = "0.23" # default value
    vat_rate_f = float(vat_rate)
    vat_rate_prc = "{:.2f}".format(vat_rate_f * 100)
    if vat_rate_prc.endswith('.00'):
      vat_rate_prc = vat_rate_prc.replace('.00', '')
    value = "{:.2f}".format(value_f)
    tax_f = value_f * tax_rate_f
    vat_element = root.find('vat')
    vat_f = value_f * vat_rate_f
    total_f = value_f + vat_f
    tax = "{:.2f}".format(tax_f)
    vat = "{:.2f}".format(vat_f)
    total = "{:.2f}".format(total_f) 
    (intpart, floatpart) = total.split('.')

    numbertext = "{} ευρώ".format(num_to_text(int(intpart)))

    if floatpart != '' :
      floatpart_i = int(floatpart)
      if floatpart_i > 0:
	  if(num_to_text(int(floatpart))==1):
	    numbertext = "{} και {} λεπτό".format(numbertext,
                                              num_to_text(int(floatpart)))
	  else:
	    numbertext = "{} και {} λεπτά".format(numbertext,
                                              num_to_text(int(floatpart)))

    outfn = 'invoice_' + str(num) + '.tex'
  
    with codecs.open('invoice.tex', mode='r', encoding='utf-8') as inf:
      with codecs.open(outfn, mode='w', encoding='utf-8') as outf:
	  for line in inf:
            line = line.replace("{{NUM}}", str(num))
            line = line.replace("{{DATE}}", date)
            line = line.replace("{{STAMP}}", stamp)
            line = line.replace("{{CLIENT}}", client)
            line = line.replace("{{OCCUPATION}}", occupation)
            line = line.replace("{{TAXOFFICE}}", taxoffice)
            line = line.replace("{{ADDRESS}}", address)
            line = line.replace("{{TAXNUMBER}}", taxnumber)
            line = line.replace("{{DESCRIPTION}}", description)
            line = line.replace("{{VALUE}}", value)
            line = line.replace("{{TAXRATE}}", tax_rate_prc)
            line = line.replace("{{TAX}}", tax)
            line = line.replace("{{VATRATE}}", vat_rate_prc)
            line = line.replace("{{VAT}}", vat)
            line = line.replace("{{TOTAL}}", total)
            line = line.replace("{{NUMBERTEXT}}",
                                numbertext.decode('utf-8').capitalize())
            outf.write(line)

    with open("archive", "a") as myfile:
      myfile.write(str(num)+"\t"+date+"\t"+value+"\n")
    call(["xelatex", outfn])
    call(["okular","invoice_"+str(num)+".pdf"])
  else:
    print "Update info in template invoice.xml"
else:
  print "Wrong answer."
  sys.exit(1)


