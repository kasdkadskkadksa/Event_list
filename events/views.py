from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Event, Participant
from .forms import EventForm, ParticipantForm
from django.utils import timezone
from django.db.models import Q, Count

def event_list(request):
    events = Event.objects.annotate(participant_count=Count('participants'))

    # Параметры фильтрации
    search = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    status = request.GET.get('status', '')
    current_sort = request.GET.get('sort', '')

    # Определение направления сортировки для всех столбцов
    sort_params = {
        'title': '-title' if current_sort == 'title' else 'title',
        'start_date': '-start_date' if current_sort == 'start_date' else 'start_date',
        'end_date': '-end_date' if current_sort == 'end_date' else 'end_date',
        'status': '-status' if current_sort == 'status' else 'status',
        'updated_at': '-updated_at' if current_sort == 'updated_at' else 'updated_at',
        'participant_count': '-participant_count' if current_sort == 'participant_count' else 'participant_count',
    }

    # Фильтрация
    if search:
        events = events.filter(
            Q(title__icontains=search) |
            Q(location__icontains=search) |
            Q(description__icontains=search)
        )
    if start_date:
        try:
            date_obj = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            events = events.filter(start_date__date=date_obj)
        except ValueError:
            pass
    if status:
        events = events.filter(status=status)

    # Сортировка
    allowed_sorts = [
        'title', '-title',
        'start_date', '-start_date',
        'end_date', '-end_date',
        'status', '-status',
        'updated_at', '-updated_at',
        'participant_count', '-participant_count'
    ]
    if current_sort in allowed_sorts:
        events = events.order_by(current_sort)
    else:
        events = events.order_by('-start_date')

    # Статистика статусов
    status_stats = [
        {'status': code, 'name': name, 'count': events.filter(status=code).count()}
        for code, name in Event.STATUS_CHOICES
    ]

    # Пагинация
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'events/event_list.html', {
        'page_obj': page_obj,
        'status_stats': status_stats,
        'sort_params': sort_params,
        'request': request,
        'current_sort': current_sort,
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

def delete_participant(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    participant.delete()
    return redirect('event_participants', event_id=participant.event.id)

def register_participant(request, event_id=None):
    event = None
    if event_id:
        event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            try:
                participant = form.save(commit=False)
                if event:
                    participant.event = event
                participant.save()
                return redirect('event_participants', event_id=event_id) if event_id else redirect('event_list')
            except IntegrityError:
                form.add_error('email', 'Этот email уже зарегистрирован для данного события')
    else:
        initial = {'event': event} if event else {}
        form = ParticipantForm(initial=initial)
    return render(request, 'events/register_participant.html', {'form': form, 'event': event})

def event_participants(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participants = Participant.objects.filter(event=event).select_related('event')
    search = request.GET.get('search', '')
    if search:
        participants = participants.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search)
        )
    return render(request, 'events/participants.html', {
        'event': event,
        'participants': participants
    })
