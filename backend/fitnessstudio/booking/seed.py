import pandas as pd
from fitness.models import FitnessClass, Booking
from django.utils.dateparse import parse_datetime

df = pd.read_csv('fitness_classes.csv')
for _, row in df.iterrows():
    FitnessClass.objects.create(
        id=row['id'],
        name=row['name'],
        date_time=parse_datetime(row['date_time']),
        instructor=row['instructor'],
        capacity=row['capacity'],
        available_slots=row['available_slots']
    )
