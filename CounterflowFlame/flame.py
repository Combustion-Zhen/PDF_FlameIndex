import numpy as np
import cantera as ct

def BilgerMixtureFraction( flame, fuel, oxidizer ):

    zFuel = BilgerSpecificMoleNumber( fuel )
    zOxidizer = BilgerSpecificMoleNumber( oxidizer )
    v = VectorMixtureFractionForMassFraction( fuel, oxidizer )

    Z = np.dot( flame.Y.transpose(), v )
    Z -= zOxidizer / ( zFuel - zOxidizer )

    return Z

def ProgressVariable( flame, speciesList ):

    v = VectorProgressVariableForMassFraction( flame.gas, speciesList )

    c = np.dot( flame.Y.transpose(), v )

    return c

def VectorMixtureFractionForMassFraction( fuel, oxidizer ):

    zFuel = BilgerSpecificMoleNumber( fuel )
    zOxidizer = BilgerSpecificMoleNumber( oxidizer )

    mixtureFractionDenominator = zFuel - zOxidizer

    v = np.zeros( fuel.n_species )
    for i in range( fuel.n_species ):
        v[i] = 2.*fuel.n_atoms(i,'C') \
              +0.5*fuel.n_atoms(i,'H') \
              -fuel.n_atoms(i,'O')

    v /= fuel.molecular_weights
    v /= mixtureFractionDenominator

    return v

def VectorProgressVariableForMassFraction( gas, speciesList ):

    v = np.zeros( gas.n_species )

    for species in speciesList :
        v[gas.species_index(species)] = 1.

    return v

def BilgerSpecificMoleNumber( gas ):

    zC = gas.elemental_mass_fraction('C')/gas.atomic_weight('C')
    zH = gas.elemental_mass_fraction('H')/gas.atomic_weight('H')
    zO = gas.elemental_mass_fraction('O')/gas.atomic_weight('O')

    z = 2.*zC + 0.5*zH - zO

    return z
