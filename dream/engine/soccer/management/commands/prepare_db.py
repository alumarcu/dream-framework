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
        from dream.engine.soccer.tools import engine_params
        from dream.engine.soccer.models import BoardTemplate, FieldZone, FieldZoneXy

        template_param = engine_params('template')
        """:type : dream.engine.soccer.models.EngineParam"""

        template_id = template_param.value

        tmpl = BoardTemplate.objects.get(pk=template_id)
        """:type : dream.engine.soccer.models.BoardTemplate"""

        field_zones = FieldZone.objects.all()
        """:type : list[dream.engine.soccer.models.FieldZone]"""

        grid_width = tmpl.cols * tmpl.zone_width
        grid_height = tmpl.rows * tmpl.zone_height

        for fz in field_zones:
            fz_xy = FieldZoneXy()
            """:type : dream.engine.soccer.models.FieldZoneXy"""

            fz_xy.zone = fz
            fz_xy.template = template_id

            fz_xy.home_xi = fz.col * tmpl.zone_width - tmpl.zone_width
            fz_xy.home_xj = fz.col * tmpl.zone_width

            fz_xy.home_yi = fz.row * tmpl.zone_height - tmpl.zone_height
            fz_xy.home_yj = fz.row * tmpl.zone_height

            #fz_xy.away_xi =

        # TODO: Compute zones

        """
        def initialize_zones(self):
            from dream.engine.soccer.models import FieldZone

            raw_zones = FieldZone.objects.all()
            self.zone_len = (self.grid.length / 2) / self.rows
            self.zone_width = self.grid.width / self.cols

            self.zones = {}
            for zone in raw_zones:
                self.zones[zone.code] = {
                    'home_len': (
                        zone.row * self.zone_len - self.zone_len,
                        zone.row * self.zone_len),
                    'home_width': (
                        zone.col * self.zone_width - self.zone_width,
                        zone.col * self.zone_width),
                    'away_len': (
                        self.grid.length - (zone.row * self.zone_len - self.zone_len),
                        self.grid.length - (zone.row * self.zone_len)),
                    'away_width': (
                        self.grid.width - (zone.col * self.zone_width - self.zone_width),
                        self.grid.width - (zone.col * self.zone_width)),
                    }

                self.zones[zone.code]['home_center'] = self.get_zone_center(
                    self.zones[zone.code]['home_width'],
                    self.zones[zone.code]['home_len'])

                self.zones[zone.code]['away_center'] = self.get_zone_center(
                    self.zones[zone.code]['away_width'],
                    self.zones[zone.code]['away_len'])
        """
