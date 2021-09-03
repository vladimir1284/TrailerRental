from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from .models import Trailer, TrailerPicture, Maintenance, Contact, Lessee, Lease, LeaseStage
from .forms import TrailerForm, MaintenanceForm, ContactForm, LesseeForm, LeaseForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.core.mail import EmailMessage

@login_required
def contact_detail(request, id):
    contact = Contact.objects.get(id=id)
    return render(request, 'towit/client/contact.html', {'contact': contact})

@login_required
def capture_signature(request, lease_id, position):
    return render(request, 'towit/contract/signature.html', {'lease_id': lease_id,
                                                             'position': position})

@login_required
def contract_detail(request, id):
    contract = Lease.objects.get(id=id)
    return render(request, 'towit/contract/contract_detail.html', {'contract': contract})

@login_required
def dashboard(request):
    contacts = Contact.objects.all().order_by("-interest_date")[:5]
    maintenances = Maintenance.objects.all().order_by("-date")[:5]
    contracts = Lease.objects.all().order_by("contract_end_date")[:5]
    trailers = Trailer.objects.all()
    return render(request, 'towit/dashboard.html', {'contacts': contacts,
                                                    'maintenances': maintenances,
                                                    'trailers': trailers,
                                                    'contracts': contracts})
    
@login_required
def trailers(request):
    trailers = Trailer.objects.all()
    return render(request, 'towit/trailer/trailers.html', {'trailers': trailers})

@login_required
def contacts(request):
    contacts = Contact.objects.all()
    return render(request, 'towit/client/contacts.html', {'contacts': contacts})

@login_required
def contracts(request):
    contracts = Lease.objects.all()
    return render(request, 'towit/contract/contracts.html', {'contracts': contracts})

@login_required
def maintenances(request, trailer_id):
    trailer = Trailer.objects.get(id = trailer_id)
    maintenances = Maintenance.objects.filter(trailer = trailer)
    return render(request, 'towit/trailer/maintenances.html', {'maintenances': maintenances,
                                                              'trailer': trailer})

@login_required
def delete_trailer_image(request, id):
    img = TrailerPicture.objects.get(id=id)
    img.delete()
    return redirect('/towit/trailer/' + str(img.trailer.id))

@login_required
def change_contract_stage(request, id, stage):
    lease = Lease.objects.get(id=id)
    lease.stage = LeaseStage.objects.get(id=stage)
    lease.save()
    if (stage == 2):
        # Send a copy by mail
        return generate_pdf(request, id)
    else:
        return redirect('/towit/contract/' + str(lease.id))


def generate_pdf(request, id):
    contract = Lease.objects.get(id=id)

    """Generate pdf."""
    # Rendered
    html_string = render_to_string('towit/contract/contract_pdf.html', {'contract': contract})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=contract_for_signature.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
        # Send email
        output.seek(0)
        send_contract(id, output.read())

    return response

def send_contract(id, pdf_data):
    lease = Lease.objects.get(id = id)
    body = """
            Dear %s, find attached the contract ready for signature.
            """ % (lease.lessee.name)
    email = EmailMessage(
            'Contract ready for signature',
            body,
            'trailerrentalweb@gmail.com',
            ['vladimir.rdguez@gmail.com', 
             'towithouston@gmail.com',
             lease.lessee.mail],
            reply_to=['trailerrentalweb@gmail.com'],
            headers={'Message-ID': 'TOWIT'},
        )
    email.attach('contract_for_signature.pdf', pdf_data, 'application/pdf')
    email.send()
    
@login_required
def delete_trailer(request, id):
    try:
        trailer = Trailer.objects.get(id=id)
        trailer.delete()
    except:
        pass
    return redirect('/towit/trailers/')

@login_required
def delete_contract(request, id):
    try:
        contract = Lease.objects.get(id=id)
        contract.delete()
    except:
        pass
    return redirect('/towit/contracts/')

@login_required
def trailer_json(request, id):
    trailer = Trailer.objects.get(id=id)    
    return JsonResponse({'type': trailer.type.name, 
                         'size': trailer.size,
                         'id': trailer.id,
                         'current_tires_condition': trailer.get_current_tires_condition_display(),
                         'number_of_axles': trailer.get_number_of_axles_display(), 
                         'bed_type': trailer.get_bed_type_display(), 
                         'bed_comments': trailer.bed_comments, 
                         'has_spare_tire': trailer.get_has_spare_tire_display(), 
                         'number_of_ramps': trailer.number_of_ramps, 
                         'ramps_material': trailer.get_ramps_material_display(), 
                         'ramps_length': trailer.get_ramps_length_display(), 
                         'electrical_instalation': trailer.electrical_instalation})

@login_required
def trailer_detail(request, id):
    trailer = Trailer.objects.get(id=id)
    print(Maintenance.objects.filter(trailer=trailer).order_by("-date"))
    try:
        mtn = Maintenance.objects.filter(trailer=trailer).order_by("-date")[0]
    except:
        mtn = ""
    images = TrailerPicture.objects.filter(trailer = trailer)[:]
    tax = int(trailer.tax_price*0.06)
    return render(request, 'towit/trailer/trailer.html', {'trailer': trailer,
                                                          'images': images,
                                                          'tax': tax,
                                                          'maintenance': mtn})

class MaintenanceCreateView(LoginRequiredMixin,CreateView):
    model = Maintenance
    form_class = MaintenanceForm    
    template_name = 'towit/trailer/new_maintenance.html' 
    
    def form_valid(self, form):
        form.instance.trailer = Trailer.objects.get(id=self.kwargs['trailer_id'])
        return super(MaintenanceCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(MaintenanceCreateView, self).get_context_data(**kwargs)
        context['trailer_id'] = self.kwargs['trailer_id']
        return context
    
class MaintenanceUpdateView(LoginRequiredMixin,UpdateView):
    model = Maintenance
    form_class = MaintenanceForm    
    template_name = 'towit/trailer/new_maintenance.html' 
    
    def form_valid(self, form):
        form.instance.trailer = Maintenance.objects.get(id=self.kwargs['pk']).trailer
        print(form.instance)
        return super(MaintenanceUpdateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(MaintenanceUpdateView, self).get_context_data(**kwargs)
        context['trailer_id'] = Maintenance.objects.get(id=self.kwargs['pk']).trailer.id
        return context
    
class TrailerCreateView(LoginRequiredMixin,CreateView):
    model = Trailer
    form_class = TrailerForm    
    template_name = 'towit/trailer/new_trailer.html' 
    
    def post(self, request, * args, ** kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('pictures')
        if form.is_valid():            
            trailer = form.save()
            for f in files:
                pic = TrailerPicture(trailer = trailer, image = f)
                pic.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class TrailerUpdateView(LoginRequiredMixin,UpdateView):
    model = Trailer
    form_class = TrailerForm    
    template_name = 'towit/trailer/update_trailer.html' 
    
    def post(self, request, * args, ** kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('pictures')
        if form.is_valid():          
            self.object = self.get_object()
            for f in files:
                pic = TrailerPicture(trailer = self.object, image = f)
                pic.save()
            return super(TrailerUpdateView, self).post(request, **kwargs)
        else:
            return self.form_invalid(form)
    
class ContactCreateView(LoginRequiredMixin,CreateView):
    model = Contact
    form_class = ContactForm    
    template_name = 'towit/client/new_contact.html' 
    
class ContactUpdateView(LoginRequiredMixin,UpdateView):
    model = Contact
    form_class = ContactForm    
    template_name = 'towit/client/update_contact.html' 

class LesseeCreateView(LoginRequiredMixin,CreateView):
    model = Lessee
    form_class = LesseeForm    
    template_name = 'towit/client/new_lessee.html' 
    
    def get_initial(self):
        try:
            # If the trailer to be rented is known it is saved in the session
            self.request.session['trailer_id'] = self.kwargs['trailer_id']
        except:
            pass
        try:
            contact = Contact.objects.get(id = self.kwargs['contact_id'])
            print(contact)
            return {
                'name':contact.name,
                'mail':contact.mail,
                'phone':contact.phone,
                'address':contact.address
            }
        except:
            return super(LesseeCreateView, self).get_initial()

    
class LeaseCreateView(LoginRequiredMixin,CreateView):
    model = Lease
    form_class = LeaseForm    
    template_name = 'towit/contract/new_contract.html' 
    
    def get_initial(self):
        default_init = super(LeaseCreateView, self).get_initial()
        try:
            # If the trailer to be rented is known it is selected as initial value
            default_init.setdefault('trailer',self.request.session['trailer_id'])
        except:
            pass
        try:
            # Init the lessee in the contract
            default_init.setdefault('lessee',self.kwargs['lessee_id'])
        except:
            pass
        return default_init      
    
    def form_valid(self, form):
        form.instance.stage = LeaseStage.objects.get(id=1)
        # Clear the trailer to be rented from the session
        self.request.session.pop('trailer_id', 0)
        return super(LeaseCreateView, self).form_valid(form) 
    
class ContractUpdateView(LoginRequiredMixin,UpdateView):
    model = Lease
    form_class = LeaseForm    
    template_name = 'towit/contract/update_contract.html' 
        
