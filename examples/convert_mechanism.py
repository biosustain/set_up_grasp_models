import os

from set_up_grasp_models.set_up_models.convert_mechanisms import convert_er_mech_to_grasp_pattern


# convert orderedBiBi
file_in = os.path.join('mechanisms', 'orderedBiBi_mech_er.txt')
file_out = os.path.join('mechanisms', 'orderedBiBi_pattern.txt')

convert_er_mech_to_grasp_pattern(file_in, file_out)


# convert orderedBiBi with activation
file_in = os.path.join('mechanisms', 'orderedBiBiActiv_mech_er.txt')
file_out = os.path.join('mechanisms', 'orderedBiBiActiv_pattern.txt')
activ_list = ['pyr_c']

convert_er_mech_to_grasp_pattern(file_in, file_out, activ_list=activ_list)


# convert orderedBiBi with activation, where the reaction can proceed both
#  with and without the activator bound to the enzyme
file_in = os.path.join('mechanisms', 'orderedBiBiActivTwoTracks_mech_er.txt')
file_out = os.path.join('mechanisms', 'orderedBiBiActivTwoTracks_pattern.txt')
activ_list = ['pyr_c']

convert_er_mech_to_grasp_pattern(file_in, file_out, activ_list=activ_list)


# convert uniUniPromiscuous
file_in = os.path.join('mechanisms', 'uniUniPromiscuous_mech_er.txt')
file_out = os.path.join('mechanisms', 'uniUniPromiscuous_pattern.txt')

convert_er_mech_to_grasp_pattern(file_in, file_out, promiscuous=True)


# convert pingPongBiBi
file_in = os.path.join('mechanisms', 'pingPongBiBi_mech_er.txt')
file_out = os.path.join('mechanisms', 'pingPongBiBi_pattern.txt')

convert_er_mech_to_grasp_pattern(file_in, file_out)


# convert randomdBiBi with competitive inhib
file_in = os.path.join('mechanisms', 'randomBiBiCompInhib_mech_er.txt')
file_out = os.path.join('mechanisms', 'randomBiBiCompInhib_pattern.txt')
inhib_list = ['pyr_c']

convert_er_mech_to_grasp_pattern(file_in, file_out, inhib_list=inhib_list)


# convert orderedBiBi promiscuous reaction with common cofactors and with competitive inhib
file_in = os.path.join('mechanisms', 'orderedBiBiCompInhibPromiscuousCofactors_mech_er.txt')
file_out = os.path.join('mechanisms', 'orderedBiBiCompInhibPromiscuousCofactors_pattern.txt')
inhib_list = ['mltn_c']

convert_er_mech_to_grasp_pattern(file_in, file_out, inhib_list=inhib_list, promiscuous=True)