neutrons  = input('Enter the number of neutrons: ')
protons   = input('Enter the number of protons: ')
electrons = input('Enter the number of electrons: ')

amu = (float(neutrons) * 1.008664916) + (float(protons) * 1.00727647) + (float(electrons) * 0.000548597)
print('The atomic weight of the atom is {0} amu. ({1})'.format(round(amu), amu))
