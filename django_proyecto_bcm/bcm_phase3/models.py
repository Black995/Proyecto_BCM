from django.db import models
from bcm_phase1.models import CrisisScenario



class IncidentHistory(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    crisis_scenario = models.ForeignKey(
        CrisisScenario, related_name='crisis_scenario_indicent_history', on_delete=models.CASCADE)


class ContingencyPlan(models.Model):
    number_order = models.PositiveIntegerField()
    description = models.CharField(max_length=300)

    contingency_father = models.ForeignKey('self', blank=True, null=True, related_name='contingency_children', on_delete=models.CASCADE)
    crisis_scenario = models.ForeignKey(
        CrisisScenario, related_name='crisis_scenario_contingency_plan', on_delete=models.CASCADE)
