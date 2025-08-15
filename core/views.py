from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import News, ContactInquiry, GetInvolvedInquiry, ConsultationBooking, NewsletterSubscription
from .forms import ContactForm, GetInvolvedForm, ConsultationForm, NewsletterForm

def home(request):
    if request.method == 'POST' and 'consultation_submit' in request.POST:
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ConsultationForm()
    latest_news = News.objects.all().order_by('-date')[:3]
    return render(request, 'index.html', {
        'consultation_form': form,
        'latest_news': latest_news
    })

def about(request):
    return render(request, 'about.html')

def services(request):
    if request.method == 'POST' and 'consultation_submit' in request.POST:
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form = ConsultationForm()
    return render(request, 'services.html', {'consultation_form': form})

def impact(request):
    return render(request, 'impact.html')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_us')
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'contact_form': form})

def get_involved(request):
    if request.method == 'POST':
        form = GetInvolvedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('get_involved')
    else:
        form = GetInvolvedForm()
    return render(request, 'get_involved.html', {'get_involved_form': form})

class NewsListView(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = News.objects.all().order_by('-date')
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        if category and category != 'all_news':
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = News.CATEGORY_CHOICES
        context['newsletter_form'] = NewsletterForm()
        return context

    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_list')
        return self.get(request, *args, **kwargs)

class NewsDetailView(DetailView):
    model = News
    template_name = 'news_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_news'] = News.objects.filter(category=self.object.category).exclude(id=self.object.id)[:3]
        context['newsletter_form'] = NewsletterForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_detail', slug=self.object.slug)
        context = self.get_context_data()
        context['newsletter_form'] = form
        return self.render_to_response(context)