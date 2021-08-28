from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from .models import Trailer, TrailerPicture, maintenance
from .forms import TrailerForm, maintenanceForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def trailers(request):
    trailers = Trailer.objects.all()
    return render(request, 'towit/trailer/trailers.html', {'trailers': trailers})

@login_required
def delete_trailer_image(request, id):
    img = TrailerPicture.objects.get(id=id)
    img.delete()
    return redirect('/towit/trailer/' + str(img.trailer.id))

@login_required
def trailer_detail(request, id):
    trailer = Trailer.objects.get(id=id)
    images = TrailerPicture.objects.filter(trailer = trailer)[:]
    tax = int(trailer.tax_price*0.06)
    return render(request, 'towit/trailer/trailer.html', {'trailer': trailer,
                                                          'images': images,
                                                          'tax': tax})

class MaintenanceCreateView(LoginRequiredMixin,CreateView):
    model = maintenance
    form_class = maintenanceForm    
    template_name = 'towit/trailer/new_maintenance.html' 
    
    def form_valid(self, form):
        form.instance.trailer = Trailer.objects.get(id=self.kwargs['trailer_id'])
        print(form.instance)
        context = {'trailer_id':self.kwargs['trailer_id']}
        return super(MaintenanceCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(MaintenanceCreateView, self).get_context_data(**kwargs)
        context['trailer_id'] = self.kwargs['trailer_id']
        return context
    
    # def post(self, request, * args, ** kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     if form.is_valid():        
    #         print(form)    
    #         form.
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    
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
    template_name = 'towit/trailer/new_trailer.html' 
    
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
    

