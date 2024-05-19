from django.core.management.base import BaseCommand
from django.db.models import Count
from officersHome.models import NewOfficerRegistration, OfficerStationGroup

class Command(BaseCommand):
    help = 'Update officer station groups'

    def handle(self, *args, **kwargs):
        # Clear existing grouped data
        OfficerStationGroup.objects.all().delete()

        # Group users by officer_current_station and get the count of users in each station
        stations_with_user_counts = NewOfficerRegistration.objects.values('officer_current_station').annotate(user_count=Count('id')).order_by('-user_count')

        # Save grouped data to the new model
        for station in stations_with_user_counts:
            OfficerStationGroup.objects.create(
                station_name=station['officer_current_station'],
                user_count=station['user_count']
            )

        self.stdout.write(self.style.SUCCESS('Successfully updated officer station groups'))
