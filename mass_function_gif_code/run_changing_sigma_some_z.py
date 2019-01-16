import subprocess
import os
import numpy as np


def make_run(sigma_lims, num_sig):
    def save_script_vals(sigma_8):
        script = "[runtime]\n" \
                 "sampler = test\n" \
                 "[test]\n" \
                 "save_dir=results_rainbow\n" \
                 "fatal_errors=T\n" \
                 "[pipeline]\n" \
                 "modules = consistency camb rescale mf_tinker\n" \
                 "values =rainbow_values.ini\n" \
                 "[consistency]\n" \
                 "file = cosmosis-standard-library/utility/consistency/consistency_interface.py\n" \
                 "[rescale]\n" \
                 "file = cosmosis-standard-library/utility/sample_sigma8/sigma8_rescale.py\n" \
                 "[camb]\n" \
                 "file = cosmosis-standard-library/boltzmann/camb/camb.so\n" \
                 "mode=all\n" \
                 "lmax=2500\n" \
                 "feedback=0\n" \
                 "zmin = 0.0\n" \
                 "zmax = 1.0\n" \
                 "nz = 2\n" \
                 "[mf_tinker]\n" \
                 "file = cosmosis-standard-library/mass_function/mf_tinker/tinker_mf_module.so\n" \
                 "redshift_zero = 0\n" \
                 "feedback=0\n"

        values = "[cosmological_parameters]\n" \
                 "h0 = 0.7       ;H0 (km/s/Mpc)/100.0km/s/Mpc\n" \
                 "omega_m = {o_m}  ;density fraction for matter today\n" \
                 "omega_b = 0.04    ;density fraction for baryons today\n" \
                 "omega_k = 0.0     ;spatial curvature\n" \
                 "sigma8_input = {sigma_eight}\n" \
                 ";helium\n" \
                 "yhe = 0.245341  ;helium mass fraction\n" \
                 ";reionization\n" \
                 "tau = 0.08      ;reionization optical depth\n" \
                 ";inflation Parameters\n" \
                 "n_s = 0.96      ;scalar spectral index\n" \
                 "A_s = 2.1e-9    ;scalar spectrum primordial amplitude\n" \
                 "k_s = 0.05      ;Power spectrum pivot scale\n" \
                 "n_run = 0.0     ;running of scalar spectrum\n" \
                 ";r_t = 0.0       ;tensor to scalar ratio\n" \
                 ";n_t = 0.0       ;tensor spectral index\n" \
                 ";dark energy equation of state\n" \
                 "w = {w}   ;equation of state of dark energy\n" \
                 "wa = 0.0   ;equation of state of dark energy (redshift dependency)\n"

        values = values.format(o_m=0.318, sigma_eight=sigma_8, w=str(float(-1.0)))

        with open('rainbow.ini', 'w') as rainbow:
            rainbow.writelines(script)
        rainbow.close()

        with open('rainbow_values.ini', 'w') as rainbow_values:
            rainbow_values.writelines(values)
        rainbow_values.close()

    og_dir = os.getcwd()
    ls = os.listdir(".")
    for name in ls:
        if "run_changing_sigma_some_z" not in name:
            subprocess.call("rm -r {dir}".format(dir=name), shell=True)

    sigma_space = np.linspace(sigma_lims[0], sigma_lims[1], num_sig)
    for ind in range(0, len(sigma_space)):
        dir_name = "rainbow_sigma{sig_val}".format(sig_val=sigma_space[ind])
        subprocess.call("mkdir " + dir_name, shell=True)
        os.chdir(dir_name)
        save_script_vals(sigma_space[ind])
        subprocess.call("cosmosis rainbow.ini", shell=True)

        os.chdir(og_dir)


if __name__ == "__main__":
    sigma_lims = [0.5, 0.9]
    num_sig = 100
    make_run(sigma_lims, num_sig)




