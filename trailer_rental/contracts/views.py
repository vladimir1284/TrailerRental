from django.shortcuts import render
from . import forms
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import ast
from .models import Contract

def generate_pdf(request):
    #Check to see if we are getting a POST request back
    if request.method == "POST":
        # data = ast.literal_eval(request.POST['form'])
        # print(type(data))
        # Get data from previous view
        data_id = int(request.POST['form'])
        data = Contract.objects.get(id=data_id)
        data.accepted = True
        data.save()
        # Clean unacepted contracts
        Contract.objects.all().filter(accepted=False).delete()

        """Generate pdf."""
        # Rendered
        html_string = render_to_string('contracts/Contract_Template.html', 
                    {'Effective_date' : data.effective_date.date().strftime("%B %d, %Y"),
                    'Lessee_name' : data.lessee_name,
                    'Lessee_address' : data.lessee_address,
                    'Lessee_email' : data.lessee_mail,
                    'Number_of_payments' : data.number_of_payments,
                    'Payment_amount' : data.payment_amount,
                    'Service_charge' : data.service_charge,
                    'Security_deposit' : data.security_deposit,
                    'Contract_end_date' : data.contract_end_date.date().strftime("%B %d, %Y"),
                    'Location' : data.location,
                    'Model' : data.model,
                    'VIN' : data.vin})
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
            instance = Contract(**form.cleaned_data)
            instance.save()
            return render(request, 'contracts/Contract_Review.html', 
                    {'Effective_date' : instance.effective_date.date().strftime("%B %d, %Y"),
                    'Lessee_name' : instance.lessee_name,
                    'Lessee_address' : instance.lessee_address,
                    'Lessee_email' : instance.lessee_mail,
                    'Number_of_payments' : instance.number_of_payments,
                    'Payment_amount' : instance.payment_amount,
                    'Service_charge' : instance.service_charge,
                    'Security_deposit' : instance.security_deposit,
                    'Contract_end_date' : instance.contract_end_date.date().strftime("%B %d, %Y"),
                    'Location' : instance.location,
                    'Model' : instance.model,
                    'VIN' : instance.vin,
                    'data': instance.id
                    })

    return render(request, 'contracts/contract_form.html', {'form': form})