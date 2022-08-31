from django.db import models
from configuration.models import Headquarter


class Risk(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)

    headquarters = models.ManyToManyField(
        Headquarter, related_name='headquarter_risk')
    staffs = models.ManyToManyField(
        'bcm_phase2.staff', related_name='staff_risk')


class CrisisScenario(models.Model):

    VERY_UNLIKELY = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    SURE = 5
    FREQUENCY = (
        (VERY_UNLIKELY, 'Muy improbable'),
        (UNLIKELY, 'Improbable'),
        (POSSIBLE, 'Posible'),
        (LIKELY, 'Probable'),
        (SURE, 'Seguro'),
    )

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    frequency = models.SmallIntegerField(choices=FREQUENCY)

    headquarters = models.ManyToManyField(
        Headquarter, related_name='headquarter_crisis_scenario')
    _risks = models.ManyToManyField(
        Risk, related_name='crisis_scenario_risk', db_column='risks')

    @property
    def risks(self):
        return self._risks.values_list(flat=True)

    @risks.setter
    def risks(self, risk_ids):
        # Eliminamos los registros anteriores de los riesgos
        self._risks.clear()
        # Guardamos los nuevos registros
        if(risk_ids):
            for risk_id in risk_ids:
                risk = Risk.objects.filter(id=risk_id).first()
                if(risk is not None):
                    self._risks.add(risk)
