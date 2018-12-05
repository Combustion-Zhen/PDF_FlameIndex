import numpy as np
from scipy import special
import cantera as ct

def BilgerMixtureFraction( flame, fuel, oxidizer ):

    zFuel = BilgerSpecificMoleNumber( fuel )
    zOxidizer = BilgerSpecificMoleNumber( oxidizer )
    v = VectorMixtureFractionForMassFraction( fuel, oxidizer )

    Z = np.dot( flame.Y.transpose(), v )
    Z -= zOxidizer / ( zFuel - zOxidizer )

    return Z

def BilgerSpecificMoleNumber( gas ):

    zC = gas.elemental_mass_fraction('C')/gas.atomic_weight('C')
    zH = gas.elemental_mass_fraction('H')/gas.atomic_weight('H')
    zO = gas.elemental_mass_fraction('O')/gas.atomic_weight('O')

    z = 2.*zC + 0.5*zH - zO

    return z

def LagrangianFlameIndex( flame, fuel, oxidizer, 
                          speciesList = ['CO2', 'CO', 'H2O', 'H2'],
                          betaLean = 5., betaRich = 0.291 ):

    C, D, R = TransportBudget( flame )

    vectorMixtureFraction = VectorMixtureFractionForMassFraction( 
            fuel, oxidizer )
    vectorProgressVariable = VectorProgressVariableForMassFraction( 
            flame.gas, speciesList )

    fluxMixtureFraction = np.dot( D.transpose(), vectorMixtureFraction )
    fluxProgressVariable = np.dot( D.transpose(), vectorProgressVariable )

    magFluxMixtureFraction = np.absolute( fluxMixtureFraction )
    magFluxProgressVariable = np.absolute( fluxProgressVariable )

    flameMixtureFraction = BilgerMixtureFraction( flame, fuel, oxidizer )
    flameBeta =  ( 0.5 * ( betaLean - betaRich )
                  *special.erfc( ( flameMixtureFraction - 0.06 ) / 0.01 ) 
                 ) + betaRich
    magFlameBeta = np.absolute( flameBeta )

    indexLagrangian = ( magFluxProgressVariable 
                       - magFlameBeta * magFluxMixtureFraction 
                      ) / ( magFluxProgressVariable 
                           + magFlameBeta * magFluxMixtureFraction )
    return indexLagrangian

def ProgressVariable( flame, speciesList ):

    v = VectorProgressVariableForMassFraction( flame.gas, speciesList )

    c = np.dot( flame.Y.transpose(), v )

    return c

def ScalarDissipationRateMixtureFraction( flame, fuel, oxidizer ):

    mixtureFraction = BilgerMixtureFraction( flame, fuel, oxidizer )

    mixtureFractionGradient = np.gradient( Z, flame.grid )

    flame.transport_model = 'UnityLewis'

    chi = 2. * flame.mix_diff_coeffs[0] * np.square( mixtureFractionGradient )

    return chi

def StoichiometricMixtureFraction( fuel, oxidizer ):

    zFuel = BilgerSpecificMoleNumber( fuel )
    zOxidizer = BilgerSpecificMoleNumber( oxidizer )

    nu = - zFuel / zOxidizer

    Zst = 1. / ( 1. + nu )

    return Zst

def TakenoIndex( flame, fuelName, oxidizerName ):

    indexFuel = flame.gas.species_index( fuelName )
    indexOxidizer = flame.gas.species_index( oxidizerName )

    gradientFuel = np.gradient( flame.Y[indexFuel], flame.grid )
    gradientOxidizer = np.gradient( flame.Y[indexOxidizer], flame.grid )

    indexTakeno = gradientFuel * gradientOxidizer
    indexTakeno /= np.maximum( np.absolute( indexTakeno ), 
                               np.finfo( float ).resolution )

    return indexTakeno

def TransportBudget( flame ):

    gradientMassFraction = np.gradient( flame.Y, flame.grid, axis = 1 )

    convection = flame.density * flame.u * gradientMassFraction

    reaction = ( flame.net_production_rates.transpose() 
                * flame.gas.molecular_weights ).transpose()

    diffusion = convection - reaction

    return convection, diffusion, reaction

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
