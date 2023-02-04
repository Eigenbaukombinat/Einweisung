from django.db import models
from django.db.models.signals import m2m_changed
from django.db import transaction


einweisung_level_choices = (
    ('E', 'Instructor'),
    ('X', 'Allowed'),
    ('F', 'Advanced')
)


einweisable_types = (
    ('workshop', 'Workshop'),
    ('machine', 'Machine'),
    ('activity', 'Activity')
)


class Member(models.Model):
    name = models.CharField(max_length=200)
    member_id = models.CharField(max_length=50, unique=True) 
    is_active = models.BooleanField(default=True)
    rfid = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Einweisable(models.Model):
    name = models.CharField(max_length=200)
    etype = models.CharField(max_length=200, choices=einweisable_types,
                default='machine')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name


class Room(Einweisable):
    pass


class Einweisung(models.Model):
    einweisable = models.ForeignKey(Einweisable, on_delete=models.CASCADE)
    member = models.ForeignKey(
        Member, related_name="einweisung_member", on_delete=models.CASCADE)
    instructor = models.ForeignKey(Member,
        related_name="einweisung_instructor", on_delete=models.CASCADE)
    level = models.CharField(max_length=1, choices=einweisung_level_choices)
    issue_date = models.DateField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return (f"{self.member.name}: {self.level} "
                f"{self.einweisable.name} ({self.issue_date})")

    class Meta:
        verbose_name_plural = "Einweisungen"
        permissions = [
            ("view_all", "View all einweisungen"),
        ]
        unique_together = (('einweisable', 'member', 'level'),)


class Multieinweisung(models.Model):
    einweisable = models.ForeignKey(Einweisable, on_delete=models.CASCADE)
    members = models.ManyToManyField(Member)
    level = models.CharField(max_length=1, choices=einweisung_level_choices)
    instructor = models.ForeignKey(Member,
        related_name="multieinweisung_instructor", on_delete=models.CASCADE)
    issue_date = models.DateField()

    def __str__(self):
        return (f"{self.instructor.name}: "
                f"{self.einweisable.name} ({self.issue_date})")

    class Meta:
        verbose_name_plural = "Multi-Einweisungen"
        permissions = [
            ("view_all", "View all einweisungen"),
        ]

