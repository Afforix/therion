#ifdef CATCH2_V3
#include <catch2/catch_test_macros.hpp>
#else
#include <catch2/catch.hpp>
#endif
#include <cmath>

#include "thproj.h"
#include "thcsdata.h"
#include "thcs.h"

#ifndef M_PI
#define M_PI       3.14159265358979323846
#endif

// tests for coordinate systems transformations using Proj library

double th_eps = 0.05;

bool coord_equal(double x1, double x2, double precision = 0) {
  return fabs(x1 - x2) < (precision == 0 ? th_eps : precision);
}

double dms2dec(int d, int m, double s) {
  return (double) d + m/60.0 + s/3600.0;
}

double deg2rad(double d) {
  return d / 180.0 * M_PI;
}

double x,y,z;

// p1 data from skgeodesy.sk
double p1_ll_phi = deg2rad(dms2dec(48, 56, 10.50838));
double p1_ll_lambda = deg2rad(dms2dec(19, 39, 11.93192));
double p1_ll_h = 2068.93;

double p1_jtsk_y = 379033.66;
double p1_jtsk_x = 1208895.36;
double p1_jtsk_h = 2025.31;

double p1_jtsk03_y = 379033.29;
double p1_jtsk03_x = 1208895.40;
double p1_jtsk03_h = 2025.31;

double p1_utm_e = 401375.61;
double p1_utm_n = 5421243.26;
double p1_utm_h = 2025.437;

double p1_s42_y = 7401459.88;
double p1_s42_x = 5423543.01;

double undefined = NAN;

std::vector<axis_orient> ax;
double scale;
bool gis_ok;


TEST_CASE( "projections: init", "[proj]" ) {
    CHECK(thcs_check(thcs_get_params(TTCS_JTSK03)));
}

//TEST_CASE( "projections: init garbage", "[proj]" ) {
//    CHECK_FALSE(thcs_check("+proj=garbage +ellps=wgs84"));
//}

TEST_CASE( "projections: is lat/long", "[proj]" ) {
    CHECK(thcs_islatlong(thcs_get_params(TTCS_JTSK03))==false);
    CHECK(thcs_islatlong(thcs_get_params(TTCS_EPSG + 32634))==false);
    CHECK(thcs_islatlong(thcs_get_params(TTCS_LAT_LONG)));
    CHECK(thcs_islatlong(thcs_get_params(TTCS_EPSG + 4326)));
}

TEST_CASE( "projections: meridian convergence", "[proj]" ) {
    // therion uses a convention that the convergence is positive west to central meridian
    CHECK(coord_equal(thcsconverg(TTCS_EPSG + 32634, p1_utm_e, p1_utm_n), -atan(tan(p1_ll_lambda-deg2rad(21.0))*sin(p1_ll_phi))*180/M_PI, 0.1/3600));   // 0.1 deg second
    // https://geodesyapps.ga.gov.au/geographic-to-grid
    CHECK(coord_equal(thcsconverg(TTCS_EPSG + 32634, 350812.125, 5318235.614),  1.486562, 0.01/3600));  // 48 N, 19 E (central meridian 21 E)
    CHECK(coord_equal(thcsconverg(TTCS_EPSG + 32634, 649187.875, 5318235.614), -1.486562, 0.01/3600));  // 48 N, 23 E
    CHECK(coord_equal(thcsconverg(TTCS_EPSG + 32734, 350812.125, 4681764.386), -1.486562, 0.01/3600));  // 48 S, 19 E
    CHECK(coord_equal(thcsconverg(TTCS_EPSG + 32734, 649187.875, 4681764.386),  1.486562, 0.01/3600));  // 48 S, 23 E
}

TEST_CASE( "projections: UTM zones", "[proj]" ) {
    CHECK(thcs2zone(TTCS_JTSK03, 509063.948, 1303089.825,0)==34);
    CHECK(thcs2zone(TTCS_JTSK03, 509063.963, 1303089.823,0)==33);
}

TEST_CASE( "projections: EPSG label (generated)", "[proj]" ) {
    CHECK(thcs_get_label(TTCS_EPSG + 32634) == "WGS 84 / UTM zone 34N");
}

TEST_CASE( "projections: custom label (defined)", "[proj]" ) {
    CHECK(thcs_get_label(TTCS_OSGB_ST) == "OSGB:ST");
}

TEST_CASE( "projections: custom label (generated)", "[proj]" ) {
    CHECK(thcs_get_label(TTCS_LAT_LONG) == "WGS 84");
}

TEST_CASE( "projections: JTSK03 -- utm", "[proj]" ) {
    thcs2cs(TTCS_JTSK03, TTCS_ETRS34,
            p1_jtsk03_y, p1_jtsk03_x, p1_jtsk03_h, x, y, z);
    CHECK(coord_equal(x, p1_utm_e, 0.01));
    CHECK(coord_equal(y, p1_utm_n, 0.01));
    CHECK(coord_equal(z, p1_jtsk_h, 0.001));
}

TEST_CASE( "projections: JTSK03 -- utm, NaN z coordinate", "[proj]" ) {
    thcs2cs(TTCS_JTSK03, TTCS_ETRS34,
            p1_jtsk03_y, p1_jtsk03_x, undefined, x, y, z);
    CHECK(coord_equal(x, p1_utm_e, 0.01));
    CHECK(coord_equal(y, p1_utm_n, 0.01));
    CHECK(std::isnan(z));
}

/*
TEST_CASE( "projections: +krovak +czech -- utm, auto=true", "[proj]" ) {
    thcs_cfg.proj_auto = true;
    thcs2cs("+proj=krovak +czech +ellps=bessel +lat_0=49.5 +lon_0=24.833333333333333333 +k=0.9999 +towgs84=485.021,169.465,483.839,7.786342,4.397554,4.102655,0", thcs_get_params(TTCS_UTM34N),
            p1_jtsk_y, p1_jtsk_x, p1_jtsk_h, x, y, z);
    thcs_cfg.proj_auto = false;
    CHECK(coord_equal(x, p1_utm_e, 0.01));
    CHECK(coord_equal(y, p1_utm_n, 0.01));
    CHECK(coord_equal(z, p1_jtsk_h, 0.001));
} */

TEST_CASE( "projections: iJTSK03 -- utm", "[proj]" ) {
    thcs2cs(TTCS_IJTSK03, TTCS_UTM34N,
            -p1_jtsk03_y, -p1_jtsk03_x, p1_jtsk03_h, x, y, z);
    CHECK(coord_equal(x, p1_utm_e, 0.01));
    CHECK(coord_equal(y, p1_utm_n, 0.01));
    CHECK(coord_equal(z, p1_jtsk_h, 0.001));
}

TEST_CASE( "projections: latlong -- JTSK03", "[proj]" ) {
    thcs2cs(TTCS_LAT_LONG, TTCS_JTSK03,
        p1_ll_lambda, p1_ll_phi, p1_ll_h, x, y, z);
    CHECK(coord_equal(x, p1_jtsk03_y, 0.01));
    CHECK(coord_equal(y, p1_jtsk03_x, 0.01));
}

TEST_CASE( "projections: JTSK03 -- EPSG_4417", "[proj]" ) {
    thcs2cs(TTCS_JTSK03, TTCS_EPSG + 4417,
        p1_jtsk03_y, p1_jtsk03_x, p1_jtsk03_h, x, y, z);
    CHECK(coord_equal(x, p1_s42_y, 2.1));
    CHECK(coord_equal(y, p1_s42_x, 0.9));
}

TEST_CASE( "projections: iJTSK03 -- EPSG_4417", "[proj]" ) {
    thcs2cs(TTCS_IJTSK03, TTCS_EPSG + 4417,
        -p1_jtsk03_y, -p1_jtsk03_x, p1_jtsk03_h, x, y, z);
    CHECK(coord_equal(x, p1_s42_y, 2.1));
    CHECK(coord_equal(y, p1_s42_x, 0.9));
}

TEST_CASE( "UTM34N -- EPSG_4417", "[proj]" ) {    // UTM34N -> S42
    thcs2cs(TTCS_UTM34N, TTCS_EPSG + 4417,
        p1_utm_e, p1_utm_n, p1_utm_h, x, y, z);
    CHECK(coord_equal(x, p1_s42_y, 2.1));
    CHECK(coord_equal(y, p1_s42_x, 0.9));
}

TEST_CASE( "EPSG_4326 -- EPSG_32634", "[proj]" ) {  // LATLON -> UTM34N
    thcs2cs(TTCS_EPSG + 4326, TTCS_EPSG + 32634,
        p1_ll_lambda, p1_ll_phi, p1_ll_h, x, y, z);
    CHECK(coord_equal(x, p1_utm_e, 0.01));
    CHECK(coord_equal(y, p1_utm_n, 0.01));
}

// null grid
TEST_CASE( "s-merc -- EPSG_32634", "[proj]" ) {  // Pseudo Mercator -> UTM34N
    thcs2cs(TTCS_S_MERC, TTCS_EPSG + 32634,
        2187796.96, 6264051.66, 2025.44, x, y, z);
    CHECK(coord_equal(x, p1_utm_e, 0.01));
    CHECK(coord_equal(y, p1_utm_n, 0.01));
    CHECK(coord_equal(z, 2025.44, 0.001));
}

TEST_CASE( "axes -- JTSK", "[proj]" ) {
    ax = thcs_axesinfo(TTCS_JTSK, scale, gis_ok);
    CHECK(ax[0] == axis_orient::WEST);
    CHECK(ax[1] == axis_orient::SOUTH);
    CHECK(scale == 1.0);
    CHECK(gis_ok == false);
}

TEST_CASE( "axes -- EPSG_32634", "[proj]" ) {
    ax = thcs_axesinfo(TTCS_EPSG + 32634, scale, gis_ok);
    CHECK(ax[0] == axis_orient::EAST);
    CHECK(ax[1] == axis_orient::NORTH);
    CHECK(scale == 1.0);
    CHECK(gis_ok == true);
}

TEST_CASE( "axes -- latlong", "[proj]" ) {
    ax = thcs_axesinfo(TTCS_LAT_LONG, scale, gis_ok);
    CHECK(ax[0] == axis_orient::NORTH);
    CHECK(ax[1] == axis_orient::EAST);
    CHECK(scale == 0.0);
    CHECK(gis_ok == false);
}

/*
// GRID
TEST_CASE( "projections: JTSK grid -- utm, auto=true", "[proj]" ) {
    thcs_cfg.proj_auto = true;
    thcs2cs("+proj=krovak +ellps=bessel +czech +nadgrids=slovak", thcs_get_params(TTCS_UTM34N),
            p1_jtsk_y, p1_jtsk_x, p1_jtsk_h, x, y, z);
    thcs_cfg.proj_auto = false;
    CHECK(coord_equal(x, p1_utm_e, 1));
    CHECK(coord_equal(y, p1_utm_n, 1));
    CHECK(coord_equal(z, p1_utm_h, 1));
}

// GRID
TEST_CASE( "projections: iJTSK grid -- utm, auto=true", "[proj]" ) {
    thcs_cfg.proj_auto = true;
    thcs2cs("+proj=krovak +ellps=bessel +lat_0=49.5 +lon_0=24.833333333333333333 +k=0.9999 +nadgrids=slovak", thcs_get_params(TTCS_UTM34N),
            -p1_jtsk_y, -p1_jtsk_x, p1_jtsk_h, x, y, z);
    thcs_cfg.proj_auto = false;
    CHECK(coord_equal(x, p1_utm_e, 1));
    CHECK(coord_equal(y, p1_utm_n, 1));
    CHECK(coord_equal(z, p1_utm_h, 1));
}
*/

// tbc
