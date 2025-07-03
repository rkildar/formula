from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    RangeDateFilter,
    RangeNumericFilter,
    RelatedDropdownFilter,
    TextFilter,
)
from unfold.decorators import display

from formula.models_cma import (
    Appointment,
    CMAUser,
    CarCondition,
    Daily,
    Damage,
    Employee,
    EmployeeGroup,
    IntervalGroup,
    VConstruction,
    VImpulsion,
    VPollutantClass,
    Vehicle,
)
from formula.sites import formula_admin_site


@admin.register(CMAUser, site=formula_admin_site)
class CMAUserAdmin(ModelAdmin):
    search_fields = ["username", "firstname", "lastname", "email"]
    list_display = ["username", "firstname", "lastname", "email", "rights", "active"]
    list_filter = ["rights", "active"]


@admin.register(EmployeeGroup, site=formula_admin_site)
class EmployeeGroupAdmin(ModelAdmin):
    search_fields = ["type"]
    list_display = ["id", "type"]


@admin.register(Employee, site=formula_admin_site)
class EmployeeAdmin(ModelAdmin):
    search_fields = ["firstname", "lastname", "employee_id"]
    list_display = [
        "display_header",
        "employee_id",
        "employee_group",
        "town",
        "working_hours",
        "holidays",
        "holidays_remaining",
    ]
    list_filter = [
        ("employee_group", RangeNumericFilter),
        "town",
        ("entry", RangeDateFilter),
    ]
    fieldsets = (
        (None, {"fields": ("employee_id", "employee_group", "salutation")}),
        (
            _("Personal info"),
            {
                "fields": (
                    ("firstname", "lastname"),
                    "street",
                    ("zip", "town"),
                    "birthday",
                    "social_number",
                    "medical_insurance",
                    "tax_number",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Employment"),
            {
                "fields": (
                    "entry",
                    "trial_period",
                    "year_contract",
                    "leaving",
                    "temporary",
                    "working_hours",
                    "holidays",
                    "holidays_remaining",
                    "tax_class",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Driving"),
            {
                "fields": (
                    "drivers_license",
                    "driver_card",
                    "modules",
                    "modulename",
                    "moduledate",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Work Schedule"),
            {
                "fields": ("work_starting", "work_break"),
                "classes": ["tab"],
            },
        ),
    )

    @display(description=_("Employee"), header=True)
    def display_header(self, instance: Employee):
        return f"{instance.firstname} {instance.lastname}"


@admin.register(VPollutantClass, site=formula_admin_site)
class VPollutantClassAdmin(ModelAdmin):
    search_fields = ["name"]
    list_display = ["id", "name"]


@admin.register(VImpulsion, site=formula_admin_site)
class VImpulsionAdmin(ModelAdmin):
    search_fields = ["name"]
    list_display = ["id", "name"]


@admin.register(VConstruction, site=formula_admin_site)
class VConstructionAdmin(ModelAdmin):
    search_fields = ["name"]
    list_display = ["id", "name"]


@admin.register(IntervalGroup, site=formula_admin_site)
class IntervalGroupAdmin(ModelAdmin):
    search_fields = ["name"]
    list_display = ["id", "name"]


@admin.register(Vehicle, site=formula_admin_site)
class VehicleAdmin(ModelAdmin):
    search_fields = ["brand", "model", "license_plate", "vin"]
    list_display = [
        "display_header",
        "license_plate",
        "brand",
        "model",
        "registrationdate",
        "inspection",
        "active",
    ]
    list_filter = [
        "brand",
        "model",
        ("active", ChoicesDropdownFilter),
        ("registrationdate", RangeDateFilter),
        ("inspection", RangeDateFilter),
    ]
    fieldsets = (
        (None, {"fields": ("brand", "model", "license_plate", "active")}),
        (
            _("Vehicle Details"),
            {
                "fields": (
                    "interval_group",
                    "insurance_number",
                    "registrationdate",
                    "vin",
                    "servicelife",
                    "inspection",
                    "construction",
                    "driver_card",
                    "comment",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Status"),
            {
                "fields": (
                    "added",
                    "sign_off",
                    "reason",
                    "pollutant_class",
                    "impulsion",
                    "tour",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Leasing"),
            {
                "fields": (
                    "financing",
                    "leasing_mile",
                    "leasing_nr",
                    "leasing_provider",
                    "leasing_beginn",
                    "leasing_end",
                    "leasing_kmm",
                    "leasing_kmg",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Maintenance"),
            {
                "fields": (
                    "tacho_test",
                    "sp_insp",
                    "drain",
                    "mwa",
                ),
                "classes": ["tab"],
            },
        ),
    )

    @display(description=_("Vehicle"), header=True)
    def display_header(self, instance: Vehicle):
        return f"{instance.brand} {instance.model}"


@admin.register(Appointment, site=formula_admin_site)
class AppointmentAdmin(ModelAdmin):
    search_fields = ["event"]
    list_display = ["id", "key_id", "day", "event", "sort", "gid", "bc"]
    list_filter = [("day", RangeDateFilter)]


@admin.register(CarCondition, site=formula_admin_site)
class CarConditionAdmin(ModelAdmin):
    list_display = ["id", "day", "vid", "eid", "tour", "km_start", "km_end", "refuel"]
    list_filter = [("day", RangeDateFilter), ("vid", RangeNumericFilter), ("eid", RangeNumericFilter)]


@admin.register(Daily, site=formula_admin_site)
class DailyAdmin(ModelAdmin):
    list_display = [
        "id",
        "day",
        "tours",
        "delivery_stops",
        "delivery_packets",
        "express_plus",
        "express10",
        "express12",
    ]
    list_filter = [("day", RangeDateFilter)]


@admin.register(Damage, site=formula_admin_site)
class DamageAdmin(ModelAdmin):
    search_fields = ["dmgtype", "comment"]
    list_display = ["id", "day", "eid", "vid", "dmgtype", "dmg_number", "dmg_sum", "dmg_costs"]
    list_filter = [
        ("day", RangeDateFilter),
        ("vid", RangeNumericFilter),
        ("eid", RangeNumericFilter),
        "dmgtype",
    ]