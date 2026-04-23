"""
Views for patients app.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


def patient_list(request):
    """Patient list view."""
    context = {
        'title': 'Patients - OpenCare-Africa',
    }
    return render(request, 'patients/patient_list.html', context)


@login_required
def patient_detail(request, pk):
    """Patient detail view."""
    context = {
        'title': 'Patient Details - OpenCare-Africa',
        'patient_id': pk,
    }
    return render(request, 'patients/patient_detail.html', context)


@login_required
def patient_create(request):
    """Create new patient view."""
    context = {
        'title': 'Add New Patient - OpenCare-Africa',
    }
    return render(request, 'patients/patient_create.html', context)


@login_required
def patient_edit(request, pk):
    """Edit patient view."""
    context = {
        'title': 'Edit Patient - OpenCare-Africa',
        'patient_id': pk,
    }
    return render(request, 'patients/patient_edit.html', context)


def visit_list(request):
    """Patient visit list view."""
    context = {
        'title': 'Patient Visits - OpenCare-Africa',
    }
    return render(request, 'patients/visit_list.html', context)


@login_required
def visit_detail(request, pk):
    """Patient visit detail view."""
    context = {
        'title': 'Visit Details - OpenCare-Africa',
        'visit_id': pk,
    }
    return render(request, 'patients/visit_detail.html', context)


@login_required
def visit_create(request):
    """Create new visit view."""
    context = {
        'title': 'New Visit - OpenCare-Africa',
    }
    return render(request, 'patients/visit_create.html', context)


@require_http_methods(["GET"])
def patient_search(request):
    """Patient search endpoint."""
    query = request.GET.get('q', '')
    return JsonResponse({
        'message': 'Patient search endpoint',
        'query': query,
        'results': []
    })


@require_http_methods(["GET"])
def patient_stats(request):
    """Patient statistics endpoint."""
    return JsonResponse({
        'total_patients': 0,
        'active_patients': 0,
        'new_patients_this_month': 0,
        'visits_today': 0
    })


@login_required
def patient_delete(request, pk):
    """Delete patient view."""
    context = {
        'title': 'Delete Patient - OpenCare-Africa',
        'patient_id': pk,
    }
    return render(request, 'patients/patient_delete.html', context)


def advanced_search(request):
    """Advanced patient search view."""
    context = {
        'title': 'Advanced Search - OpenCare-Africa',
    }
    return render(request, 'patients/advanced_search.html', context)


@login_required
def patient_visits(request, patient_pk):
    """Patient visits list view."""
    context = {
        'title': 'Patient Visits - OpenCare-Africa',
        'patient_id': patient_pk,
    }
    return render(request, 'patients/patient_visits.html', context)


@login_required
def visit_edit(request, pk):
    """Edit visit view."""
    context = {
        'title': 'Edit Visit - OpenCare-Africa',
        'visit_id': pk,
    }
    return render(request, 'patients/visit_edit.html', context)


@login_required
def visit_delete(request, pk):
    """Delete visit view."""
    context = {
        'title': 'Delete Visit - OpenCare-Africa',
        'visit_id': pk,
    }
    return render(request, 'patients/visit_delete.html', context)


@login_required
def medical_history(request, patient_pk):
    """Patient medical history view."""
    context = {
        'title': 'Medical History - OpenCare-Africa',
        'patient_id': patient_pk,
    }
    return render(request, 'patients/medical_history.html', context)


@login_required
def medical_history_create(request, patient_pk):
    """Create medical history view."""
    context = {
        'title': 'Add Medical History - OpenCare-Africa',
        'patient_id': patient_pk,
    }
    return render(request, 'patients/medical_history_create.html', context)


@login_required
def medical_history_detail(request, pk):
    """Medical history detail view."""
    context = {
        'title': 'Medical History Details - OpenCare-Africa',
        'history_id': pk,
    }
    return render(request, 'patients/medical_history_detail.html', context)


@login_required
def medical_history_edit(request, pk):
    """Edit medical history view."""
    context = {
        'title': 'Edit Medical History - OpenCare-Africa',
        'history_id': pk,
    }
    return render(request, 'patients/medical_history_edit.html', context)


@login_required
def medical_history_delete(request, pk):
    """Delete medical history view."""
    context = {
        'title': 'Delete Medical History - OpenCare-Africa',
        'history_id': pk,
    }
    return render(request, 'patients/medical_history_delete.html', context)


@login_required
def patient_statistics(request):
    """Patient statistics view."""
    context = {
        'title': 'Patient Statistics - OpenCare-Africa',
    }
    return render(request, 'patients/patient_statistics.html', context)


@login_required
def patient_reports(request):
    """Patient reports view."""
    context = {
        'title': 'Patient Reports - OpenCare-Africa',
    }
    return render(request, 'patients/patient_reports.html', context)


@login_required
def export_patients(request):
    """Export patients view."""
    context = {
        'title': 'Export Patients - OpenCare-Africa',
    }
    return render(request, 'patients/export_patients.html', context)


@login_required
def bulk_import(request):
    """Bulk import patients view."""
    context = {
        'title': 'Bulk Import Patients - OpenCare-Africa',
    }
    return render(request, 'patients/bulk_import.html', context)


@login_required
def bulk_export(request):
    """Bulk export patients view."""
    context = {
        'title': 'Bulk Export Patients - OpenCare-Africa',
    }
    return render(request, 'patients/bulk_export.html', context)


@login_required
def patient_dashboard(request, pk):
    """Patient dashboard view."""
    context = {
        'title': 'Patient Dashboard - OpenCare-Africa',
        'patient_id': pk,
    }
    return render(request, 'patients/patient_dashboard.html', context)


@login_required
def patient_timeline(request, pk):
    """Patient timeline view."""
    context = {
        'title': 'Patient Timeline - OpenCare-Africa',
        'patient_id': pk,
    }
    return render(request, 'patients/patient_timeline.html', context)
