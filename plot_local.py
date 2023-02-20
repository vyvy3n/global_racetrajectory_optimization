import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


DPI = 300
LINEWIDTH = 0.7

# To plot full track, use plot params below
DPI = 2000
LINEWIDTH = 0.1

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# csv_data_temp = np.loadtxt('outputs/traj_race_cl.csv', comments='#', delimiter=';')
# print(csv_data_temp.shape)
traj_race = pd.read_csv('outputs/traj_race_cl.csv', skiprows = 2, sep = "; ")
traj_race = traj_race.rename(columns={'# s_m': 's_m'})
print(traj_race.head())

traj_ltpl = pd.read_csv('outputs/traj_ltpl_cl.csv', skiprows = 2, sep = "; ")
traj_ltpl = traj_ltpl.rename(columns={'# x_ref_m': 'x_ref_m'})
print(traj_ltpl.head())
print(traj_ltpl.columns)

# calculate boundaries
# x_ref_m; y_ref_m; width_right_m; width_left_m; x_normvec_m; y_normvec_m;
trajectory = traj_race[['x_m', 'y_m']].to_numpy()
reftrack = traj_ltpl[['x_ref_m', 'y_ref_m']].to_numpy()
normvec_normalized_interp = traj_ltpl[['x_normvec_m', 'y_normvec_m']].to_numpy()
bound1 = reftrack + normvec_normalized_interp * np.expand_dims(traj_ltpl['width_right_m'], 1)
bound2 = reftrack - normvec_normalized_interp * np.expand_dims(traj_ltpl['width_left_m'], 1)



x_range = (
	min(np.hstack([bound1[:, 0], bound2[:, 0]])),
	max(np.hstack([bound1[:, 0], bound2[:, 0]])))
y_range = (
	min(np.hstack([bound1[:, 1], bound2[:, 1]])),
	max(np.hstack([bound1[:, 1], bound2[:, 1]])))
print("x range:", x_range)
print("y range:", y_range)


plots_path = 'plots-local'
if not os.path.exists(plots_path):
	os.mkdir(plots_path)

plt.figure()
plt.plot(reftrack[:, 0], reftrack[:, 1], "k--", linewidth = LINEWIDTH)
plt.plot(bound1[:, 0], bound1[:, 1], "k-", linewidth = LINEWIDTH)
plt.plot(bound2[:, 0], bound2[:, 1], "k-", linewidth = LINEWIDTH)
plt.plot(trajectory[:, 0], trajectory[:, 1], "r-", linewidth = LINEWIDTH)

plt.grid()
ax = plt.gca()
ax.set_aspect("equal", "datalim")
plt.xlabel("east in m")
plt.ylabel("north in m")

# Local Plot
# plt.xlim([50, 150])
# plt.ylim([900, 1100])

plt.savefig(os.path.join(plots_path, "traj_race_plus_track.png"), dpi = DPI)