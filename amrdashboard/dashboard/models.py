from django.contrib.auth.models import User
from django.db import models

# Create your models here.

ANTIMICROBIALS = ['amikacin',
                  'amoxicillin_clavulanicacid',
                  'ampicillin',
                  'ampicillin_sulbactum',
                  'cefaperazone_sulbactum',
                  'cefexime', 'cefotaxime',
                  'cefoxitin', 'ceftazidime',
                  'ceftazidime_clavalunicacid',
                  'ceftriaxone', 'chloramphenicol',
                  'ciprofloxacin', 'colistin',
                  'cotrimoxazole', 'ertapenem',
                  'erythromycin',
                  'gentamicin_highlevel', 'imipenem',
                  'levofloxacin', 'linezolid',
                  'meropenem', 'netilmicin',
                  'nitrofurantoin', 'penicillin',
                  'piperacillin_tazobactum',
                  'rifampicin', 'teicoplanin',
                  'tetracycline',
                  'ticarcillin_clavulanicacid',
                  'tigecycline', 'vancomycin']

ORGANISMS = ['acinetobacter',
             'citrobacter',
             'coagulase negative staphylococcus',
             'enterobacter',
             'enterococcus',
             'escherichia',
             'klebsiella',
             'methicillin sensitive staphylococcus aureus(mssa)',
             'pantoea aggiomeroms (prevously enterobacter)',
             'pseudomonas',
             'serratia marcescens',
             'staphyloccus hemolyticus (ms-cons)',
             'staphylococcus aureus',
             'staphylococcus aureus(mssa)',
             'staphylococcus epidermidis',
             'stenotnophomonas maltophilia']

COLLTYPES = ['Broncho-alveolar lavage',
             'Endotracheal aspirate',
             'CSF',
             'Blood',
             'Tracheal Aspirate',
             'Peritoneal',
             'Shunts',
             'Urine',
             'Catheter Tip',
             'Acitic Fluid',
             'Tissue Biopsy',
             'Pus Swab',
             'Pus',
             'Sputum',
             'Pleural',
             'Endotracheal washing',
             'Throat Swab',
             'Wound Swab']

SITES = ['Lab', 'ICU', 'Ward', 'Emergency']


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    name = models.CharField(max_length=50, null=True, blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class PathTest(models.Model):
    testid = models.CharField(max_length=25)
    date = models.DateField(null=True)
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()
    sampletype = models.CharField(max_length=50)
    organism = models.CharField(max_length=50)
    collsite = models.CharField(max_length=50)

    # AM Fields, add all
    amikacin = models.IntegerField(default=-1)
    amoxicillin_clavulanicacid = models.IntegerField(default=-1)
    ampicillin = models.IntegerField(default=-1)
    ampicillin_sulbactum = models.IntegerField(default=-1)
    cefaperazone_sulbactum = models.IntegerField(default=-1)
    cefexime = models.IntegerField(default=-1)
    cefotaxime = models.IntegerField(default=-1)
    cefoxitin = models.IntegerField(default=-1)
    ceftazidime = models.IntegerField(default=-1)
    ceftazidime_clavalunicacid = models.IntegerField(default=-1)
    ceftriaxone = models.IntegerField(default=-1)
    chloramphenicol = models.IntegerField(default=-1)
    ciprofloxacin = models.IntegerField(default=-1)
    colistin = models.IntegerField(default=-1)
    cotrimoxazole = models.IntegerField(default=-1)
    ertapenem = models.IntegerField(default=-1)
    erythromycin = models.IntegerField(default=-1)
    gentamicin_highlevel = models.IntegerField(default=-1)
    imipenem = models.IntegerField(default=-1)
    levofloxacin = models.IntegerField(default=-1)
    linezolid = models.IntegerField(default=-1)
    meropenem = models.IntegerField(default=-1)
    netilmicin = models.IntegerField(default=-1)
    nitrofurantoin = models.IntegerField(default=-1)
    penicillin = models.IntegerField(default=-1)
    piperacillin_tazobactum = models.IntegerField(default=-1)
    rifampicin = models.IntegerField(default=-1)
    teicoplanin = models.IntegerField(default=-1)
    tetracycline = models.IntegerField(default=-1)
    ticarcillin_clavulanicacid = models.IntegerField(default=-1)
    tigecycline = models.IntegerField(default=-1)
    vancomycin = models.IntegerField(default=-1)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.testid


# Snippets for Google Login

class GoogleProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    google_user_id = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=100)
    profile_url = models.CharField(max_length=100)
