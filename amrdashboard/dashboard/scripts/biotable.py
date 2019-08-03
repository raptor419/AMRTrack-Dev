import numpy as np
import pandas as pd
from django_pandas.io import read_frame

from dashboard.models import PathTest



def getdatatable():
    qs = PathTest.objects.all()
    df = read_frame(qs)
    print(df)
    return df

