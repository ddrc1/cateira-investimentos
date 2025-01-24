from django.core.management.base import BaseCommand
from django.core import management

from apps.assets.models import Asset, AssetType, Sector, SubSector

class Command(BaseCommand):
    """
    Command to populate specific tables:
    - Asset
    - AssetType
    - Sector
    - SubSector

    Note: This command should be considered when the application is
    deployed in Docker, or it is running for the first time.
    """

    help = 'Populate specific tables for the first time.'

    def handle(self, *args, **kwargs):
        if AssetType.objects.exists():
            self.stdout.write('AssetType already populated.')
        else:
            management.call_command('loaddata', 'assettype', format='json', verbosity=0)
            self.stdout.write('Successfully populated AssetType!')

        if Sector.objects.exists():
            self.stdout.write('Sector already populated.')
        else:
            management.call_command(
                'loaddata', 'sector', format='json', verbosity=0
            )
            self.stdout.write('Successfully populated Sector!')

        if SubSector.objects.exists():
            self.stdout.write('SubSector already populated.')
        else:
            management.call_command(
                'loaddata', 'subsector', format='json', verbosity=0
            )
            self.stdout.write('Successfully populated SubSector!')

        if Asset.objects.exists():
            self.stdout.write('Asset already populated.')
        else:
            management.call_command('loaddata', 'asset', format='json', verbosity=0)
            self.stdout.write('Successfully populated Asset!')