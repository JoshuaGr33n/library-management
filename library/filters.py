import django_filters
from .models import Book, Loan

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    availability = django_filters.BooleanFilter()

    class Meta:
        model = Book
        fields = ['title', 'author', 'availability']
        

class LoanFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name='user__id')
    book = django_filters.NumberFilter(field_name='book__id')
    borrowed_date_after = django_filters.DateTimeFilter(field_name='borrowed_date', lookup_expr='gte')
    borrowed_date_before = django_filters.DateTimeFilter(field_name='borrowed_date', lookup_expr='lte')
    returned_date = django_filters.DateFromToRangeFilter(field_name='returned_date')
    is_active = django_filters.BooleanFilter(method='filter_active_loans')

    class Meta:
        model = Loan
        fields = ['user', 'book', 'borrowed_date_after', 'borrowed_date_before', 'returned_date', 'is_active'] 
    
    def filter_active_loans(self, queryset, name, value):
        if value:
            return queryset.filter(returned_date__isnull=True)
        return queryset.filter(returned_date__isnull=False)           