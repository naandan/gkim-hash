from django.core.management.base import BaseCommand, CommandError
from master.models import Master, Congregation
from datetime import datetime, timedelta
from master.constans import DaysOfWeek
from django.db.models import Exists, OuterRef
from management.models import ManagementPresence

class Command(BaseCommand):
    help = 'Cek Presensi Jemaat yang tidak hadir'

    def add_arguments(self, parser):
        # get current day (e.g Monday, Tuesday, etc)
        parser.add_argument('day', type=int, help='Day of week (1-7), 1: Monday, 2: Tuesday, 3: Wednesday, 4: Thursday, 5: Friday, 6: Saturday, 7: Sunday', nargs='?', default=datetime.now().weekday() + 1)
        
    def handle(self, *args, **options):
        # get all jemaat not present in current day
        absent_congregation = Congregation.objects.filter(
            masteruser__date_of_death=None,
            is_congregation=True,
            worship__day_worship=options['day'],
        ).exclude(
            Exists(
                ManagementPresence.objects.filter(
                    masteruser=OuterRef('masteruser'),
                    created_at__date=datetime.now().date()
                    
                )
            )
        ).select_related('masteruser', 'worship')

        if absent_congregation.count() == 0:
            self.stdout.write(self.style.SUCCESS('Tidak ada jemaat yang tidak hadir'))
            return
        
        absent_presences = ManagementPresence.objects.bulk_create(
            [ManagementPresence(masteruser=congregation.masteruser, worship=congregation.worship, present=False) for congregation in absent_congregation]
        )
        
        