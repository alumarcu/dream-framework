from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from dream.core.models import *


class MatchStatusFilter(admin.SimpleListFilter):
    """
    Allows filtering matches by their status in the admin interface
    """
    title = _('Status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            (Match.STATUS_SCHEDULED, _('Scheduled')),
            (Match.STATUS_SIM_STARTED, _('Sim Started')),
            (Match.STATUS_SIM_IN_PROGRESS, _('Sim In Progress')),
            (Match.STATUS_SIM_FINISHED, _('Sim Finished')),
            (Match.STATUS_RENDER_STARTED, _('Render Started')),
            (Match.STATUS_RENDER_IN_PROGRESS, _('Render In Progress')),
            (Match.STATUS_RENDER_FINISHED, _('Render Finished')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(status=self.value())


class SportFilter(admin.SimpleListFilter):
    title = _('Sport')
    parameter_name = 'sport'

    def lookups(self, request, model_admin):
        return (
            (Sport.SPORT_SOCCER_KEY, _('Association Football')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(sport__common_key=self.value())


class AttributeApplicabilityFilter(admin.SimpleListFilter):
    title = _('Applies to')
    parameter_name = 'applies_to'

    def lookups(self, request, model_admin):
        return (
            (Attribute.APPLIES_TO_MANAGER, _('Manager')),
            (Attribute.APPLIES_TO_NPC, _('NPC')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(applies_to=self.value())


class AttributeTypeFilter(admin.SimpleListFilter):
    title = _('Type')
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            (Attribute.ATTR_TYPE_TRAIT, _('%s - Trait' % Attribute.ATTR_TYPE_TRAIT)),
            (Attribute.ATTR_TYPE_SKILL, _('%s - Skill' % Attribute.ATTR_TYPE_SKILL)),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(type=self.value())


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'edit',
        'id',
        'status',
        'division',
        'round',
        'season',
        'date_scheduled',
        'modified'
    )
    list_filter = (MatchStatusFilter, )
    search_fields = [
        'division__name',
        'division__league__name'
    ]

    def edit(self, obj):
        return 'Edit'

    edit.short_description = ''
    edit.admin_order_field = 'requirement__name'

    class MatchTeamInline(admin.TabularInline):
        model = MatchTeam

    inlines = [MatchTeamInline]


@admin.register(MatchTeam)
class MatchTeamAdmin(admin.ModelAdmin):
    list_display = (
        'team',
        'role',
        'tactics',
        'tactics_ref'
    )


@admin.register(Npc)
class NpcAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'nickname',
        'id',
        'team',
        'club',
    )

    class NpcAttributeInline(admin.TabularInline):
        model = NpcAttribute

    inlines = [NpcAttributeInline]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'country_code',
        'id',
    )
    search_fields = [
        'name',
        'country_code',
    ]


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'country',
        'sport',
        'min_age',
        'max_age',
        'gender',
        'modified',
    )
    search_fields = [
        'name',
        'country__name',
        'country__country_code',
        'sport',
    ]
    list_filter = ('gender', SportFilter)

    class DivisionsInline(admin.TabularInline):
        model = Division

    inlines = [DivisionsInline]


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'sport',
        'applies_to',
        'modified',
        'type',
    )
    search_fields = [
        'name',
        'description',
    ]
    list_filter = (SportFilter, AttributeApplicabilityFilter, AttributeTypeFilter, )


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'common_key'
    )
    search_fields = [
        'name'
    ]


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'league',
        'level',
        'teams_num',
        'modified',
    )
    search_fields = [
        'name',
        'league__name',
        'league__country__name',
        'league__country__country_code'
    ]


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'modified',
        'manager',
        'country'
    )
    search_fields = [
        'name',
        'country__name',
        'country__country_code',
    ]

    class TeamInline(admin.TabularInline):
        model = Team

    inlines = [
        TeamInline
    ]


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'age',
        'gender',
        'modified',
    )
    search_fields = [
        'name',
        'user__first_name',
        'user__last_name',
        'user__email',
        'user__username'
    ]

    class ManagerAttributeInline(admin.TabularInline):
        model = ManagerAttribute

    inlines = [ManagerAttributeInline]


@admin.register(ManagerAttribute)
class ManagerAttributeAdmin(admin.ModelAdmin):
    list_display = (
        'manager',
        'attribute',
        'value',
    )
    search_fields = [
        'attribute__name'
    ]


@admin.register(NpcAttribute)
class NpcAttribute(admin.ModelAdmin):
    list_display = (
        'npc',
        'attribute',
        'value'
    )
    search_fields = [
        'attribute__name'
    ]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'club',
        'name',
        'gender',
        'modified',
    )
    search_fields = [
        'name'
        'club__name',
    ]

    class NpcInline(admin.TabularInline):
        model = Npc

    inlines = [
        NpcInline
    ]
