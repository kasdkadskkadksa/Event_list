from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Event, Participant
from .forms import EventForm, ParticipantForm
from django.utils import timezone
from django.db.models import Q, Count, F

def event_list(request):
    # Инициализация QuerySet с аннотацией количества участников
    events = Event.objects.annotate(participant_count=Count('participants'))

    # Фильтрация по общему поиску
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    # Фильтр по локации
    location = request.GET.get('location', '')
    if location:
        events = events.filter(location__icontains=location)

    # Фильтр по статусу
    status = request.GET.get('status', '')
    if status:
        events = events.filter(status=status)

    # Фильтр по дате начала
    start_date = request.GET.get('start_date', '')
    if start_date:
        try:
            date_obj = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            events = events.filter(start_date__date=date_obj)
        except ValueError:
            pass

    # Сортировка
    allowed_sorts = ['title', 'start_date', 'end_date', 'location', 'status', 'participant_count', 'updated_at']
    sort_by = request.GET.get('sort', '-start_date')
    if sort_by.lstrip('-') in allowed_sorts:
        events = events.order_by(sort_by)
    else:
        events = events.order_by('-start_date')

    # Статистика по статусам (на основе отфильтрованных событий)
    status_stats = []
    for status_code, status_name in Event.STATUS_CHOICES:
        count = events.filter(status=status_code).count()
        status_stats.append({'status': status_code, 'count': count, 'name': status_name})

    # Пагинация
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Передача данных в шаблон
    return render(request, 'events/event_list.html', {
        'page_obj': page_obj,
        'status_stats': status_stats,
        'request': request,
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

def event_participants(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participants = event.participants.all()
    return render(request, 'events/participants.html', {
        'event': event,
        'participants': participants,
    })

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

def participant_list(request):
    participants = Participant.objects.select_related('event')

    # Поиск по имени или email
    search = request.GET.get('search', '')
    if search:
        participants = participants.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search)
        )

    return render(request, 'events/participant_list.html', {
        'participants': participants
    })