import ineqpy
import numpy as np
import pandas as pd


def test_api():
    # todo improve this test.
    # only checks that all methods works.
    svy = ineqpy.api.Survey
    data = np.random.randint(0, 100, (int(1e3), 3))
    w = np.random.randint(1, 10, int(1e3)).reshape(-1, 1)
    data = np.hstack([data, w])
    columns = list("abcw")
    try:
        df = svy(data=data, columns=columns, weights="w")
        df.weights
        df.mean("a")
        df.var("a")
        df.skew("a")
        df.kurt("a")
        df.gini("a")
        df.atkinson("a")
        df.theil("a")
        df.percentile("a")
        assert True
    except Exception as e:
        assert False, e


def test_df():
    # GH #15
    LEN = 10
    values = [np.arange(LEN), np.random.randint(1, 10, LEN)]
    df = pd.DataFrame(values, index=["x", "n"]).T

    try:
        svy = ineqpy.api.Survey(df, df.index, df.columns, weights="n")
        svy.lorenz("x")
        assert True
    except Exception as e:
        assert False, e
