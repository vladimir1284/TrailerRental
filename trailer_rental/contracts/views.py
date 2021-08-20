from django.shortcuts import render
from . import forms
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import ast

def generate_pdf(request):
    #Check to see if we are getting a POST request back
    if request.method == "POST":
        data = ast.literal_eval(request.POST['form'])
        print(type(data))

    """Generate pdf."""
    # Rendered
    html_string = render_to_string('contracts/Contract_Template.html', data)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response

# Create your views here.
def index(request):
    return render(request, 'contracts/index.html')

def newContract(request):
    form = forms.FormContract()
    #Check to see if we are getting a POST request back
    if request.method == "POST":
        # if post method = True
        form = forms.FormContract(request.POST)
        # Then we check to see if the form is valid (this is an automatic  validation by Django)
        if form.is_valid():
            data = {'Effective_date' : form.cleaned_data['effective_date'].date().strftime("%B %d, %Y"),
                    'Lessee_name' : form.cleaned_data['lessee_name'],
                    'Lessee_address' : form.cleaned_data['lessee_address'],
                    'Lessee_email' : form.cleaned_data['lessee_mail'],
                    'Number_of_payments' : form.cleaned_data['number_of_payments'],
                    'Payment_amount' : form.cleaned_data['payment_amount'],
                    'Service_charge' : form.cleaned_data['service_charge'],
                    'Security_deposit' : form.cleaned_data['security_deposit'],
                    'Contract_end_date' : form.cleaned_data['contract_end_date'].date().strftime("%B %d, %Y"),
                    'Location' : form.cleaned_data['location'],
                    'Model' : form.cleaned_data['model'],
                    'VIN' : form.cleaned_data['vin']
                    }
            return render(request, 'contracts/Contract_Review.html', 
                    {'Effective_date' : form.cleaned_data['effective_date'].date().strftime("%B %d, %Y"),
                    'Lessee_name' : form.cleaned_data['lessee_name'],
                    'Lessee_address' : form.cleaned_data['lessee_address'],
                    'Lessee_email' : form.cleaned_data['lessee_mail'],
                    'Number_of_payments' : form.cleaned_data['number_of_payments'],
                    'Payment_amount' : form.cleaned_data['payment_amount'],
                    'Service_charge' : form.cleaned_data['service_charge'],
                    'Security_deposit' : form.cleaned_data['security_deposit'],
                    'Contract_end_date' : form.cleaned_data['contract_end_date'].date().strftime("%B %d, %Y"),
                    'Location' : form.cleaned_data['location'],
                    'Model' : form.cleaned_data['model'],
                    'VIN' : form.cleaned_data['vin'],
                    'data': data
                    })

    return render(request, 'contracts/contract_form.html', {'form': form})