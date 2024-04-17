from numba import njit
import numpy as np


from res.getero.reaction_consts.ion_etching_clorine import E_th_Cl_ie

from res.getero.algorithm.silicon_reactions.chlorine import clorine_etching, clorine_ion_etching
from res.getero.algorithm.silicon_reactions.argon import argon_sputtering
from res.getero.algorithm.silicon_reactions.silicon_redepo import Si_redepo, SiCl_redepo, SiCl2_redepo

from res.getero.algorithm.utils import straight_reflection


@njit()
def silicon_reaction(curr_type, curr_counter, prev_counter, curr_farr, prev_farr,
                     Si_num, is_on_horiz, curr_angle, curr_en):
    # Основное вещество (идёт активная реакция)
    if curr_type == 0:
        # радикал Хлора
        if curr_en < E_th_Cl_ie:
            ans = clorine_etching(curr_type, curr_counter, prev_counter, curr_farr,
                               prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)



            return ans
        else:
            ans = clorine_ion_etching(curr_type, curr_counter, prev_counter, curr_farr,
                                   prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)

            return ans
    elif curr_type == 1:
        # атом Ar
        ans = argon_sputtering(curr_type, curr_counter, prev_counter, curr_farr,
                               prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)
        return ans
    elif curr_type == 2:
        # ион Cl_plus
        ans = clorine_ion_etching(curr_type, curr_counter, prev_counter, curr_farr,
                            prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)

        return ans
    elif curr_type == 3:
        # ион Ar_plus
        ans = argon_sputtering(curr_type, curr_counter, prev_counter, curr_farr,
                                  prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)
        return ans
    elif curr_type == 4:
        # Si попытка переосаждения
        print("Si r")
        ans = Si_redepo(curr_type, curr_counter, prev_counter, curr_farr,
                                  prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)
        return ans
    elif curr_type == 5:
        # SiCl попытка переосаждения
        print("SiCl")
        ans = SiCl_redepo(curr_type, curr_counter, prev_counter, curr_farr,
                        prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)
        return ans
    elif curr_type == 6:
        # SiCl2 попытка переосаждения
        print("SiCl2")
        ans = SiCl2_redepo(curr_type, curr_counter, prev_counter, curr_farr,
                        prev_farr, Si_num, is_on_horiz, curr_angle, curr_en)
        return ans
    elif curr_type == 7:
        # SiCl3 попытка переосаждения
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
    elif curr_type == 8:
        # SiCl4 попытка переосаждения
        #print("dsdsdsdsdsds")
        curr_angle = straight_reflection(curr_angle, is_on_horiz)
    return curr_type, curr_counter, prev_counter, curr_farr, prev_farr, False, curr_angle, curr_en, False, np.zeros((6))












