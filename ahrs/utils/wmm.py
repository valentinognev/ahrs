"""
World Magnetic Model
====================

The main utility of the World Magnetic Model (WMM) [WMM]_ is to provide
magnetic declination for any desired location on the globe.

In addition to the magnetic declination, the WMM also provides the complete
geometry of the field from 1 km below the World Geodetic System (WGS 84)
[WGS84]_ ellipsoid surface to approximately 850 km above it. The magnetic field
extends deep into the Earth and far out into space, but the WMM is not valid at
these extremes.

Earth's magnetic field is viewed as a magnetic dipole produced by a sphere of
uniform magnetization. The "south" of the dipole lies on the northern
Hemipshere and drifts westward at about 55 to 60 km per year, whereas the other
pole, just outside the Antarctic Circle, drifts by about 10 to 15 km per year.

The strongest contribution to Earth's magnetism is the magnetic field produced
by the Earth's liquid-iron outer core, called the "core field". Magnetic
minerals in the crust and upper mantle make a further contribution that can be
locally significant. All these fields of "internal" origin and their large
scale components are included in the WMM.

"External" magnetic fields, arising from electric currents in the upper
atmosphere and near-Earth space, predominantly generated by solar wind, are
time-varying and produce secondary magnetic fields, which are not represented
in the WMM.

Current estimations include secondary thermal convection currents near Earth's
core-mantle producing local magnetic dipoles. These dipoles are superimposed to
approximate the observed multipole nature of the magnetic field. The creation
and decay of these inner convections are suspected to yield the magnetic drift.

The magnetic flux density (magnetic field) :math:`B` can be expressed as the
gradient of a potential, :math:`V`:

.. math::
    B = -\\nabla V

This has a convenient solution expressed in spherical harmonics of :math:`n`
degrees:

.. math::
    V(r, \\theta, \\phi) = a \\sum_{n=1}^k\\Big(\\frac{a}{r}\\Big)^{n+1}\\sum_{m=0}^{n}\\big(g_n^m \\cos(m\\phi) + h_n^m \\sin(m\\phi)\\big) P_n^m(\\theta)

where :math:`a` is Earth's mean radius; :math:`g_n^m` and :math:`h_n^m` are
*Gaussian coefficients* of degree :math:`n` and order :math:`m`; :math:`r`,
:math:`\\theta`, and :math:`\\phi` are the geocentric radius, coelevation and
longitude in spherical polar coordinates; and :math:`P_n^m(\\theta)` are the
associated Legendre functions [Heiskanen]_.

The time-dependent Gauss coefficients are estimated empirically from a
least-squares fit using satellite magnetic measurements [Langel]_. These
coefficients are provided by the NCEI Geomagnetic Modeling Team and British
Geological Survey in a file with extension COF [WMM2020]_.

With degree :math:`n=1` only dipoles are considered. For :math:`n=2` the
quadrupoles, :math:`n=3` the octuploles, and so on. The method of this WMM
expands to *degree* and *order* 12.

The secular variation (SV) is the yearly change of the core field, which is
also accounted in the WMM by a linear model. Due to unpredictable changes in
the core field, the values of the WMM coefficients are updated every five
years (a lustrum). The most recent version is valid from 2020 to 2024.

The geomagnetic field vector B is described by 7 elements:

+---------+-----------------------------------------------+--------+----------------+
|         |                                               |        | Range          |
| Element | Definition                                    | Units  +--------+-------+
|         |                                               |        | Min    | Max   |
+=========+===============================================+========+========+=======+
| X       | Northerly intensity                           | nT     | -17000 | 43000 |
+---------+-----------------------------------------------+--------+--------+-------+
| Y       | Easterly intensity                            | nT     | -18000 | 17000 |
+---------+-----------------------------------------------+--------+--------+-------+
| Z       | Vertical intensity (Positive downwards)       | nT     | -67000 | 62000 |
+---------+-----------------------------------------------+--------+--------+-------+
| H       | Horizontal intensity                          | nT     |      0 | 43000 |
+---------+-----------------------------------------------+--------+--------+-------+
| F       | Total intensity                               | nT     |  23000 | 67000 |
+---------+-----------------------------------------------+--------+--------+-------+
| I       | Inclination angle (a.k.a. dip angle)          | degree |    -90 | 90    |
+---------+-----------------------------------------------+--------+--------+-------+
| D       | Declination angle (a.k.a. magnetic variation) | degree |   -180 | 180   |
+---------+-----------------------------------------------+--------+--------+-------+

The quantities ``X``, ``Y`` and ``Z`` are perpendicular vectors and can be used
to determine the quantities ``F``, ``I`` and ``D``, and viceversa.

The vertical direction is perpendicular to the horizontal plane of the WGS 84
ellipsoid model of the Earth.

At a location on the plane of a chosen horizontal coordinate system,
**grivation** is the angle between grid north and magnetic north, i.e., the
angle measured clockwise from the direction parallel to the grid's Northing
axis to the horizontal component of the magnetic field at the observer's
location.

Grivation is useful for local surveys, where location is given by grid
coordinates rather than by longitude and latitude. It is dependent on the map
projection used to define the grid coordinates. In general, it is estimated as:

.. math::
    GV = D - C

where :math:`C` is the "convergence-of-meridians" defined as the clockwise
angle from the northward meridional arc to the grid Northing direction.

The class ``WMM`` contains a couple of methods to load and create a geomagnetic
model from a set of given coefficients. To obtain the magnetic elements at a
certain spot on the Earth, we call the method ``magnetic_field``

.. code:: python

    >>> wmm = ahrs.utils.WMM()              # Create today's magnetic model
    >>> wmm.magnetic_field(10.0, -20.0)     # Magnetic field at latitude = 10°, longitude = -20°
    >>> wmm.D                               # Magnetic declination [degrees]
    -9.122361367239034
    >>> wmm.magnetic_field(10.0, -20.0, height=10.5)     # 10.5 km above sea level
    >>> wmm.D
    -9.128404039098971

By default, the class ``WMM`` will create a model for the day, when the object
is being created. To ask for the values at a different date, we simply pass it
as a parameter.

.. code:: python

    >>> wmm.magnetic_field(10.0, -20.0, height=10.5, date=datetime.date(2017, 5, 12))    # on 12th May, 2017
    >>> wmm.D
    -9.73078560629778

All main elements are computed at the same time and accessed independently

.. code:: python

    >>> wmm.X
    30499.640469609083
    >>> wmm.Y
    -5230.267158472566
    >>> wmm.Z
    -1716.633311360368
    >>> wmm.H
    30944.850352270452
    >>> wmm.F
    30992.427998627096
    >>> wmm.I
    -3.1751692563622993
    >>> wmm.GV
    -9.73078560629778

or in a dictionary

.. code:: python

    >>> wmm.magnetic_elements
    {'X': 30499.640469609083, 'Y': -5230.267158472566, 'Z': -1716.633311360368,
    'H': 30944.850352270452, 'F': 30992.427998627096, 'I': -3.1751692563622993,
    'D': -9.73078560629778, 'GV': -9.73078560629778}

.. note::
    The model in this package includes coefficients for dates between **2015**
    and **2024** only. Models out of this timespan cannot be built.

The WMM was developed jointly by the National Centers for Environmental
Information (NCEI, Boulder CO, USA) (formerly National Geophysical Data Center
(NGDC)) and the British Geological Survey (BGS, Edinburgh, Scotland). As part
of the regular update cycle of the World Magnetic Model both institutions have
released the latest model on December 10th, 2019.

This script is based on the originally conceived one by Christopher Weiss
(cmweiss@gmail.com) [Weiss]_, who adapted it from the geomagc software and
World Magnetic Model of the NOAA Satellite and Information Service, National
Geophysical Data Center [Chulliat]_.

License
-------
The WMM source code and binaries are in the public domain and not licensed or
under copyright. The information and software may be used freely by the public.
As required by 17 U.S.C. 403, third parties producing copyrighted works
consisting predominantly of the material produced by U.S. government agencies
must provide notice with such work(s) identifying the U.S. Government material
incorporated and stating that such material is not subject to copyright
protection.

References
----------
.. [Chulliat] Chulliat, A., W. Brown, P. Alken, C. Beggan, M. Nair, G. Cox, A.
    Woods, S. Macmillan, B. Meyer and M. Paniccia, The US/UK World Magnetic
    Model for 2020-2025: Technical Report, National Centers for Environmental
    Information, NOAA, doi:10.25923/ytk1-yx35, 2020.
    (https://www.ngdc.noaa.gov/geomag/WMM/data/WMM2020/WMM2020_Report.pdf)
.. [Heiskanen] W. A. Heiskanen and H. Moritz. Physical Geodesy. TU Graz. 1993.
.. [Langel] R. A. Langel and W. J. Hinze. The Magnetic Field of Earth's
    Lithosphere: The Satellite Perspective. Cambridge University Press. 1998.
.. [Weiss] Christopher Weiss' GeoMag repository (https://github.com/cmweiss/geomag)
.. [Wertz] James R. Wertz. Spacecraft Attitude Determination and Control.
    Kluwer Academics. 1978.
.. [WGS84] World Geodetic System 1984. Its Definition and Relationships with
    Local Geodetic Systems. National Geospatial-Intelligence Agency (NGA)
    Standarization Document. 2014.
    ftp://ftp.nga.mil/pub2/gandg/website/wgs84/NGA.STND.0036_1.0.0_WGS84.pdf
.. [WMM] The World Magnetic Model (https://www.ngdc.noaa.gov/geomag/WMM/DoDWMM.shtml)
.. [WMM2020] WMM2020 Model values: NCEI Geomagnetic Modeling Team and British
    Geological Survey. 2019. World Magnetic Model 2020. NOAA National Centers
    for Environmental Information. doi: 10.25921/11v3-da71, 2020.

"""

# PSL
import datetime
import pkgutil
from io import StringIO
from typing import Union, Tuple, Dict
# Third-Party Dependencies
import numpy as np
from ..common.constants import *
from ..common.frames import ned2enu

def geodetic2spherical(lat: float, lon: float, h: float, a: float = EARTH_EQUATOR_RADIUS/1000.0, b: float = EARTH_POLAR_RADIUS/1000.0) -> Tuple[float, float, float]:
    """
    Transform geodetic coordinates into spherical geocentric coordinates

    The transformation cannot be a simple cylindric to spherical conversion, as
    we must also consider a planet's ellipsoid form. With the aid of its
    pre-defined flatness and eccentricity, we can better approximate the values
    of the conversion.

    In this function the Earth's major and minor semi-axis are considered.
    However, we can convert the coordinates of different ellipsoidal bodies, by
    giving the dimensions of its semi-axes.

    Notice that the longitude between both systems remains the same.

    Parameters
    ----------
    lat : float
        Latitude, in radians, of point in geodetic coordinates
    lon : float
        Longitude, in radians, of point in geodetic coordinates
    h : float
        Height, in kilometers, of point in geodetic coordinates
    a : float, default: 6378.137
        Major semi-axis, in kilometers. Defaults to Earth's equatorial radius
    b : float, default: 6356.752314245
        Minor semi-axis, in kilometers. Defaults to Earth's polar radius

    Returns
    -------
    lat_spheric : float
        Latitude of point in spherical coordinates.
    lon : float
        Longitue of point in spherical coordinates. Same as geodetic.
    r : float
        Radial distance of point in spherical coordinates.
    """
    # Estimate Spheroid's Flatness and First Eccentricity
    f = (a-b)/a                             # Flatness
    e2 = f*(2.0-f)                          # First Eccentricity
    # Transform geodetic coordinates into spherical geocentric coordinates
    Rc = a/np.sqrt(1.0-e2*np.sin(lat)**2)   # Radius of curvature of prime vertical
    rho = (Rc+h)*np.cos(lat)
    z = (Rc*(1-e2)+h)*np.sin(lat)
    r = np.linalg.norm([rho, z])            # Radial distance
    lat_spheric = np.arcsin(z/r)            # Spherical latitude
    return lat_spheric, lon, r

class WMM:
    """
    World Magnetic Model

    It is mainly used to compute all elements of the World Magnetic Model (WMM)
    at any given point on Earth.

    The main magnetic field :math:`B` is a potential field defined, in
    geocentric spherical coordinates (longitude :math:`\\lambda`, latitude
    :math:`\\phi '` and radius :math:`r`), as the negative spatial gradient of a
    scalar potential at a time :math:`t`. This potential can be expanded in
    terms of spherical harmonics:

    .. math::
        V(\\lambda, \\phi', r, t) = a\\sum_{n=1}^{N}\\Big(\\frac{a}{r}\\Big)^{n+1}\\sum_{m=0}^{n}f(n, m, \\lambda, t)P_n^m(\\phi')

    where

    .. math::
        f(n, m, \\lambda, t) = g_n^m(t) \\cos(m\\lambda) + h_n^m(t) \\sin(m\\lambda)

    and the Schmidt semi-normalized associated Legendre functions :math:`P_n^m(\\phi')`
    are defined as:

    .. math::
        P_n^m(\\mu) = \\left\\{
        \\begin{array}{ll}
            \\sqrt{2\\frac{(n-m)!}{(n+m)!}}P_{n, m}(\\mu) & \\mathrm{if} \; m > 0 \\\\
            P_{n, m}(\\mu) & \\mathrm{if} \; m = 0
        \\end{array}
        \\right.

    Any object of this class is initialized with the corresponding epoch,
    determined by the given date. If no date is given, it is assumed for the
    day of the object's creation.

    Once the WMM object is created, the estimation of the geomagnetic elements
    is carried out with a call to the method `magnetic_field` giving the
    location on Earth at which the magnetic elements will be calculated. This
    location is given in decimal geodetic coordinates. See examples.

    Every WMM object is created with a set of coefficients read from a COF
    file, defined by the desired working date of the model. The latest
    model available is WMM2020 corresponding to the lustrum 2020-2024.

    This class can create models with dates between 2015 and 2024.

    Parameters
    ----------
    date : datetime.date, int or float, default: current day
        Date of desired magnetic field estimation.
    latitude : float, default: None
        Latitude, in decimal degrees, in geodetic coordinates.
    longitude : float, default: None
        Longitude, in decimal degrees, in geodetic coordinates.
    height : float, default: 0.0
        Mean Sea Level Height, in kilometers.
    frame : str, default: 'NED'
        Local tangent plane coordinate frame. Valid options are right-handed
        ``'NED'`` for North-East-Down and ``'ENU'`` for East-North-Up.

    Attributes
    ----------
    date : datetime.date, default: datetime.date.today()
        Desired date to estimate
    date_dec : float
        Desired date to estimate as decimal
    epoch : float
        Initial time of model in decimal years
    model : str
        WMM Model identificator
    modeldate : str
        Release date of WMM Model
    wmm_filename : str
        COF File used to build Model
    degree : int
        Degree of model
    latitude : float
        Latitude, in decimal degrees, in geodetic coordinates
    longitude : float
        Longitude in decimal degrees, in geodetic coordinates
    height : float, default: 0.0
        Mean Sea Level Height in kilometers
    X : float, default: None
        Northerly intensity, in nT
    Y : float, default: None
        Easterly intensity, in nT
    Z : float, default: None
        Vertical intensity, in nT
    H : float, default: None
        Horizontal intensity, in nT
    F : float, default: None
        Total intensity, in nT
    I : float, default: None
        Inclination angle (dip), in degrees
    D : float, default: None
        Declination angle, in degrees
    GV : float, default: None
        Grivation, in degrees

    Examples
    --------
    The magnetic field can be computed at the creation of the WMM object by
    passing the main parameters to its constructor:

    >>> wmm = ahrs.utils.WMM(datetime.date(2017, 5, 12), latitude=10.0, longitude=-20.0, height=10.5)
    >>> wmm.magnetic_elements
    {'X': 30499.640469609083, 'Y': -5230.267158472566, 'Z': -1716.633311360368,
    'H': 30944.850352270452, 'F': 30992.427998627096, 'I': -3.1751692563622993,
    'D': -9.73078560629778, 'GV': -9.73078560629778}

    """
    def __init__(self,
                 date: Union[datetime.date, int, float] = None,
                 latitude: float = MUNICH_LATITUDE,
                 longitude: float = MUNICH_LONGITUDE,
                 height: float = MUNICH_HEIGHT,
                 frame: str = 'NED') -> None:
        self.reset_coefficients(date)
        self.__dict__.update(dict.fromkeys(['X', 'Y', 'Z', 'H', 'F', 'I', 'D', 'GV']))
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.height: float = height
        self.frame: str = frame
        self._guard_clauses()
        if all([self.latitude, self.longitude]):
            self.magnetic_field(self.latitude, self.longitude, self.height, date=self.date)

    def _guard_clauses(self):
        for item in ['latitude', 'longitude', 'height']:
            if not isinstance(self.__getattribute__(item), (int, float)):
                raise TypeError(f"{item} must be int or float. Got {type(self.__getattribute__(item))}")
        if not isinstance(self.frame, str):
            raise TypeError(f"frame must be str. Got {type(self.frame)}")
        if abs(self.latitude) > 90:
            raise ValueError(f"Latitude must be between -90 and 90. Got {self.latitude}")
        if abs(self.longitude) > 180:
            raise ValueError(f"Longitude must be between -180 and 180. Got {self.longitude}")
        if self.frame.upper() not in ['NED', 'ENU']:
            raise ValueError(f"{self.frame} is not a valid frame. Try 'NED' or 'ENU'")

    def reset_coefficients(self, date: Union[datetime.date, int, float] = None) -> None:
        """
        Reset Gauss coefficients to given date.

        Given the date, the corresponding coefficients are updated. Basic
        properties (epoch, release date, and model id) are read and updated in
        the current instance.

        The two coefficient tables (arrays) are also updated, where the
        attribute `c` contains the Gaussian coefficients, while the attribute
        `cd` contains the secular Gaussian coefficients.

        The lenght of the Gaussian coefficient array determines the degree
        :math:`n` of the model. This property updates the value of attribute
        ``degree``.

        Parameters
        ----------
        date : datetime.date, int or float, default: current day
            Date of desired magnetic field estimation.

        """
        self.reset_date(date)
        self.__dict__.update(self.get_properties(self.wmm_filename))
        self.load_coefficients(self.wmm_filename)

    def load_coefficients(self, cof_file: str) -> None:
        """
        Load model coefficients from COF file.

        The model coefficients, also referred to as Gauss coefficients, are
        listed in a COF file. These coefficients can be used to compute values
        of the fields elements and their annual rates of change at any
        location near the surface of the Earth.

        The COF file has 6 columns:

        * ``n`` is the degree.
        * ``m`` is the order.
        * ``g`` are time-dependent Gauss coefficients of degree ``n`` and order ``m``.
        * ``h`` are time-dependent Gauss coefficients of degree ``n`` and order ``m``.
        * ``gd`` are secular variations of coefficient ``g``.
        * ``hd`` are secular variations of coefficient ``h``.

        which constitute the *model* of the field. The first-order time
        derivatives are called *secular terms*. The units are ``nT`` for the
        main field, and ``nT/year`` for the secular variation.

        The Gauss coefficients are defined for a time :math:`t` as:

        .. math::
            \\begin{eqnarray}
            g_n^m(t) & = & g_n^m(t_0) + (t-t_0) \\dot{g}_n^m(t_0) \\\\
            h_n^m(t) & = & h_n^m(t_0) + (t-t_0) \\dot{h}_n^m(t_0)
            \\end{eqnarray}

        where time is given in decimal years and :math:`t_0` corresponds to the
        epoch read from the corresponding COF file.

        Parameters
        ----------
        cof_file : str
            Path to COF file with the coefficients of the WMM

        """
        file_data = pkgutil.get_data(__name__, cof_file).decode()
        data = np.genfromtxt(StringIO(file_data), comments="999999", skip_header=1)
        self.degree = int(max(data[:, 0]))
        self.c = np.zeros((self.degree+1, self.degree+1))
        self.cd = np.zeros((self.degree+1, self.degree+1))
        for row in data:
            n, m = row[:2].astype(int)
            self.c[m, n] = row[2]           # g_n^m
            self.cd[m, n] = row[4]          # g_n^m secular
            if m != 0:
                self.c[n, m-1] = row[3]     # h_n^m
                self.cd[n, m-1] = row[5]    # h_n^m secular

    def get_properties(self, cof_file: str) -> Dict[str, Union[str, float]]:
        """
        Return dictionary of WMM properties from COF file.

        Three properties are read and returned in a dictionary:

        * ``epoch`` is the initial time :math:`t_0` as a `float`.
        * ``model`` is a string of model used for the required lustrum.
        * ``modeldate`` is the release date of used magnetic model.

        Parameters
        ----------
        cof_file : str
            Path to COF file with the coefficients of the WMM

        Returns
        -------
        properties : dictionary
            Dictionary with the three WMM properties.

        Examples
        --------
        >>> wmm = ahrs.WMM()
        >>> wmm.get_properties('my_coefficients.COF')
        {'model': 'WMM-2020', 'modeldate': '12/10/2019', 'epoch': 2020.0}

        """
        if not cof_file.endswith(".COF"):
            raise TypeError("File must have extension 'COF'")
        first_line = pkgutil.get_data(__name__, cof_file).decode().split('\n')[0]
        v = first_line.strip().split()
        properties = dict(zip(["model", "modeldate"], v[1:]))
        properties.update({"epoch": float(v[0])})
        return properties

    def reset_date(self, date: Union[datetime.date, int, float]) -> None:
        """
        Set date to use with the model.

        The WMM requires a date. This date can be given as an instance of
        `datetime.date` or as a decimalized date of the format ``YYYY.d``.

        If None is given it sets the date to the present day. In addition, the
        corresponding COF file is also set.

        Please note that only coefficents from year 2015 and later are provided
        with this module.

        Parameters
        ----------
        date : datetime.date, int or float, default: current day
            Date of desired magnetic field estimation.
        """
        if date is None:
            self.date = datetime.date.today()
            self.date_dec = self.date.year + self.date.timetuple().tm_yday/365.0
        elif isinstance(date, (int, float)):
            self.date_dec = float(date)
            self.date = datetime.date.fromordinal(round(datetime.date(int(date), 1, 1).toordinal() + (self.date_dec-int(self.date_dec))*365))
        elif isinstance(date, datetime.date):
            self.date = date
            self.date_dec = self.date.year + self.date.timetuple().tm_yday/365.0
        else:
            raise TypeError(f"Date must be an instance of datetime.date or a decimalized year. Got {type(date)}")
        if self.date.year < 2015:
            raise ValueError("No available coefficients for dates before 2015.")
        self.wmm_filename = 'WMM2015/WMM.COF' if self.date_dec < 2020.0 else 'WMM2020/WMM.COF'

    def denormalize_coefficients(self, latitude: float) -> None:
        """Recursively estimate associated Legendre polynomials and derivatives
        done in a recursive way as described by Michael Plett in [Wertz]_ for
        an efficient computation.

        Given the Gaussian coefficients, it is possible to estimate the
        magnetic field at any latitude on Earth for a certain date.

        First, it is assumed that :math:`P_n^m(x)` are the Schmidt
        semi-normalized functions. A normalization is made so that the
        relative strength of terms of same degree :math:`n` but order :math:`m`
        are used by comparing their respective Gauss coefficients.

        For :math:`m=0` they are called *Legendre Polynomials* and can be
        computed recursively with:

        .. math::

            P_n(x) = \\frac{2n-1}{n} x P_{n-1}(x) - \\frac{n-1}{n}P_{n-2}(x)

        For :math:`m>0` they are known as *associated Legendre functions*
        of degree :math:`n` and order :math:`m` and reduced to:

        .. math::

            P_{nm}(x) = (1-t^2)^{m/2} \\frac{d^m P_n(x)}{dt^m}

        expressing the associated Legendre functions in terms of the Legendre
        polynomials of same degree :math:`n`.

        A more general formula to estimate both polynomial and associated
        functions is given by:

        .. math::

            P_{nm}(x) = 2^{-n}(1-x^2)^{m/2} \\sum_{k=0}^{K}(-1)^k\\frac{(2n-2k)!}{k!(n-k)!(n-m-2k)!}x^{n-m-2k}

        where :math:`K` is either :math:`(n-m)/2` or :math:`(n-m-1)/2`,
        whichever is an integer. For a computational improvement, the terms are
        calculated recursively.
        
        We have to denormalize the coefficients from Schmidt to Gauss. The
        Gauss functions :math:`P^{n, m}` are related to Schmidt functions
        :math:`P_n^m` as:

        .. math::

            P_n^m = S_{n, m}P^{n, m}

        where the factors :math:`S_{n, m}` are combined with Gaussian
        coefficients to accelerate the computation, because they are
        independent of the geographic location. Thus, we denormalize the
        coefficients with:

        .. math::

            \\begin{array}{ll}
                g^{n,m} & = S_{n,m} g_n^m \\\\
                h^{n,m} & = S_{n,m} h_n^m
            \\end{array}

        The recursion for :math:`S_{n, m}` is:

        .. math::

            \\begin{array}{rlr}
                S_{0,0} & = 1 & \\\\
                S_{n,0} & = S_{n-1, 0} \\frac{2n-1}{n} & n\\geq 1 \\\\
                S_{n,m} & = S_{n-1, m}\\sqrt{\\frac{(n-m+1)(\\delta _m^1+1)}{n+m}} & m\\geq 1
            \\end{array}

        where the Kronecker delta :math:`\\delta_j^i` is:

        .. math::

            \\delta_j^i = \\left\\{
            \\begin{array}{ll}
                1 & \\: i = j \\\\
                0 & \\: \\mathrm{otherwise}
            \\end{array}
            \\right.

        Similarly, :math:`P^{n, m}(x)` can be recursively obtained:

        .. math::

            \\begin{array}{ll}
                P^{0,0} & = 1 \\\\
                P^{n,n} & = \\sin (x) P^{n-1, n-1} \\\\
                P^{n,m} & = \\cos (x) P^{n-1, m} - K^{n, m} P^{n-2, m}
            \\end{array}

        where:

        .. math::

            K^{n, m} = \\left\\{
            \\begin{array}{ll}
                \\frac{(n-1)^2-m^2}{(2n-1)(2n-3)} & \\: n>1 \\\\
                0 & \\: n=1
            \\end{array}
            \\right.

        Likewise, the gradient :math:`\\frac{dP^{n, m}}{dx}` is estimated as:

        .. math::

            \\begin{array}{llr}
                \\frac{dP^{0, 0}}{dx} & = 1 & \\\\
                \\frac{dP^{n, n}}{dx} & = \\sin (x) \\frac{dP^{n-1, n-1}}{dx} + \\cos (x) P^{n-1, n-1} & n\\geq 1 \\\\
                \\frac{dP^{n, m}}{dx} & = \\cos (x) \\frac{dP^{n-1, m}}{dx} - \\sin (x) P^{n-1, m} - K^{n, m} \\frac{dP^{n-2, m}}{dx} &
            \\end{array}

        Parameters
        ----------
        latitude : float
            Latitude in spherical geocentric coordinates

        """
        cos_lat = np.cos(latitude)                  # cos(phi')
        sin_lat = np.sin(latitude)                  # sin(phi')
        S = np.identity(self.degree+1)              # Scale factors
        self.k = np.zeros((self.degree+1, self.degree+1))
        self.P = np.identity(self.degree+2)
        self.dP = np.zeros((self.degree+2, self.degree+1))
        for n in range(1, self.degree+1):
            S[0, n] = S[0, n-1] * (2*n-1)/n
            delta = 1           # Kronecker delta
            for m in range(n+1):
                self.k[m, n] = ((n-1)**2 - m**2) / ((2*n-1)*(2*n-3))
                if m > 0:
                    S[m, n] = S[m-1, n] * np.sqrt((n-m+1)*(delta+1)/(n+m))
                    self.c[n, m-1] *= S[m, n]
                    self.cd[n, m-1] *= S[m, n]
                    delta = 0
                if n == m:
                    self.P[m, n] = cos_lat*self.P[m-1, n-1]
                    self.dP[m, n] = cos_lat*self.dP[m-1, n-1] + sin_lat*self.P[m-1, n-1]
                else:
                    self.P[m, n] = sin_lat*self.P[m, n-1] - self.k[m, n]*self.P[m, n-2]
                    self.dP[m, n] = sin_lat*self.dP[m, n-1] - cos_lat*self.P[m, n-1] - self.k[m, n]*self.dP[m, n-2]
                self.c[m, n] *= S[m, n]
                self.cd[m, n] *= S[m, n]

    def magnetic_field(self, latitude: float, longitude: float, height: float = 0.0, date: Union[datetime.date, int, float] = datetime.date.today()) -> None:
        """
        Calculate the geomagnetic field elements for a location on Earth.

        The code includes comments with references to equation numbers
        corresponding to the ones in the official report.

        Having the coefficients :math:`g^{n, m}` and :math:`h^{n, m}`, we
        extrapolate them for the desired time :math:`t` as:

        .. math::

            \\begin{array}{ll}
                g_n^m(t) & = g_n^m(t_0) + \\Delta_t \\dot{g}_n^m (t_0) \\\\
                h_n^m(t) & = h_n^m(t_0) + \\Delta_t \\dot{h}_n^m (t_0)
            \\end{array}

        where :math:`\\Delta_t = t-t_0` is the difference between the time
        :math:`t` and the reference epoch model :math:`t_0` (``2020.0`` for the
        newest version.)

        The vector components of the main magnetic field :math:`B` are then
        calculated with:

        .. math::

            \\begin{array}{ll}
                X' & = -\\sum_{n=1}^N\\Big(\\frac{a}{r}\\Big)^{n+2} \\sum_{m=0}^n\\big(g_n^m(t) \\cos(m\\lambda)+h_n^m(t)\\sin(m\\lambda)\\big) \\frac{dP_n^m(\\sin \\phi ')}{d\\phi '} \\\\
                Y' & = \\frac{1}{\\cos\\phi '}\\sum_{n=1}^N\\Big(\\frac{a}{r}\\Big)^{n+2} \\sum_{m=0}^n m\\big(g_n^m(t) \\sin(m\\lambda)-h_n^m(t)\\cos(m\\lambda)\\big)P_n^m(\\sin \\phi ') \\\\
                Z' & = -\\sum_{n=1}^N(n+1)\\Big(\\frac{a}{r}\\Big)^{n+2} \\sum_{m=0}^n\\big(g_n^m(t) \\cos(m\\lambda)+h_n^m(t)\\sin(m\\lambda)\\big)P_n^m(\\sin \\phi ')
            \\end{array}

        Finally, the geomagnetic vector components are rotated into ellipsoidal
        reference frame.

        .. math::

            \\begin{array}{ll}
                X & = X'\\cos(\\phi ' - \\phi) - Z' \\sin(\\phi ' - \\phi) \\\\
                Y & = Y' \\\\
                Z & = X'\\sin(\\phi ' - \\phi) + Z' \\cos(\\phi ' - \\phi)
            \\end{array}

        These components are used to compute the rest of the magnetic elements:

        .. math::

            \\begin{array}{ll}
                H & = \\sqrt{X^2 + Y^2} \\\\
                F & = \\sqrt{H^2 + Z^2} \\\\
                I & = \\arctan(\\frac{Z}{H}) \\\\
                D & = \\arctan(\\frac{Y}{X})
            \\end{array}

        .. note::
            The use of ``arctan2`` yields a more precise result than ``arctan``,
            because it estimates the angle exploring all quadrants.

        For polar regions, where the declination changes drastically, the WMM
        defines two different grivations (one for each pole) defined as:

        .. math::

            GV = \\left\\{
            \\begin{array}{ll}
                D-\\lambda & \\: \\phi > 55 ° \\\\
                D+\\lambda & \\: \\phi < -55 °
            \\end{array}
            \\right.

        Parameters
        ----------
        latitude : float
            Latitude, in decimal degrees, in geodetic coordinates
        longitude : float
            Longitude in decimal degrees, in geodetic coordinates
        height : float, default: 0.0
            Mean Sea Level Height in kilometers
        date : datetime.date, int or float, default: datetime.date.today()
            Desired date to estimate
        """
        if date is not None:
            self.reset_coefficients(date)
        self.latitude = latitude
        self.longitude = longitude
        self.height = height
        latitude *= DEG2RAD
        longitude *= DEG2RAD
        # Transform geodetic coordinates into spherical geocentric coordinates
        lat_prime, _, r = geodetic2spherical(latitude, longitude, self.height)
        # Compute cos(m*phi') and sin(m*phi') for all m values
        self.sp = np.zeros(self.degree+1)               # sin(m*phi')
        self.cp = np.ones(self.degree+2)                # cos(m*phi')
        self.sp[1] = np.sin(longitude)
        self.cp[1] = np.cos(longitude)
        for m in range(2, self.degree+1):
            self.sp[m] = self.sp[1]*self.cp[m-1] + self.cp[1]*self.sp[m-1]
            self.cp[m] = self.cp[1]*self.cp[m-1] - self.sp[1]*self.sp[m-1]
        dt = round(self.date_dec, 1) - self.epoch       # t - t_0
        self.gh = np.zeros((self.degree+2, self.degree+1))
        self.denormalize_coefficients(lat_prime)
        cos_lat = np.cos(lat_prime)                     # cos(phi')
        sin_lat = np.sin(lat_prime)                     # sin(phi')
        Zp = Xp = Yp = Bp = 0.0
        a = EARTH_MEAN_RADIUS/1000.0                    # Mean earth radius in km
        ar = a/r
        # Spherical Harmonics (eq. 4)
        for n in range(1, self.degree+1):   #### !! According to report it must be equal to defined degree (12 not 13)
            arn2 = ar**(n+2)
            x_p = y_p = z_p = 0.0
            for m in range(n+1):            #### !! According to report it must be equal to n
                self.gh[m, n] = self.c[m, n] + dt*self.cd[m, n]     # g_n^m (eq. 9)
                # Terms of spherical harmonic expansions
                gchs = self.gh[m, n]*self.cp[m]         # g(t)cos(ml)
                gshc = self.gh[m, n]*self.sp[m]         # g(t)sin(ml)
                if m > 0:
                    self.gh[n, m-1] = self.c[n, m-1] + dt*self.cd[n, m-1]   # h_n^m (eq. 9)
                    gchs += self.gh[n, m-1]*self.sp[m]  # g(t)cos(ml) + h(t)sin(ml)
                    gshc -= self.gh[n, m-1]*self.cp[m]  # g(t)sin(ml) - h(t)cos(ml)
                x_p += gchs * self.dP[m, n]
                y_p += m * gshc * self.P[m, n]
                z_p += gchs * self.P[m, n]
                # SPECIAL CASE: NORTH/SOUTH GEOGRAPHIC POLES
                if (cos_lat == 0.0 and m == 1):
                    Bp += arn2 * gshc
                    if n > 1:
                        Bp *= sin_lat - self.k[m, n]
            Xp += arn2 * x_p                            # (eq. 10)  #### !! According to report must be a substraction. Must re-check this
            Yp += arn2 * y_p                            # (eq. 11)
            Zp -= (n+1) * arn2 * z_p                    # (eq. 12)
        Yp = Bp if cos_lat == 0.0 else Yp/cos_lat
        # Transform magnetic vector components to geodetic coordinates (eq. 17)
        self.X = Xp*np.cos(lat_prime-latitude) - Zp*np.sin(lat_prime-latitude)
        self.Y = Yp
        self.Z = Xp*np.sin(lat_prime-latitude) + Zp*np.cos(lat_prime-latitude)
        # Rotate elements if ENU frame
        if self.frame.upper() == 'ENU':
            self.X, self.Y, self.Z = ned2enu([self.X, self.Y, self.Z])
        # Total Intensity, Inclination and Declination (eq. 19)
        self.H = np.linalg.norm([self.X, self.Y])       # sqrt(X^2+Y^2)
        self.F = np.linalg.norm([self.H, self.Z])       # sqrt(H^2+Z^2)
        self.I = RAD2DEG*np.arctan2(self.Z, self.H)
        self.D = RAD2DEG*np.arctan2(self.Y, self.X)
        # Grivation (eq. 1)
        self.GV = self.D.copy()
        if self.latitude > 55.0:
            self.GV -= self.longitude
        if self.latitude < -55.0:
            self.GV += self.longitude

    @property
    def magnetic_elements(self) -> Dict[str, float]:
        """Main geomagnetic elements in a dictionary

        =======  =============================================
        Element  Definition
        =======  =============================================
        X        Northerly intensity
        Y        Easterly intensity
        Z        Vertical intensity (Positive downwards)
        H        Horizontal intensity
        F        Total intensity
        I        Inclination angle (a.k.a. dip angle)
        D        Declination angle (a.k.a. magnetic variation)
        GV       Grivation
        =======  =============================================

        Example
        -------
        >>> wmm = WMM(datetime.date(2017, 5, 12), latitude=10.0, longitude=-20.0, height=10.5)
        >>> wmm.magnetic_elements
        {'X': 30499.640469609083, 'Y': -5230.267158472566, 'Z': -1716.633311360368,
        'H': 30944.850352270452, 'F': 30992.427998627096, 'I': -3.1751692563622993,
        'D': -9.73078560629778, 'GV': -9.73078560629778}
        """
        return {k: self.__dict__[k] for k in ['X', 'Y', 'Z', 'H', 'F', 'I', 'D', 'GV']}
