from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .forms import TickerForm
import yfinance as yf
from plotly.offline import plot
from plotly.graph_objs import Scatter

# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Home'
    }
    return render(request, 'blog/home.html', context)

def contact(request):
    context = {
    }
    return render(request, 'blog/contact_me.html', context)


def security(request):
    sec_graph = ""
    search_ticker = ""
    form = TickerForm(request.POST or None)
    if form.is_valid():
        search_ticker = str(form.cleaned_data['ticker'])
        #form.save()
        sec = yf.Ticker(search_ticker)
        sec_info = sec.history(period='max').reset_index()
        x_data = sec_info['Date']
        y_data = sec_info['Close']
        sec_graph = plot([Scatter(x=x_data, y=y_data, name='test',
                                 opacity=0.8, marker_color='green')],
                        output_type='div')
        form = TickerForm()

    context = {
        'form': form,
        'sec_graph': sec_graph,
        'search_ticker': search_ticker,
    }
    return render(request, "blog/security.html", context)

#LoginRequiredMixin
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #naming convention: <app>/<model>_<viewtype.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' #naming convention: <app>/<model>_<viewtype.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    context = {
        'title': 'Blog About Page',
    }
    return render(request, 'blog/about.html', context)

