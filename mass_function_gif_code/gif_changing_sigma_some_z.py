import os
import numpy as np
from matplotlib import pyplot as plt
import subprocess
import imageio
import sys


def extract(base_dir):
    def extract_cosmo_par(inner_dict):
        os.chdir('temporary_storage/cosmological_parameters')
        with open('values.txt') as cosmo_par:
            for line in cosmo_par.readlines():
                if "omega_m" in line:
                    inner_dict['omega_m'] = line.split("=")[-1].strip()
                elif "sigma_8" in line:
                    inner_dict['sigma_8'] = line.split("=")[-1].strip()
        cosmo_par.close()
        os.chdir(og_dir)
        return inner_dict

    def extract_mass_func(inner_dict):
        os.chdir('temporary_storage/mass_function')
        dndlnmh = np.loadtxt('dndlnmh.txt')
        masses = np.loadtxt('m_h.txt')
        redshifts = np.loadtxt('z.txt')
        inner_dict["dndlnmh"] = dndlnmh
        inner_dict["masses"] = masses
        inner_dict["redshifts"] = redshifts
        os.chdir(og_dir)
        return inner_dict

    og_dir = os.getcwd()
    os.chdir(base_dir)
    ls = os.listdir()
    os.chdir(og_dir)
    sigma_vals = [name.split('sigma')[-1] for name in ls if "rainbow_sigma" in name]

    result_dict = {}
    for val in sigma_vals:
        inner_dict = {}
        subprocess.call("cp -r {base_dir}/rainbow_sigma{sigma}/results_rainbow/mass_function temporary_storage/".
                        format(base_dir=base_dir, sigma=val), shell=True)
        subprocess.call("cp -r {base_dir}/rainbow_sigma{sigma}/results_rainbow/cosmological_parameters temporary_storage/".
                        format(base_dir=base_dir, sigma=val), shell=True)

        inner_dict = extract_cosmo_par(inner_dict)
        inner_dict = extract_mass_func(inner_dict)
        result_dict[val] = inner_dict
        subprocess.call("rm -r {top_dir}/temporary_storage".format(top_dir=og_dir), shell=True)
        subprocess.call("mkdir {top_dir}/temporary_storage".format(top_dir=og_dir), shell=True)

    return result_dict


def make_images(data):
    subprocess.call("rm -r sigma_images/", shell=True)
    subprocess.call("mkdir sigma_images", shell=True)
    name = "_sigma8_range"
    color_dict = {"0.0": 'red', "1.0": 'black'}

    sigma_list = [float(el) for el in data]
    sigma_list.sort()

    i = 0
    for s in sigma_list:
        el = str(s)
        masses = data[el]['masses']
        dndlnmh = data[el]['dndlnmh']
        redshifts = data[el]['redshifts']

        plt.figure(i)
        plt.rc('xtick', labelsize='small')
        plt.rc('ytick', labelsize='small')
        plt.xlabel('$M_{200m}$ [$M_{\odot}/h$]')
        plt.ylabel('d$n$/dln$M$ [$h^3Mpc^{-3}$]')
        plt.xscale('log')
        plt.yscale('log')
        plt.minorticks_on()
        plt.tick_params(axis='both', direction='in', which='both', top=True, right=True)
        plt.grid(linestyle='dotted', linewidth=1)
        plt.ylim([10e-9, 10e-4])
        plt.xlim([10e+12, 10e+15])

        for x in range(0, len(redshifts)):
            z = redshifts[x]
            plt.plot(masses, dndlnmh[x], label=r"$\Omega_m={m}, \sigma_8={sig}, z={z}$".
                     format(z='{:.2f}'.format(round(z, 2)), sig='{:.3f}'.format(round(float(data[el]['sigma_8']), 3)),
                            m=data[el]['omega_m']), color=color_dict[str(z)])
            plt.legend(bbox_to_anchor=(0.885, 1.05, 0.2, 0.2), loc=0, borderaxespad=3)

        plt.savefig("sigma_images/step{ind}{comb_w}.png".format(ind=i, comb_w=name))
        plt.close(i)

        i += 1
    images = [imageio.imread("sigma_images/step{ind}{comb_w}.png".format(ind=i, comb_w=name))
              for i in range(0, len(data))]
    imageio.mimsave("animations/massf{comb_w}.gif".format(comb_w=name), images)


if __name__ == "__main__":
    datablock = extract("/home/dt237/software/cosmosis-docker/cosmosis/rainbows/changing_sigma_some_z")
    make_images(datablock)


