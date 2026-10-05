from django.core.exceptions import ValidationError
from django.db import models

from baseapp.models import BaseModel
from resumes.models import Resume
from vacancies.models import Vacancy


class Application(BaseModel):

    class Status(models.TextChoices):
        NEW = "new", "NEW"
        VIEWED = "viewed", "VIEWED"
        INVITED = "invited", "INVITED"
        REJECTED = "rejected", "REJECTED"

    TRANSITIONS = {
        Status.NEW: {Status.VIEWED, Status.INVITED, Status.REJECTED,},
        Status.VIEWED: {Status.INVITED, Status.REJECTED,},
        Status.INVITED: {Status.REJECTED,},
        Status.REJECTED: {Status.INVITED,},
    }

    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NEW, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["vacancy", "resume"], name="unique_application")]
        indexes = [models.Index(fields=["vacancy", "status"])]

    def __str__(self):
        return f"{self.resume.employee} -> {self.vacancy}"

    def can_change_to(self, new_status):
        return new_status in self.TRANSITIONS[self.status]

    def clean(self):
        if (self._state.adding and self.vacancy.status != Vacancy.StatusChoices.ACTIVE):
            raise ValidationError("Bu vakansiya faol emas.")