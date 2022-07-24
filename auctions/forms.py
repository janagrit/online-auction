from django import forms
from .models import Category, Listing


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'starting_bid', 'category', 'status', 'imageURL')
        widgets = {'category': forms.Select(choices=Listing.objects.all(), attrs={'class': 'form-control'}),
                   'status': forms.Select(choices=Category.objects.all(), attrs={'class': 'form-control'}),
                   'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                   'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add Description'}),
                   'imageURL': forms.URLInput(attrs={'class': 'form-control', 'placeholder': "Image URL (optional)"}),
                   'starting_bid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Add the price '})
                   }


class BidForm(forms.Form):

    value = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bid'}))
    item_id = forms.IntegerField(widget=forms.HiddenInput())




class CommentForm(forms.Form):
    comment = forms.CharField(
        label="Comment",
        widget=forms.Textarea(attrs={'class': 'form-control'}))
    item_id = forms.IntegerField(widget=forms.HiddenInput())
