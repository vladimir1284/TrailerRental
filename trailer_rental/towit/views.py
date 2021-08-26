from django.shortcuts import render
from django.http import Http404

from django.views.generic import CreateView
from .models import Trailer, TrailerPicture
from .forms import TrailerForm

def trailers(request):
    trailers = Trailer.objects.all()
    return render(request, 'towit/trailer/trailers.html', {'trailers': trailers})

def trailer_detail(request, id):
    trailer = Trailer.objects.get(id=id)
    return render(request, 'towit/trailer/trailer.html', {'trailer': trailer})

class TrailerCreateView(CreateView):
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
    

