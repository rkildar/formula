import json
from datetime import datetime, timedelta

from django.db.models import Count, Sum
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from formula.models_cma import CarCondition, Daily, Damage, Employee, Vehicle


def dashboard_callback(request, context):
    # Get counts
    active_vehicles = Vehicle.objects.filter(active=1).count()
    total_vehicles = Vehicle.objects.count()
    active_employees = Employee.objects.filter(leaving__isnull=True).count()
    total_employees = Employee.objects.count()
    
    # Get recent damages
    recent_damages = Damage.objects.order_by('-day')[:5]
    damages_count = Damage.objects.count()
    
    # Get daily stats for the last 7 days
    today = datetime.now().date()
    last_week = today - timedelta(days=7)
    daily_stats = Daily.objects.filter(day__gte=last_week).order_by('day')
    
    # Prepare data for charts
    days = [d.day.strftime('%d.%m') for d in daily_stats]
    delivery_stops = [d.delivery_stops for d in daily_stats]
    delivery_packets = [d.delivery_packets for d in daily_stats]
    pickup_stops = [d.pickup_stops for d in daily_stats]
    pickup_packets = [d.pickup_packets for d in daily_stats]
    
    # Calculate total kilometers driven
    total_km = 0
    car_conditions = CarCondition.objects.filter(
        day__gte=last_week, 
        km_start__isnull=False, 
        km_end__isnull=False
    )
    for cc in car_conditions:
        if cc.km_end > cc.km_start:  # Ensure valid data
            total_km += (cc.km_end - cc.km_start)
    
    context.update(
        {
            "navigation": [
                {"title": _("Dashboard"), "link": "/", "active": True},
                {"title": _("Fleet"), "link": "/admin/formula/vehicle/"},
                {"title": _("Employees"), "link": "/admin/formula/employee/"},
            ],
            "filters": [
                {"title": _("All"), "link": "#", "active": True},
                {
                    "title": _("Last 7 days"),
                    "link": "#",
                },
            ],
            "kpi": [
                {
                    "title": _("Active Vehicles"),
                    "metric": f"{active_vehicles}",
                    "footer": mark_safe(
                        f'<strong class="text-green-600 font-medium">{active_vehicles}/{total_vehicles}</strong>&nbsp;vehicles in service'
                    ),
                },
                {
                    "title": _("Active Employees"),
                    "metric": f"{active_employees}",
                    "footer": mark_safe(
                        f'<strong class="text-green-600 font-medium">{active_employees}/{total_employees}</strong>&nbsp;employees'
                    ),
                },
                {
                    "title": _("Total Kilometers"),
                    "metric": f"{total_km:,}",
                    "footer": mark_safe(
                        f'<strong class="text-green-600 font-medium">Last 7 days</strong>'
                    ),
                },
            ],
            "progress": [
                {
                    "title": _("Delivery Stops"),
                    "description": f"{sum(delivery_stops) if delivery_stops else 0}",
                    "value": 100,
                },
                {
                    "title": _("Delivery Packets"),
                    "description": f"{sum(delivery_packets) if delivery_packets else 0}",
                    "value": 100,
                },
                {
                    "title": _("Pickup Stops"),
                    "description": f"{sum(pickup_stops) if pickup_stops else 0}",
                    "value": 100,
                },
                {
                    "title": _("Pickup Packets"),
                    "description": f"{sum(pickup_packets) if pickup_packets else 0}",
                    "value": 100,
                },
                {
                    "title": _("Damages"),
                    "description": f"{damages_count}",
                    "value": 100,
                },
            ],
            "chart": json.dumps(
                {
                    "labels": days,
                    "datasets": [
                        {
                            "label": _("Delivery Stops"),
                            "type": "line",
                            "data": delivery_stops,
                            "backgroundColor": "#f0abfc",
                            "borderColor": "#f0abfc",
                        },
                        {
                            "label": _("Delivery Packets"),
                            "data": delivery_packets,
                            "backgroundColor": "#9333ea",
                        },
                        {
                            "label": _("Pickup Stops"),
                            "type": "line",
                            "data": pickup_stops,
                            "backgroundColor": "#60a5fa",
                            "borderColor": "#60a5fa",
                        },
                        {
                            "label": _("Pickup Packets"),
                            "data": pickup_packets,
                            "backgroundColor": "#3b82f6",
                        },
                    ],
                }
            ),
            "performance": [
                {
                    "title": _("Recent Damages"),
                    "metric": f"{damages_count}",
                    "footer": mark_safe(
                        '<strong class="text-red-600 font-medium">Attention needed</strong>&nbsp;for vehicle maintenance'
                    ),
                    "table": [
                        {
                            "columns": [
                                {"name": _("Date")},
                                {"name": _("Vehicle")},
                                {"name": _("Type")},
                                {"name": _("Cost")},
                            ],
                            "rows": [
                                [
                                    damage.day.strftime('%d.%m.%Y'),
                                    f"ID: {damage.vid}",
                                    damage.dmgtype[:30] + ('...' if len(damage.dmgtype) > 30 else ''),
                                    f"€{damage.dmg_costs if damage.dmg_costs else 'N/A'}"
                                ]
                                for damage in recent_damages
                            ],
                        }
                    ],
                },
            ],
        },
    )

    return context