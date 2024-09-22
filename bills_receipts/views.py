from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentForm, DocumentFilterForm

@login_required
def document_list(request):
    documents = Document.objects.filter(user=request.user)

    # Apply filters
    if request.GET.get('title'):
        documents = documents.filter(title__icontains=request.GET['title'])
    if request.GET.get('date'):
        documents = documents.filter(date=request.GET['date'])
    if request.GET.get('bill_number'):
        documents = documents.filter(bill_number__icontains=request.GET['bill_number'])

    form = DocumentFilterForm(request.GET or None)
    return render(request, 'bills_receipts/document_list.html', {'documents': documents, 'form': form})

@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'bills_receipts/document_form.html', {'form': form})

@login_required
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'bills_receipts/document_form.html', {'form': form})

@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        document.delete()
        return redirect('document_list')
    return render(request, 'bills_receipts/document_confirm_delete.html', {'document': document})
