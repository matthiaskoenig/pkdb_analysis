import pint


# Define unit registry for examples

ureg = pint.UnitRegistry()
ureg.define("none = count")
ureg.define("cups = count")
ureg.define("beverages = count")
ureg.define("none = count")
ureg.define("percent = 0.01*count")
ureg.define("IU = [activity_amount]")
ureg.define("NO_UNIT = [no_unit]")
