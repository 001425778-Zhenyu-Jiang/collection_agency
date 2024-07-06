import csv
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Account

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'error': 'File is not CSV type'}, status=400)
        
        file_data = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(file_data)
        
        for row in reader:
            Account.objects.create(
                client_reference_no=row['client reference no'],
                balance=row['balance'],
                status=row['status'],
                consumer_name=row['consumer name'],
                consumer_address=row['consumer address'],
                ssn=row['ssn']
            )
        
        return JsonResponse({'message': 'CSV file uploaded successfully'})
    return JsonResponse({'error': 'Invalid method'}, status=405)

def index(request):
    return render(request, 'accounts/index.html')

def get_accounts(request):
    min_balance = request.GET.get('min_balance')
    max_balance = request.GET.get('max_balance')
    consumer_name = request.GET.get('consumer_name')
    status = request.GET.get('status')
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)

    accounts = Account.objects.all()

    if min_balance:
        accounts = accounts.filter(balance__gte=min_balance)
    if max_balance:
        accounts = accounts.filter(balance__lte=max_balance)
    if consumer_name:
        accounts = accounts.filter(consumer_name__icontains=consumer_name)
    if status:
        accounts = accounts.filter(status__iexact=status)

    paginator = Paginator(accounts, per_page)

    try:
        accounts_page = paginator.page(page)
    except PageNotAnInteger:
        accounts_page = paginator.page(1)
    except EmptyPage:
        accounts_page = paginator.page(paginator.num_pages)

    data = list(accounts_page.object_list.values())
    response = {
        'data': data,
        'pagination': {
            'current_page': accounts_page.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_next': accounts_page.has_next(),
            'has_previous': accounts_page.has_previous(),
        }
    }
    return JsonResponse(response, safe=False)
