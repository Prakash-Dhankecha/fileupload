from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadedFileForm
import pandas as pd

# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)
            summary = generate_summary(df)
            form.save()
            return render(request, 'fileupload/summary.html', {'summary': summary})
    else:
        form = UploadedFileForm()
    return render(request, 'fileupload/upload.html', {'form': form})

def generate_summary(df):
    df.columns = [column.lower().replace(' ', '_') for column in df.columns]
    summary = df.groupby(['cust_state', 'dpd']).size().reset_index(name='Count')
    return summary