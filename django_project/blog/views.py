from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import TickerForm
import yfinance as yf
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter, Bar, Marker


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
    sec_divs = ""
    sec_isin = ""
    sec_descript = ""
    sec_title = ""
    sec_market_cap = ""
    sec_price_to_earnings = ""
    sec_profit_margins = ""
    sec_sector = ""
    sec_country = ""
    sec_employees = ""
    sec_website = ""
    sec_phone = ""

    form = TickerForm(request.POST or None)
    if form.is_valid():
        search_ticker = str(form.cleaned_data['ticker'])
        # form.save()

        sec = yf.Ticker(search_ticker)

        sec_info = sec.get_info()
        sec_isin = sec.get_isin()

        sec_descript = sec_info['longBusinessSummary']
        sec_title = sec_info['longName']
        sec_market_cap = sec_info['marketCap']
        sec_price_to_earnings = sec_info['pegRatio']
        sec_profit_margins = sec_info['profitMargins']
        sec_sector = sec_info['sector']
        sec_country = sec_info['country']
        sec_employees = sec_info['fullTimeEmployees']
        sec_website = sec_info['website']
        sec_phone = sec_info['phone']

        sec_profit_margins = "{:.0%}".format(sec_profit_margins)
        sec_market_cap = "$" + f'{sec_market_cap:,}'

        sec_info = sec.history(period='max').reset_index()
        x_data = sec_info['Date']
        y_data = sec_info['Close']
        dividends = pd.DataFrame(sec.actions)
        x_div = dividends.index
        y_div = dividends['Dividends']

        sec_divs = plot([Scatter(x=x_div, y=y_div, name='divs',
                                 opacity=0.8, marker_color='blue')],
                        output_type='div')

        sec_graph = plot([Scatter(x=x_data, y=y_data, name='test',
                                  opacity=0.8, marker_color='green')],
                         output_type='div')
        form = TickerForm()

    context = {
        'form': form,
        'sec_graph': sec_graph,
        'sec_divs': sec_divs,
        'search_ticker': search_ticker,
        'sec_isin': sec_isin,
        'sec_descript': sec_descript,
        'sec_title': sec_title,
        'sec_market_cap': sec_market_cap,
        'sec_price_to_earnings': sec_price_to_earnings,
        'sec_profit_margins': sec_profit_margins,
        'sec_sector': sec_sector,
        'sec_country': sec_country,
        'sec_employees': sec_employees,
        'sec_website': sec_website,
        'sec_phone': sec_phone,
        'post': Post.objects.all(),

    }

    return render(request, "blog/security.html", context)

def economic(request):
    context = {

    }
    return render(request, "blog/economy.html", context)

# LoginRequiredMixin
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # naming convention: <app>/<model>_<viewtype.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # naming convention: <app>/<model>_<viewtype.html
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
