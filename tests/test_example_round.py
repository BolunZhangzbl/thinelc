from thinelc import PyPBFInt, PyPBFFloat
from thinelc.utils import *
import os


abs_path = os.path.abspath(os.path.dirname(__file__))


print("test parse_input_dict: \n")
input_list = [{0: 53.550050047480966, 1: 33.01363408349268, 2: 61.972980420498914, 3: 1.8339520322329905, 4: 67.77103440539256, 5: 61.28221166466044, 6: 40.96954245193537, 7: 42.17715208839638},
              {(0, 1): 50.922441833827484, (0, 2): 48.29428374140523, (0, 3): 16.304298613983843, (0, 4): 26.7858063039301, (0, 5): 36.94719787264254, (0, 6): 31.097918382260808, (0, 7): 66.31425403098898, (1, 2): 40.38463226446161, (1, 3): 14.107357706003627, (1, 4): 47.01796520859973, (1, 5): 41.67551113347407, (1, 6): 44.51336824874781, (1, 7): 24.268650845343622, (2, 3): 16.652134629623426, (2, 4): 48.571888348819655, (2, 5): 49.00708871030495, (2, 6): 45.15410013099699, (2, 7): 32.76469262184217, (3, 4): 17.423346347631973, (3, 5): 17.678357022600807, (3, 6): 15.222460852334763, (3, 7): 13.673449601170976, (4, 5): 43.101354394030785, (4, 6): 40.42664646557161, (4, 7): 51.45737454342285, (5, 6): 44.847491583673744, (5, 7): 43.98744489522803, (6, 7): 49.35242023178369},
              {(0, 1, 2): -61.050387098722055, (0, 1, 3): -12.964050251774069, (0, 2, 3): -18.411384298999195, (1, 2, 3): -14.840138391732765, (0, 1, 4): -63.89328817626969, (0, 2, 4): -90.05025352973708, (1, 2, 4): -69.19303752041611, (0, 1, 5): -60.33151854118164, (0, 2, 5): -84.71836339632053, (1, 2, 5): -67.62545547514429, (0, 1, 6): -51.3359033232485, (0, 2, 6): -73.3179623585048, (1, 2, 6): -54.738382270619525, (0, 1, 7): -54.62127637350625, (0, 2, 7): -70.89820252646483, (1, 2, 7): -65.98948853322833, (0, 3, 4): -19.699216894204042, (1, 3, 4): -14.683045958273592, (0, 3, 5): -18.386094557081968, (1, 3, 5): -14.32432345885027, (0, 3, 6): -15.83262337710559, (1, 3, 6): -11.486117083499924, (0, 3, 7): -15.133873144672453, (1, 3, 7): -14.196480572459237, (0, 4, 5): -89.8951172112273, (1, 4, 5): -67.43611619784382, (0, 4, 6): -78.00611134417963, (1, 4, 6): -55.581459581659075, (0, 4, 7): -72.30136914988898, (1, 4, 7): -64.54994151284671, (0, 5, 6): -73.38268149430988, (1, 5, 6): -53.43427237492106, (0, 5, 7): -69.20007750998825, (1, 5, 7): -63.71997477455261, (0, 6, 7): -57.869148064616084, (1, 6, 7): -50.75692875158062, (2, 3, 4): -20.121706623961437, (2, 3, 5): -19.339249969994846, (2, 3, 6): -15.909231307693194, (2, 3, 7): -18.043112052470725, (2, 4, 5): -91.8425674860936, (2, 4, 6): -77.57499907883141, (2, 4, 7): -81.75605435867254, (2, 5, 6): -73.68945275336645, (2, 5, 7): -80.47242858757379, (2, 6, 7): -64.74248624680838, (3, 4, 5): -19.842603433656276, (3, 4, 6): -16.66118639089147, (3, 4, 7): -17.559246380159347, (3, 5, 6): -15.728590525976042, (3, 5, 7): -17.312731056630753, (3, 6, 7): -13.712920783359007, (4, 5, 6): -77.20432294158203, (4, 5, 7): -78.9863401152727, (4, 6, 7): -64.14136738270854, (5, 6, 7): -62.55432496225944},
              {(0, 1, 2, 3): 5.49370249894142, (0, 1, 2, 4): 33.377841194832286, (0, 1, 2, 5): 30.852230401018296, (0, 1, 2, 6): 25.08119206034913, (0, 1, 2, 7): 27.29580804230298, (0, 1, 3, 4): 5.85274370387655, (0, 1, 3, 5): 5.4074973794919, (0, 1, 3, 6): 4.398524067742315, (0, 1, 3, 7): 4.775632853495953, (0, 1, 4, 5): 32.90832368483933, (0, 1, 4, 6): 26.845017683257296, (0, 1, 4, 7): 28.802650085733923, (0, 1, 5, 6): 24.736798343341192, (0, 1, 5, 7): 26.758187273672554, (0, 1, 6, 7): 21.610274491807083, (0, 2, 3, 4): 9.23057731401039, (0, 2, 3, 5): 8.356041791466541, (0, 2, 3, 6): 6.979173340309215, (0, 2, 3, 7): 6.763273653270826, (0, 2, 4, 5): 52.66725421405863, (0, 2, 4, 6): 44.74156612851084, (0, 2, 4, 7): 40.083268208062, (0, 2, 5, 6): 39.87056921232208, (0, 2, 5, 7): 37.69063117377549, (0, 2, 6, 7): 29.96342397551833, (0, 3, 4, 5): 9.356308963597368, (0, 3, 4, 6): 7.9946192969025205, (0, 3, 4, 7): 6.964184510021258, (0, 3, 5, 6): 7.090307878154192, (0, 3, 5, 7): 6.5620331014539355, (0, 3, 6, 7): 5.2026221711029335, (0, 4, 5, 6): 46.268365821843545, (0, 4, 5, 7): 38.589981738115746, (0, 4, 6, 7): 30.162653757845057, (0, 5, 6, 7): 28.79932173295876, (1, 2, 3, 4): 6.4077759984628315, (1, 2, 3, 5): 6.268164395983777, (1, 2, 3, 6): 4.7306642311293245, (1, 2, 3, 7): 6.7799696589481755, (1, 2, 4, 5): 35.448431179681, (1, 2, 4, 6): 27.569711125475653, (1, 2, 4, 7): 35.58231554238044, (1, 2, 5, 6): 26.228199137532705, (1, 2, 5, 7): 36.4538858360728, (1, 2, 6, 7): 25.866997986752242, (1, 3, 4, 5): 6.164383977218139, (1, 3, 4, 6): 4.811416459257749, (1, 3, 4, 7): 6.129771777731915, (1, 3, 5, 6): 4.566321859567375, (1, 3, 5, 7): 6.242279305439348, (1, 3, 6, 7): 4.465307549303085, (1, 4, 5, 6): 26.851360914714746, (1, 4, 5, 7): 33.49973263923443, (1, 4, 6, 7): 25.08541298061272, (1, 5, 6, 7): 24.4858644946861, (2, 3, 4, 5): 9.058229761023153, (2, 3, 4, 6): 7.292925886318313, (2, 3, 4, 7): 8.253904288108188, (2, 3, 5, 6): 6.76134332226575, (2, 3, 5, 7): 8.234720669250475, (2, 3, 6, 7): 6.054355835363788, (2, 4, 5, 6): 41.23219707799399, (2, 4, 5, 7): 45.27902273943043, (2, 4, 6, 7): 34.313597939364044, (2, 5, 6, 7): 33.286596756618366, (3, 4, 5, 6): 7.279531560160455, (3, 4, 5, 7): 7.826752605313436, (3, 4, 6, 7): 5.943879579143898, (3, 5, 6, 7): 5.7596764318043085, (4, 5, 6, 7): 32.77719050845135}, -1.1314717797145777]
input_list = convert_values(input_list, round_digit=0)
# save_data(input_list, os.path.join(abs_path, "Q_8_matrix_float.pkl"))



# pbf2 = PyPBFFloat()
# pbf2 = parse_input_dict(pbf2, input_list)
# pbf2.shrink()
# pbf2.print()



print("test e2e_pipeline: ")
output_list1, num_newvars = e2e_pipeline(input_list, mode=0, use_int=True, display=True)
print(num_newvars)
print("\n")
