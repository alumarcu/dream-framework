from django.core.management.base import BaseCommand, CommandError
import traceback


class Command(BaseCommand):
    help = 'Process a single match by a given id'

    def handle(self, *args, **options):
        self.compute_board_template()
        pass

    def compute_board_template(self):
        """
        Calculates the zones of the selected board template and updates the FieldZoneXy table
        """
        # TODO: (Should cover with unit test)
        from dream.core.models import BoardTemplate
        from dream.engine.soccer.tools import engine_params
        from dream.engine.soccer.models import FieldZone, FieldZoneXy

        template_param = engine_params('template')
        """:type : dream.engine.soccer.models.EngineParam"""

        template_id = template_param.value

        tmpl = BoardTemplate.objects.get(pk=template_id)
        """:type : dream.engine.soccer.models.BoardTemplate"""

        field_zones = FieldZone.objects.all()
        """:type : list[dream.engine.soccer.models.FieldZone]"""

        grid_width = tmpl.cols * tmpl.zone_width
        grid_height = tmpl.rows * tmpl.zone_height

        # Remove previous calculations
        FieldZoneXy.objects.filter(template=tmpl).delete()

        for fz in field_zones:
            fz_xy = FieldZoneXy()
            """:type : dream.engine.soccer.models.FieldZoneXy"""

            fz_xy.zone = fz
            fz_xy.template = tmpl

            fz_xy.home_xi = fz.col * tmpl.zone_width - tmpl.zone_width
            fz_xy.home_xj = fz.col * tmpl.zone_width

            fz_xy.home_yi = fz.row * tmpl.zone_height - tmpl.zone_height
            fz_xy.home_yj = fz.row * tmpl.zone_height

            fz_xy.away_xi = grid_width - fz_xy.home_xi
            fz_xy.away_xj = grid_width - fz_xy.home_xj

            fz_xy.away_yi = grid_height - fz_xy.home_yi
            fz_xy.away_yj = grid_height - fz_xy.home_yj

            fz_xy.create_centers()
            fz_xy.save()
