from django.db import models
from django.utils.translation import gettext_lazy as _


class CMAUser(models.Model):
    username = models.CharField(_("username"), max_length=24)
    password = models.CharField(_("password"), max_length=64)
    salt = models.CharField(_("salt"), max_length=5)
    firstname = models.CharField(_("first name"), max_length=16)
    lastname = models.CharField(_("last name"), max_length=32)
    email = models.CharField(_("email"), max_length=40)
    rights = models.IntegerField(_("rights"))
    active = models.IntegerField(_("active"))
    sessionid = models.CharField(_("session ID"), max_length=40, null=True, blank=True)

    class Meta:
        db_table = "user"
        verbose_name = _("CMA user")
        verbose_name_plural = _("CMA users")
        managed = False  # Use existing table

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class EmployeeGroup(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(_("type"), max_length=64)

    class Meta:
        db_table = "employee_groups"
        verbose_name = _("employee group")
        verbose_name_plural = _("employee groups")
        managed = False  # Use existing table

    def __str__(self):
        return self.type


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.IntegerField(_("employee ID"))
    employee_group = models.IntegerField(_("employee group"))
    salutation = models.CharField(_("salutation"), max_length=6)
    firstname = models.CharField(_("first name"), max_length=16)
    lastname = models.CharField(_("last name"), max_length=24)
    street = models.CharField(_("street"), max_length=32)
    zip = models.IntegerField(_("ZIP"))
    town = models.CharField(_("town"), max_length=24)
    birthday = models.DateField(_("birthday"))
    social_number = models.CharField(_("social number"), max_length=16)
    medical_insurance = models.CharField(_("medical insurance"), max_length=32)
    tax_number = models.BigIntegerField(_("tax number"), null=True, blank=True)
    entry = models.DateField(_("entry"))
    trial_period = models.DateField(_("trial period"))
    year_contract = models.DateField(_("year contract"))
    leaving = models.DateField(_("leaving"), null=True, blank=True)
    temporary = models.IntegerField(_("temporary"))
    working_hours = models.FloatField(_("working hours"))
    holidays = models.IntegerField(_("holidays"))
    holidays_remaining = models.IntegerField(_("holidays remaining"))
    tax_class = models.IntegerField(_("tax class"))
    drivers_license = models.CharField(_("driver's license"), max_length=3)
    driver_card = models.IntegerField(_("driver card"))
    modules = models.IntegerField(_("modules"))
    modulename = models.CharField(_("module name"), max_length=32, null=True, blank=True)
    moduledate = models.DateField(_("module date"), null=True, blank=True)
    work_starting = models.TimeField(_("work starting"), default="07:15:00")
    work_break = models.TimeField(_("work break"), default="01:00:00")
    sessionid = models.CharField(_("session ID"), max_length=40, null=True, blank=True)
    img_id = models.IntegerField(_("image ID"), null=True, blank=True)
    readed = models.DateTimeField(_("read"), auto_now=True)

    class Meta:
        db_table = "employee"
        verbose_name = _("employee")
        verbose_name_plural = _("employees")
        managed = False  # Use existing table

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class VPollutantClass(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_("name"), max_length=64)

    class Meta:
        db_table = "v_pollutant_class"
        verbose_name = _("pollutant class")
        verbose_name_plural = _("pollutant classes")
        managed = False  # Use existing table

    def __str__(self):
        return self.name


class VImpulsion(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_("name"), max_length=64)

    class Meta:
        db_table = "v_impulsion"
        verbose_name = _("impulsion")
        verbose_name_plural = _("impulsions")
        managed = False  # Use existing table

    def __str__(self):
        return self.name


class VConstruction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_("name"), max_length=64)

    class Meta:
        db_table = "v_construction"
        verbose_name = _("construction")
        verbose_name_plural = _("constructions")
        managed = False  # Use existing table

    def __str__(self):
        return self.name


class IntervalGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_("name"), max_length=64)

    class Meta:
        db_table = "interval_groups"
        verbose_name = _("interval group")
        verbose_name_plural = _("interval groups")
        managed = False  # Use existing table

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(_("brand"), max_length=24)
    model = models.CharField(_("model"), max_length=16)
    interval_group = models.IntegerField(_("interval group"))
    license_plate = models.CharField(_("license plate"), max_length=12)
    insurance_number = models.CharField(_("insurance number"), max_length=16)
    registrationdate = models.DateField(_("registration date"))
    vin = models.CharField(_("VIN"), max_length=20)
    servicelife = models.DateField(_("service life"))
    inspection = models.DateField(_("inspection"))
    construction = models.IntegerField(_("construction"))
    driver_card = models.IntegerField(_("driver card"), default=0)
    comment = models.CharField(_("comment"), max_length=200)
    active = models.IntegerField(_("active"), default=1)
    added = models.DateField(_("added"))
    sign_off = models.DateField(_("sign off"), null=True, blank=True)
    reason = models.CharField(_("reason"), max_length=200)
    pollutant_class = models.IntegerField(_("pollutant class"), default=0)
    impulsion = models.IntegerField(_("impulsion"), default=0)
    tour = models.IntegerField(_("tour"), default=0)
    readed = models.DateTimeField(_("read"), auto_now=True)
    mwa = models.IntegerField(_("mwa"), default=0)
    financing = models.IntegerField(_("financing"), default=0)
    leasing_mile = models.IntegerField(_("leasing mile"), default=0)
    leasing_nr = models.CharField(_("leasing number"), max_length=32)
    leasing_provider = models.CharField(_("leasing provider"), max_length=64)
    leasing_beginn = models.DateField(_("leasing begin"), null=True, blank=True)
    leasing_end = models.DateField(_("leasing end"), null=True, blank=True)
    tacho_test = models.DateField(_("tacho test"), null=True, blank=True)
    sp_insp = models.DateField(_("sp inspection"), null=True, blank=True)
    drain = models.FloatField(_("drain"), default=0)
    leasing_kmm = models.IntegerField(_("leasing kmm"), null=True, blank=True)
    leasing_kmg = models.IntegerField(_("leasing kmg"), null=True, blank=True)

    class Meta:
        db_table = "vehicles"
        verbose_name = _("vehicle")
        verbose_name_plural = _("vehicles")
        managed = False  # Use existing table

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    key_id = models.IntegerField(_("key ID"))
    day = models.DateField(_("day"))
    event = models.CharField(_("event"), max_length=64, null=True, blank=True)
    sort = models.CharField(_("sort"), max_length=16)
    gid = models.IntegerField(_("group ID"), null=True, blank=True)
    bc = models.CharField(_("bc"), max_length=16, null=True, blank=True)

    class Meta:
        db_table = "appointments"
        verbose_name = _("appointment")
        verbose_name_plural = _("appointments")
        managed = False  # Use existing table

    def __str__(self):
        return f"{self.event} on {self.day}"


class CarCondition(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField(_("day"))
    vid = models.IntegerField(_("vehicle ID"))
    eid = models.IntegerField(_("employee ID"))
    seid = models.IntegerField(_("seid"), default=0)
    tour = models.IntegerField(_("tour"))
    km_start = models.IntegerField(_("km start"), null=True, blank=True)
    km_end = models.IntegerField(_("km end"), null=True, blank=True)
    refuel = models.CharField(_("refuel"), max_length=32, null=True, blank=True)
    delivery = models.IntegerField(_("delivery"), null=True, blank=True)

    class Meta:
        db_table = "carcondition"
        verbose_name = _("car condition")
        verbose_name_plural = _("car conditions")
        managed = False  # Use existing table

    def __str__(self):
        return f"Vehicle {self.vid} on {self.day}"


class Daily(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField(_("day"))
    tours = models.IntegerField(_("tours"))
    delivery_stops = models.IntegerField(_("delivery stops"))
    delivery_packets = models.IntegerField(_("delivery packets"))
    express_plus = models.IntegerField(_("express plus"))
    express10 = models.IntegerField(_("express 10"))
    express12 = models.IntegerField(_("express 12"))
    pickup_stops = models.IntegerField(_("pickup stops"))
    pickup_packets = models.IntegerField(_("pickup packets"))

    class Meta:
        db_table = "daily"
        verbose_name = _("daily")
        verbose_name_plural = _("dailies")
        managed = False  # Use existing table

    def __str__(self):
        return f"Daily report for {self.day}"


class Damage(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField(_("day"))
    eid = models.IntegerField(_("employee ID"))
    vid = models.IntegerField(_("vehicle ID"))
    dmgtype = models.CharField(_("damage type"), max_length=100)
    comment = models.CharField(_("comment"), max_length=200)
    dmg_number = models.CharField(_("damage number"), max_length=64, null=True, blank=True)
    dmg_sum = models.FloatField(_("damage sum"), null=True, blank=True)
    dmg_costs = models.FloatField(_("damage costs"), null=True, blank=True)
    damage_art = models.IntegerField(_("damage art"), default=0)

    class Meta:
        db_table = "damages"
        verbose_name = _("damage")
        verbose_name_plural = _("damages")
        managed = False  # Use existing table

    def __str__(self):
        return f"Damage to vehicle {self.vid} on {self.day}"