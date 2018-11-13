

import io
import pdfminer
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import pandas as pd
import re
import sqlite3
import glob


# In[4]:

# data dictionary to hold output resaults 
data = [] 

# Class Person to intiate our objects
class Person:
    def __init__(self, first_name="", last_name="", middle_name="", report_date="", dl_number=""):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.report_date = report_date
        self.dl_number = dl_number
      

    
    
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "dL_number": self.dl_number,
            "report_date":self.report_date
        }

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
 
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
 
            text = fake_file_handle.getvalue()
 
    # close open handles
    converter.close()
    fake_file_handle.close()
 
    if text:
        return text
if __name__ == '__main__':
 
# for loop using glob function to read all .pdf files within givin path, then extrct text only. 
 for name in glob.glob('C:\\Users\aliyahi\\*.pdf'):     
    text = extract_text_from_pdf(name)
    # print name of ll .pdf files in your folder
    print(name)
    

   
    person = Person() 

    # example of defined patterns to lookup and extract specific information we are  need from the .pdf file.
    try:     
        first_name_pattern = 'First [nN]ame[A-z -\']+Middle name'
        for match in re.findall(first_name_pattern, text):
            first_name = '{!r}'.format(match)
            first_name = first_name[11:-12].strip().upper()
            person.first_name = first_name

        middle_name_pattern = 'Middle [nN]ame[A-z -\']+Last name'
        for match in re.findall(middle_name_pattern, text):
            middle_name = '{!r}'.format(match)
            middle_name = middle_name[12:-10].strip().upper()
            person.middle_name = middle_name  

        last_name_pattern = 'Last [nN]ame[A-z -\']+Date of' 
        for match in re.findall(last_name_pattern, text):
            last_name = '{!r}'.format(match)
            last_name = last_name[10:-8].strip().upper()
            person.last_name = last_name

        dl_number_pattern = 'Driver [lL]icense[A-z-\0-9-\*]+Previous'
        for match in re.findall(dl_number_pattern, text):
            dl_number = '{!r}'.format(match)
            dl_number = dl_number[16:-9].strip().upper()
            person.dl_number = dl_number

        report_date_pattern = 'Report completed on[Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec,\d{1,2}+, \d{4}+ \d+:\d+,PM|AM]+Consumer'
        for match in re.findall(report_date_pattern, text):
            report_date = '{!r}'.format(match)
            report_date = report_date[20:-17].strip().upper()
            person.report_date = report_date

        data.append(person)
    
    except Exception as ex:
        print(ex,type(ex))


    

for person in data:
        print(person.first_name)    
        print(person.last_name)
        print(person.middle_name)
        print(person.dl_number)
        print(person.report_date)
        
        
          
# convert Lst to data frame using Pandas         
df = pd.DataFrame([d.to_dict() for d in data])

# Write to Excel and CSV file formats
df.to_excel("myApplicant.xlsx", index=False)
df.to_csv("myApplicant.csv", index=False)


# Write Sqlite DB file
df.to_sql("myApplicant", sqlite3.connect("applicant.db"))
   






