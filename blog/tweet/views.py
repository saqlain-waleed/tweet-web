from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q


def index(request):
    return render(request, 'index.html')

# List tweets
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

# Create tweet
@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweetform.html', {'form': form})

# Edit tweet
@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweetform.html', {'form': form})

# Delete tweet
@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_conform_delete.html', {'tweet': tweet})

# Register user
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

#search text 
def search(request):
    searched = None  # Initialize to avoid unbound variable errors
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Perform the search query
            # search_instance = search(query=query, user=request.user if request.user.is_authenticated else None)
            # search_instance.save() 
            searched = Tweet.objects.filter(
                Q(text__icontains=query) | Q(user__username__icontains=query)
            )  # Modify based on your model (e.g., username field)
            # Save the search term into the Search model
    else:
        form = SearchForm()

    return render(request, 'search_results.html', {'form': form, 'searched': searched})

