import numpy as np
import pandas as pd
import sys

from gamspy import (
    Alias,
    Container,
    Equation,
    Model,
    Number,
    Parameter,
    Product,
    Set,
    Sum,
    Variable,
    Sense
)

def main():
    cont = Container()

    i = Set(
        cont,
        name="i",
        records=["BRD", "MLK"],
        description="goods",
    )
    h = Set(
        cont,
        name="hh",
        records=["CAP", "LAB"],
        description="factors",
        )
    
    # Parameters
    alpha = Parameter(
        cont,
        name="delta",
        domain=i,
        description="Share parameter in utility function",
        records=[("BRD", 0.2), ("MLK", 0.8)],
    )

    px = Parameter(
        cont,
        name="px",
        domain=i,
        description="Price of the i-th good",
        records=[("BRD", 1), ("MLK", 2)],
    )

    pf = Parameter(
        cont,
        name="pf",
        domain="h",
        description="Price of the h-th factor",
        records=[("CAP", 2), ("LAB", 1)],
    )

    ff = Parameter(
        cont,
        name="ff",
        domain="h",
        description="Factor endowment",
        records=[("CAP", 10), ("LAB", 20)],
    )

    # Variables
    X = Variable(
        cont,
        name="X",
        type="positive",
        domain=i,
        description="Consumption of the i-th good",
    )

    UU = Variable(
        cont,
        name="UU",
        type="free",
        description="Utility",
    )

    eqX = Equation(
        cont,
        name="eqX",
        domain="i",
        description="Household demand function",
    )

    obj = Equation(
        cont,
        name="obj",
        description="Utility function",
    )

    # Specification of Equations
    eqX[i] = X[i] == alpha[i] * Sum(h, pf[h] * ff[h]) / px[i]

    obj[...] = UU == Product(i, X[i] ** alpha[i])

    # Setting lower bounds on variables to avoid division by zero
    X.lo[i] = 0.001

    # Defining the model
    HHmax = Model(
        cont,
        name="HHmax",
        equations=cont.getEquations(),
        problem="NLP",
        sense=Sense.MAX,
        objective=UU
    )

    HHmax.solve()

    print(HHmax.solve())
    print(eqX.records)
    print(obj.records)
    print(X.records.set_index(["i"]))
    #print(
       # "\nObjective Function Variable <omega>: ",
       # round(X.records.set_index("i").level.tolist()[0], 2),
   # )
    #print("\nDomestic prices:\n", UU.records.level)


if __name__ == "__main__":
    main()