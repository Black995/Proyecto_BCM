from django.db import models
from bcm_phase1.models import CrisisScenario



class IncidentHistory(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.CharField(max_length=200, null=True, blank=True)

    crisis_scenario = models.ForeignKey(
        CrisisScenario, related_name='crisis_scenario_indicent_history', on_delete=models.CASCADE)

