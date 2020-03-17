from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity
dose = Q_(10.0, "mg/kg") * Q_(1.0, "mole/g")
print(dose)
dose.ito_reduced_units()
