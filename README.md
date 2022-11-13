# N2-Tank-and-Regulator-Sizing
First approximate models for sizing the pressure regulator and high pressure nitrogen tank

Current Assumptions/Simplifications:
- Constant massflowrate of propellants
- Ideal pressure regulator (constant outlet pressure over time as flow rate, inlet pressure and volumetric flow rate changes)
- Nitrogen is modelled as an ideal gas (some compressibility effects may be noticeable at high pressures)
- Nitrogen gas and nitrous vapour exhibit no interaction/mixing (modelled as 2 separate gases in the same volume with the pressures of each summing to the total pressure)
- Nitrogen expansion in the tank in adiabatic and isentropic (no heat transfer from tank walls during short burn time ~6s)
- Nitrogen flow through regulator is an isenthalpic and adiabatic (no enthalpy change and no heat transfer to regulator) and therefore N2 temperature does not change through regulator. This assumes the velocity change of the N2 through the regulator is negligible
- Nitrous vapour pressure modelled as a linear drop of ~13 bar over time starting at 40 bar (based on previous hot fire data)
- Nitrous density approximated at a constant, average value of 800kg/m^3 during burn (pretty close for small pressure/temp changes)
