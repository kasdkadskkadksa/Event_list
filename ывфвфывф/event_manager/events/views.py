from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Event, Participant
from .forms import EventForm, ParticipantForm


def event_list(request):
    events = Event.objects.annotate(participant_count=Count('participant'))

    # Фильтрация
    status = request.GET.get('status')
    search = request.GET.get('search')
    if status:
        events = events.filter(status=status)
    if search:
        events = events.filter(title__icontains=search)

    # Сортировка
    order_by = request.GET.get('order_by', '-start_date')
    events = events.order_by(order_by)

    # Пагинация
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Статистика по статусам
    status_stats = Event.objects.values('status').annotate(count=Count('id'))

    return render(request, 'events/event_list.html', {
        'page_obj': page_obj,
        'status_stats': status_stats,
    })


def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})


def register_participant(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.event = event
            participant.save()
            return redirect('event_detail', pk=event_id)
    else:
        form = ParticipantForm()
    return render(request, 'events/participant_form.html', {'form': form, 'event': event})


def manage_participants(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participants = Participant.objects.filter(event=event).select_related('event')

    if request.method == 'POST':
        participant_id = request.POST.get('participant_id')
        participant = get_object_or_404(Participant, pk=participant_id)
        participant.delete()

    return render(request, 'events/manage_participants.html', {
        'event': event,
        'participants': participants,
    })