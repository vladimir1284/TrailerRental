import jinja2
from datetime import datetime

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "Contract Template.html"
template = templateEnv.get_template(TEMPLATE_FILE)


outputText = template.render(Effective_date = datetime.now().date().strftime("%B %d, %Y"),
			      Lessee_name = "Vladímir Rodríguez Diez",
			      Lessee_address = "San Ramón 233",
			      Number_of_payments = 1,
			      Payment_amount = 2000,
			      Service_charge = 50,
			      Security_deposit = 600,
			      Contract_end_date = datetime(year=2022,month=8,day=4).date().strftime("%B %d, %Y"),
			      Location = "Somewhere",
			      Model = "Brand New",
			      VIN = "234RDT456L56",
			      Lessee_email = "vladimir.rdguez@gmail.com")
			      
html_file = open('vladimir.html', 'w')
html_file.write(outputText)
html_file.close()
