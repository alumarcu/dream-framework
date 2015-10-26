from django.core.management.base import BaseCommand, CommandError
import traceback


class Command(BaseCommand):
    help = 'Process a single match by a given id'

    def add_arguments(self, parser):
        parser.add_argument('match_id', nargs='?', type=int)

    def handle(self, *args, **options):
        from dream.engine.soccer.match.simulation import ManualMatch
        try:
            mm = ManualMatch(options['match_id'])
            mm.initialize()
            mm.begin_simulation()

        except IndexError:
            traceback.print_exc()
            raise CommandError('Please supply a valid match id')
        except Exception as e:
            traceback.print_exc()
            raise CommandError('Unexpected exception %s: %s' % (type(e), e))
