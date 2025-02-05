from __future__ import print_function

import os
import sys
import unittest
from os.path import join as path_join

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pkg_resources
import pytest

import macrodensity as md

try:
    import pandas

    has_pandas = True
except ImportError:
    has_pandas = False


_file_path = os.path.dirname(__file__)


class TestDensityReadingFunctions(unittest.TestCase):
    """Test the code for reading in charge and density files"""

    def test_read_vasp(self):
        """Test the function for reading CHGCAR/LOCPOT"""
        chgcar = pkg_resources.resource_filename(
            __name__, path_join("../tests", "CHGCAR.test")
        )
        charge, ngx, ngy, ngz, lattice = md.read_vasp_density(
            chgcar, quiet=True
        )
        for v, t in (
            (charge, np.ndarray),
            (ngx, int),
            (ngy, int),
            (ngz, int),
            (lattice, np.ndarray),
        ):
            self.assertIsInstance(v, t)
        self.assertEqual(charge[0], -0.76010173913e01)
        self.assertEqual(charge[56 * 56 * 56 - 1], -4.4496715627)
        self.assertEqual(lattice[0, 0], 2.7150000)
        self.assertEqual(ngx, 56)

    def test_read_vasp_parchg(self):
        """Test the function for reading CHGCAR/LOCPOT"""
        parchg = pkg_resources.resource_filename(
            __name__, path_join("../tests", "PARCHG.test")
        )
        spin, ngx, ngy, ngz, lattice = md.read_vasp_parchg(parchg, quiet=True)
        for v, t in (
            (spin, np.ndarray),
            (ngx, int),
            (ngy, int),
            (ngz, int),
            (lattice, np.ndarray),
        ):
            self.assertIsInstance(v, t)
        self.assertEqual(spin[0], 1.0)
        self.assertEqual(lattice[0, 0], 11.721852)

        spin, ngx, ngy, ngz, lattice = md.read_vasp_parchg(
            parchg, spin=True, quiet=True
        )
        for v, t in (
            (spin[0], np.ndarray),
            (ngx, int),
            (ngy, int),
            (ngz, int),
            (lattice, np.ndarray),
        ):
            self.assertIsInstance(v, t)
        for v, t in (
            (spin[1], np.ndarray),
            (ngx, int),
            (ngy, int),
            (ngz, int),
            (lattice, np.ndarray),
        ):
            self.assertIsInstance(v, t)
        self.assertEqual(spin[1][0], 0.0)

    def test_read_gulp(self):
        """Test the function for reading GULP output"""
        gulpcar = pkg_resources.resource_filename(
            __name__, path_join("../tests", "gulp.out")
        )
        potential, ngx, ngy, ngz, lattice = md.read_gulp_potential(gulpcar)
        for v, t in (
            (potential, np.ndarray),
            (ngx, int),
            (ngy, int),
            (ngz, int),
            (lattice, np.ndarray),
        ):
            self.assertIsInstance(v, t)
        self.assertEqual(potential[0], 8.732207)
        self.assertEqual(potential[10 * 10 * 20 - 1], 8.732207)
        self.assertEqual(lattice[0, 0], 11.996500)
        self.assertEqual(ngx, 10)

    def test_density_2_grid(self):
        """Test the function for projecting the potential onto a grid"""
        chgcar = pkg_resources.resource_filename(
            __name__, path_join("../tests", "CHGCAR.test")
        )
        charge, ngx, ngy, ngz, lattice = md.read_vasp_density(
            chgcar, quiet=True
        )
        grid_pot, electrons = md.density_2_grid(charge, ngx, ngy, ngz)
        self.assertAlmostEqual(grid_pot[0, 0, 0], -0.76010173913e01)
        self.assertAlmostEqual(grid_pot[55, 55, 55], -4.4496715627)
        self.assertAlmostEqual(electrons, 8.00000, places=4)


@unittest.skipIf(not has_pandas, "Already using pandas-free reader")
class TestDensityReadingFunctionsNoPandas(TestDensityReadingFunctions):
    """Disable Pandas and test code for reading charge and density files"""

    def setUp(self):
        self._pandas = sys.modules["pandas"]
        sys.modules["pandas"] = None

    def tearDown(self):
        sys.modules["pandas"] = self._pandas


class TestOtherReadingFunctions(unittest.TestCase):

    def test_read_vasp_classic(self):
        """Test the function for reading CHGCAR/LOCPOT"""
        chgcar = pkg_resources.resource_filename(
            __name__, path_join("../tests", "CHGCAR.test")
        )
        (charge, ngx, ngy, ngz, lattice) = md.read_vasp_density_classic(chgcar)
        for v, t in (
            (charge, np.ndarray),
            (ngx, int),
            (ngy, int),
            (ngz, int),
            (lattice, np.ndarray),
        ):
            self.assertIsInstance(v, t)
        self.assertEqual(charge[0], -0.76010173913e01)
        self.assertEqual(charge[56 * 56 * 56 - 1], -4.4496715627)
        self.assertEqual(lattice[0, 0], 2.7150000)
        self.assertEqual(ngx, 56)

    def test_matrix_2_abc(self):
        """Test conversion of lattice to abc, alpha, beta, gamma format"""
        lattice = np.asarray(
            [[2.715, 2.715, 0.0], [0.0, 2.715, 2.715], [2.715, 0.0, 2.715]]
        )
        a, b, c, a_vec, b_vec, c_vec = md.matrix_2_abc(lattice)
        self.assertAlmostEqual(a, 3.8395898218429529)
        self.assertAlmostEqual(b, 3.8395898218429529)
        self.assertAlmostEqual(c, 3.8395898218429529)


class TestAveragingFunctions(unittest.TestCase):
    """Test various functions for manipulating and measuring the density"""

    def test_planar_average(self):
        """Test the code for averaging the density"""
        test_grid = np.zeros(shape=(3, 3, 3))
        for i in range(3):
            test_grid[i, :, 0] = float(i)
        planar = md.planar_average(test_grid, 3, 3, 3)
        self.assertAlmostEqual(planar[0], 1.0)
        planar = md.planar_average(test_grid, 3, 3, 3, axis="x")
        self.assertAlmostEqual(planar[2], 0.66666667)

    def test_volume_average(self):
        """Test the volume_average function"""
        test_grid = np.zeros(shape=(5, 5, 5))
        for i in range(5):
            for j in range(5):
                for k in range(5):
                    test_grid[i, j, k] = float(i * j * k)

        potential, variance = md.volume_average(
            [0, 0, 0], [2, 2, 2], test_grid, 5, 5, 5
        )
        self.assertAlmostEqual(potential, 0.125)
        self.assertAlmostEqual(variance, 0.109375)
        potential, variance = md.volume_average(
            [1, 1, 1], [2, 2, 2], test_grid, 5, 5, 5
        )
        potential, variance = md.volume_average(
            [1, 1, 1], [3, 3, 3], test_grid, 5, 5, 5
        )
        self.assertAlmostEqual(potential, 1.0)
        self.assertAlmostEqual(variance, 3.6296296296296298)

    def test_ipr(self):
        """Test the inverse_participation_ratio function"""

        parchg = pkg_resources.resource_filename(
            __name__, path_join("../tests", "CHGCAR.test")
        )

        dens, ngx, ngy, ngz, lattice = md.read_vasp_density(parchg, quiet=True)
        self.assertAlmostEqual(
            md.utils.inverse_participation_ratio(dens), 1.407e-5
        )

    def test_macroscopic_average(self):
        """Test the macroscopic averaging function"""
        f = 2.0
        fs = 100
        x = np.arange(fs)
        potential = [
            np.sin(2 * np.pi * f * (i / float(fs))) for i in np.arange(fs)
        ]
        macro = md.macroscopic_average(potential, 50, 1)
        self.assertAlmostEqual(macro[20], 0.0)

    def test_spherical_average(self):
        """Tests the spherical_average function"""
        Locpot = pkg_resources.resource_filename(
            __name__, path_join("../tests", "LOCPOT.test")
        )
        out = md.spherical_average(
            cube_size=[2, 2, 2], cube_origin=[0.5, 0.5, 0.5], input_file=Locpot
        )
        self.assertAlmostEqual(out, (6.5579496029375, 1.8665165271901357e-05))

    def test_get_band_extrema(self):
        """Tests the get_band_extrema function"""
        Outcar = pkg_resources.resource_filename(
            __name__, path_join("../tests", "OUTCAR.test")
        )
        out = md.get_band_extrema(input_file=Outcar)
        self.assertEqual(out[0], 2.8952)
        self.assertEqual(out[1], 4.411)


class TestGeometryFunctions(unittest.TestCase):
    """Test the functions that do geometry and trigonometry"""

    def test_gradient_magnitude(self):
        """Test the function for returning the magnitude of gradient at a voxel"""
        grid = np.zeros(shape=(3, 3, 3))
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    grid[i, j, k] = i * j * k
        gx, gy, gz = np.gradient(grid)
        magnitudes = md.gradient_magnitude(gx, gy, gz)
        self.assertEqual(magnitudes[1, 1, 1], 1.7320508075688772)
        self.assertEqual(magnitudes[2, 2, 2], 6.9282032302755088)

    def test_vector_2_abscissa(self):
        """Test the vector_2_abscissa function"""
        abscissa = md.vector_2_abscissa([5, 6, 7], 10, 0.2, 0.2, 0.2)
        self.assertEqual(abscissa[5], 10.488088481701517)

    def test_number_in_field(self):
        """Test the number_in_field function"""
        test_field = np.zeros(shape=(5, 5, 5))
        test_field[0, 0, 0] = 1.0
        test_field[4, 4, 4] = 1.0
        test_field[2, 3, 2] = 0.5
        test_field[1, 4, 2] = 0.3
        self.assertEqual(md.number_in_field(test_field, 0.3), 4)
        self.assertEqual(md.number_in_field(test_field, 0.5), 3)
        self.assertEqual(md.number_in_field(test_field, 1.0), 2)
        self.assertEqual(md.number_in_field(test_field, 1.1), 0)

    def test_element_vol(self):
        """Test the element_vol function"""
        self.assertEqual(md.element_vol(3000.0, 10, 20, 30), 0.5)

    def test_get_volume(self):
        """Test the get_volume function"""
        a = [5.43 * 0.5, 0.0, 5.43 * 0.5]
        b = [5.43 * 0.5, 5.43 * 0.5, 0.0]
        c = [0.0, 5.43 * 0.5, 5.43 * 0.5]
        self.assertAlmostEqual(md.get_volume(a, b, c), 40.03, places=2)

    def test_numbers_2_grid(self):
        """Tests the numbers_2_grid function"""
        a = md.numbers_2_grid([0.5, 0.5, 0.5], 10, 10, 10)
        b = [5, 5, 5]
        self.assertSequenceEqual(a.tolist(), b)

    def test_GCD(self):
        """Test the GCD function"""
        self.assertEqual(md.GCD(100, 12), 4)

    def test_GCD_List(self):
        """Tests the GCD_List function"""
        self.assertEqual(md.GCD_List([15, 100, 45]), 5)


class TestConvenienceFunctions(unittest.TestCase):

    def test_bulk_interstitial_alignment(self):
        """Tests the bulk_interstitial_alignment function"""
        Locpot = pkg_resources.resource_filename(
            __name__, path_join("../tests", "LOCPOT.test")
        )
        Outcar = pkg_resources.resource_filename(
            __name__, path_join("../tests", "OUTCAR.test")
        )
        out = md.bulk_interstitial_alignment(
            interstices=([0.5, 0.5, 0.5], [0.25, 0.25, 0.25]),
            outcar=Outcar,
            locpot=Locpot,
            cube_size=[2, 2, 2],
        )
        self.assertEqual(
            out,
            (-3.24, -1.72, [1.8665165271901357e-05, 6.277207757909537e-06]),
        )

    def test_moving_cube(self):
        """Tests the moving_cube function"""
        Locpot = pkg_resources.resource_filename(
            __name__, path_join("../tests", "LOCPOT.test")
        )
        _ = md.plotting.plot_variation_along_vector(
            cube_size=[1, 1, 1],
            vector=[1, 1, 1],
            origin_point=[0.17, 0.17, 0.17],
            vector_magnitude=16,
            input_file=Locpot,
            output_file="potential_variation.csv",
        )
        df = pd.read_csv("potential_variation.csv")
        out = df.Potential.tolist()
        self.assertAlmostEqual(out[0], 3.99827598)
        self.assertAlmostEqual(out[10], 6.53774638)
        self.assertAlmostEqual(out[-1], 3.97265811)
        self.addCleanup(os.remove, "potential_variation.csv")
        self.addCleanup(os.remove, "potential_variation.png")


class TestPlottingFunctions(unittest.TestCase):

    def test_plot_planar_average(self):
        """Tests the plot_planar_average function"""
        locpot = pkg_resources.resource_filename(
            __name__, path_join("../tests", "LOCPOT.test")
        )
        df, fig = md.plot_planar_average(
            lattice_vector=5.41, input_file=locpot
        )
        self.assertAlmostEqual(df["Planar"].tolist()[0], 0.14555565)
        self.assertAlmostEqual(df["Planar"].tolist()[10], 4.61454537)
        self.assertAlmostEqual(df["Planar"].tolist()[-1], -0.87290696)
        self.addCleanup(os.remove, "planar_average.csv")
        self.addCleanup(os.remove, "planar_average.png")

    def test_plot_on_site_potential(self):
        """Tests the plot_on_site_potential function"""
        locpot = pkg_resources.resource_filename(
            __name__, path_join("../tests", "LOCPOT.test")
        )
        poscar = pkg_resources.resource_filename(
            __name__, path_join("../tests", "POSCAR.test")
        )
        df = md.plot_on_site_potential(
            species="Zn",
            sample_cube=[5, 5, 5],
            potential_file=locpot,
            coordinate_file=poscar,
        )[0]
        self.assertEqual(df.Potential.tolist(), [-6.545211257074241])
        self.addCleanup(os.remove, "OnSitePotential.csv")
        self.addCleanup(os.remove, "OnSitePotential.png")

    def test_plot_gulp_potential(self):
        """Tests the plot_gulp_potential function"""
        gulpcar = pkg_resources.resource_filename(
            __name__, path_join("../tests", "gulp.out")
        )
        df, fig = md.plot_planar_average(
            lattice_vector=3.0,
            input_file=gulpcar,
            output_file="GulpPotential.csv",
            img_file="GulpPotential.png",
        )
        planar = df["Planar"].dropna()
        self.assertEqual(planar.tolist()[0], -23.16678352)
        self.assertAlmostEqual(planar.tolist()[10], -1.59508152)
        self.assertAlmostEqual(planar.tolist()[-1], -23.16678352)
        self.addCleanup(os.remove, "GulpPotential.csv")
        self.addCleanup(os.remove, "GulpPotential.png")

    def test_plot_active_space(self):
        """Tests the plot_active_space function"""
        Locpot = pkg_resources.resource_filename(
            __name__, path_join("../tests", "LOCPOT.test")
        )
        dict_output = md.tools._find_active_space(
            cube_size=[2, 2, 2],
            cube_origin=[0.5, 0.5, 0.5],
            tolerance=1e-4,
            input_file=Locpot,
        )
        vacuum, non_vacuum = dict_output["Vacuum"], dict_output["Non-vacuum"]
        self.assertEqual((len(vacuum), len(non_vacuum)), (17, 4079))

    def test_plot_planar_cube(self):
        """Tests the plot_planar_average function"""
        density = pkg_resources.resource_filename(
            __name__, path_join("../tests", "cube_001_spin_density.cube")
        )
        potential = pkg_resources.resource_filename(
            __name__, path_join("../tests", "cube_002_hartree_potential.cube")
        )
        dfden, _ = md.plot_planar_average(
            input_file=density, lattice_vector=4.75
        )
        dfpot, _ = md.plot_planar_average(
            input_file=potential, lattice_vector=4.75
        )
        self.assertEqual(dfden["Planar"].tolist()[0], 0.0200083723051778)
        self.assertEqual(dfden["Planar"].tolist()[-1], 0.019841719274268536)
        self.assertEqual(dfpot["Planar"].tolist()[0], -0.562656062923066)
        self.assertEqual(dfpot["Planar"].tolist()[-1], -0.581089179258661)
        self.addCleanup(os.remove, "planar_average.csv")
        self.addCleanup(os.remove, "planar_average.png")


    @pytest.mark.mpl_image_compare(
        baseline_dir=f"{_file_path}/testIm",
        filename="BandAlignment.png",
        style=f"{_file_path}/../macrodensity/macrodensity.mplstyle",
        savefig_kwargs={"transparent": True, "bbox_inches": "tight"},
    )
    def test_energy_band_alignment_diagram(self):
        """Tests the energy_band_alignment_diagram function"""
        fig = md.energy_band_alignment_diagram(
            {
                "ZnO": [4.4, 7.7],
                "MOF-5": [2.7, 7.3],
                "HKUST-1": [5.1, 6.0],
                "ZIF-8": [0.9, 6.4],
                "COF-1M": [1.3, 4.7],
                "CPO-27-Mg": [2.9, 5.9],
                "MIL-125": [3.8, 7.6],
                "TiO2": [4.8, 7.8],
            },
            ylims=(-10, 0.0),
            arrowhead=0.15,
            fig_format='png'
        )

        if os.path.exists("BandAlignment.png"):
            self.addCleanup(os.remove, "BandAlignment.png")
        return fig

if __name__ == "__main__":
    unittest.main()
