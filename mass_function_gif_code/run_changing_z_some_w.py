import subprocess
import os


def make_run(ws, z_up_low, how_many_z):
    def save_script_vals(the_w):
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
                 "zmin = {zmin}\n" \
                 "zmax = {zmax}\n" \
                 "nz = {num_z}\n" \
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

        script = script.format(zmin=str(float(z_up_low[0])), zmax=str(float(z_up_low[1])), num_z=how_many_z)
        values = values.format(o_m=0.318, sigma_eight=0.835, w=str(float(the_w)))

        with open('rainbow.ini', 'w') as rainbow:
            rainbow.writelines(script)
        rainbow.close()

        with open('rainbow_values.ini', 'w') as rainbow_values:
            rainbow_values.writelines(values)
        rainbow_values.close()

    og_dir = os.getcwd()
    ls = os.listdir(".")
    for name in ls:
        if "run_changing_z_some_w" not in name:
            subprocess.call("rm -r {dir}".format(dir=name), shell=True)

    number = len(ws)
    for ind in range(0, number):
        dir_name = "rainbow_w{wval}".format(wval=w_vals[ind])
        subprocess.call("mkdir " + dir_name, shell=True)
        os.chdir(dir_name)
        save_script_vals(w_vals[ind])
        subprocess.call("cosmosis rainbow.ini", shell=True)

        os.chdir(og_dir)


if __name__ == "__main__":
    w_vals = [-1, -0.5]
    z_lims = [0.0, 1.0]
    num_z = 80

    datablock = make_run(w_vals, z_lims, num_z)




