#!/usr/bin/env python3

import re

# <identifiers> <options> <libPROJ definition> <label>
proj_specs = [
  (["long-lat"], ["dms"], "epsg:4326", ""),
  (["lat-long"], ["dms", "swap"], "epsg:4326 ", ""),
  (["etrs"], ["dms"], "epsg:4258", ""),
  (["jtsk"],   [], "+proj=krovak +axis=wsu +ellps=bessel +lat_0=49.5 +lon_0=24.833333333333333333 +k=0.9999 +towgs84=570.8285,85.6769,462.842,4.9984,1.5867,5.2611,3.5623", ""),
  (["jtsk03"], [], "+proj=krovak +axis=wsu +ellps=bessel +lat_0=49.5 +lon_0=24.833333333333333333 +k=0.9999 +towgs84=485.021,169.465,483.839,7.786342,4.397554,4.102655,0", ""),
  (["ijtsk"],   ["output"], "+proj=krovak +ellps=bessel +lat_0=49.5 +lon_0=24.833333333333333333 +k=0.9999 +towgs84=570.8285,85.6769,462.842,4.9984,1.5867,5.2611,3.5623", ""),
  (["ijtsk03"], ["output"], "+proj=krovak +ellps=bessel +lat_0=49.5 +lon_0=24.833333333333333333 +k=0.9999 +towgs84=485.021,169.465,483.839,7.786342,4.397554,4.102655,0", ""),
  (["s-merc"], ["output"], "epsg:3857", ""),
  (["eur79z30"], ["output"], "+proj=utm +zone=30 +ellps=intl +towgs84=-86,-98,-119,0,0,0,0 +no_defs", "")
]

# add UTM projections
for zone in range(1, 61):
    proj_specs.append(([f"utm{zone}n", f"utm{zone}"], ["output"], f"epsg:{zone+32600}", ""))
    proj_specs.append(([f"utm{zone}s"], ["output"], f"epsg:{zone+32700}", ""))

# ETRS zones
for zone in range(28, 38):
    proj_specs.append(([f"etrs{zone}"], ["output"], f"epsg:{zone+25800}", ""))

# The proj_transformations list is taken directly from the Tcl code, removing only the Tcl comment lines:
proj_transformations = [
(["etrs", "epsg:4258"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["etrs", "epsg:4258"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["long-lat", "lat-long", "epsg:4326"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +proj=push +v_3 +step +proj=cart +ellps=WGS84 +step +inv +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["ijtsk", "epsg:5514"], ["etrs", "epsg:4258"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3"),
(["ijtsk", "epsg:5514"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["ijtsk03", "epsg:8353"], ["etrs", "epsg:4258"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3"),
(["ijtsk03", "epsg:8353"], ["long-lat", "lat-long", "epsg:4326"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3"),
(["ijtsk03", "epsg:8353"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["epsg:3046"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +inv +proj=utm +zone=34 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["epsg:3046"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +inv +proj=utm +zone=34 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["utm34", "epsg:32634"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +inv +proj=utm +zone=34 +ellps=WGS84 +step +proj=push +v_3 +step +proj=cart +ellps=WGS84 +step +inv +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["s-merc", "epsg:3857"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +inv +proj=webmerc +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +step +proj=push +v_3 +step +proj=cart +ellps=WGS84 +step +inv +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["ijtsk", "epsg:5514"], ["epsg:3046"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=utm +zone=34 +ellps=GRS80"),
(["ijtsk03", "epsg:8353"], ["epsg:3046"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=utm +zone=34 +ellps=GRS80"),
(["ijtsk03", "epsg:8353"], ["utm34", "epsg:32634"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3 +step +proj=utm +zone=34 +ellps=WGS84"),
(["ijtsk03", "epsg:8353"], ["s-merc", "epsg:3857"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3 +step +proj=webmerc +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84"),
(["ijtsk", "epsg:5514"], ["long-lat", "lat-long", "epsg:4326"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3"),
(["ijtsk", "epsg:5514"], ["utm34", "epsg:32634"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3 +step +proj=utm +zone=34 +ellps=WGS84"),
(["ijtsk", "epsg:5514"], ["s-merc", "epsg:3857"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3 +step +proj=webmerc +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84"),
(["long-lat", "lat-long", "epsg:4326"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +proj=push +v_3 +step +proj=cart +ellps=WGS84 +step +inv +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["utm34", "epsg:32634"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +inv +proj=utm +zone=34 +ellps=WGS84 +step +proj=push +v_3 +step +proj=cart +ellps=WGS84 +step +inv +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["s-merc", "epsg:3857"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +inv +proj=webmerc +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +step +proj=push +v_3 +step +proj=cart +ellps=WGS84 +step +inv +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["etrs", "epsg:4258"], ["long-lat", "lat-long", "epsg:4326"], "+proj=noop"),
(["long-lat", "lat-long", "epsg:4326"], ["etrs", "epsg:4258"], "+proj=noop"),
(["etrs", "epsg:4258"], ["jtsk", "epsg:5513"], "+proj=pipeline +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["etrs", "epsg:4258"], ["jtsk03", "epsg:8352"], "+proj=pipeline +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["long-lat", "lat-long", "epsg:4326"], ["jtsk03", "epsg:8352"], "+proj=pipeline +step +proj=push +v_3 +step +proj=cart +ellps=WGS84 +step +inv +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["jtsk", "epsg:5513"], ["etrs", "epsg:4258"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3"),
(["jtsk", "epsg:5513"], ["jtsk03", "epsg:8352"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["jtsk03", "epsg:8352"], ["etrs", "epsg:4258"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3"),
(["jtsk03", "epsg:8352"], ["long-lat", "lat-long", "epsg:4326"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3"),
(["jtsk03", "epsg:8352"], ["jtsk", "epsg:5513"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["epsg:3046"], ["jtsk", "epsg:5513"], "+proj=pipeline +step +inv +proj=utm +zone=34 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["epsg:3046"], ["jtsk03", "epsg:8352"], "+proj=pipeline +step +inv +proj=utm +zone=34 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["utm34", "epsg:32634"], ["jtsk03", "epsg:8352"], "+proj=pipeline +step +inv +proj=utm +zone=34 +ellps=WGS84 +step +proj=push +v_3 +step +proj=cart +ellps=WGS84 +step +inv +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["s-merc", "epsg:3857"], ["jtsk03", "epsg:8352"], "+proj=pipeline +step +inv +proj=webmerc +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +step +proj=push +v_3 +step +proj=cart +ellps=WGS84 +step +inv +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["jtsk", "epsg:5513"], ["epsg:3046"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=utm +zone=34 +ellps=GRS80"),
(["jtsk03", "epsg:8352"], ["epsg:3046"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=utm +zone=34 +ellps=GRS80"),
(["jtsk03", "epsg:8352"], ["utm34", "epsg:32634"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3 +step +proj=utm +zone=34 +ellps=WGS84"),
(["jtsk03", "epsg:8352"], ["s-merc", "epsg:3857"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3 +step +proj=webmerc +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84"),
(["jtsk", "epsg:5513"], ["long-lat", "lat-long", "epsg:4326"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3"),
(["jtsk", "epsg:5513"], ["utm34", "epsg:32634"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3 +step +proj=utm +zone=34 +ellps=WGS84"),
(["jtsk", "epsg:5513"], ["s-merc", "epsg:3857"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3 +step +proj=webmerc +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84"),
(["etrs34", "epsg:25834"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +inv +proj=utm +zone=34 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["etrs34", "epsg:25834"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +inv +proj=utm +zone=34 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["epsg:3034"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +inv +proj=lcc +lat_0=52 +lon_0=10 +lat_1=35 +lat_2=65 +x_0=4000000 +y_0=2800000 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["epsg:3034"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +inv +proj=lcc +lat_0=52 +lon_0=10 +lat_1=35 +lat_2=65 +x_0=4000000 +y_0=2800000 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["epsg:3035"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +inv +proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["epsg:3035"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +inv +proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["ijtsk", "epsg:5514"], ["etrs34", "epsg:25834"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=utm +zone=34 +ellps=GRS80"),
(["ijtsk", "epsg:5514"], ["epsg:3035"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80"),
(["ijtsk03", "epsg:8353"], ["etrs34", "epsg:25834"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=utm +zone=34 +ellps=GRS80"),
(["ijtsk", "epsg:5514"], ["epsg:3034"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=lcc +lat_0=52 +lon_0=10 +lat_1=35 +lat_2=65 +x_0=4000000 +y_0=2800000 +ellps=GRS80"),
(["ijtsk03", "epsg:8353"], ["epsg:3035"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80"),
(["ijtsk03", "epsg:8353"], ["epsg:3034"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=lcc +lat_0=52 +lon_0=10 +lat_1=35 +lat_2=65 +x_0=4000000 +y_0=2800000 +ellps=GRS80"),
(["epsg:3045"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +inv +proj=utm +zone=33 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["epsg:3045"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +inv +proj=utm +zone=33 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["jtsk", "epsg:5513"], ["epsg:3045"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=utm +zone=33 +ellps=GRS80"),
(["jtsk03", "epsg:8352"], ["epsg:3045"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=utm +zone=33 +ellps=GRS80"),
(["etrs33", "epsg:25833"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +inv +proj=utm +zone=33 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["etrs33", "epsg:25833"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +inv +proj=utm +zone=33 +ellps=GRS80 +step +proj=push +v_3 +step +proj=cart +ellps=GRS80 +step +proj=helmert +x=-485.014055 +y=-169.473618 +z=-483.842943 +rx=7.78625453 +ry=4.39770887 +rz=4.10248899 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["ijtsk", "epsg:5514"], ["etrs33", "epsg:25833"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=utm +zone=33 +ellps=GRS80"),
(["ijtsk03", "epsg:8353"], ["etrs33", "epsg:25833"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=GRS80 +step +proj=pop +v_3 +step +proj=utm +zone=33 +ellps=GRS80"),
(["utm33", "epsg:32633"], ["ijtsk03", "epsg:8352"], "+proj=pipeline +step +inv +proj=utm +zone=33 +ellps=WGS84 +step +proj=push +v_3 +step +proj=cart +ellps=WGS84 +step +inv +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["ijtsk03", "epsg:8352"], ["utm33", "epsg:32633"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3 +step +proj=utm +zone=33 +ellps=WGS84"),
(["utm33", "epsg:32633"], ["ijtsk", "epsg:5513"], "+proj=pipeline +step +inv +proj=utm +zone=33 +ellps=WGS84 +step +proj=push +v_3 +step +proj=cart +ellps=WGS84 +step +inv +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=bessel +step +proj=pop +v_3 +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["ijtsk", "epsg:5513"], ["utm33", "epsg:32633"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=push +v_3 +step +proj=cart +ellps=bessel +step +proj=helmert +x=485.021 +y=169.465 +z=483.839 +rx=-7.786342 +ry=-4.397554 +rz=-4.102655 +s=0 +convention=coordinate_frame +step +inv +proj=cart +ellps=WGS84 +step +proj=pop +v_3 +step +proj=utm +zone=33 +ellps=WGS84"),
(["jtsk", "epsg:5513"], ["ijtsk03", "epsg:8353"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["jtsk03", "epsg:8352"], ["ijtsk", "epsg:5514"], "+proj=pipeline +step +inv +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["ijtsk", "epsg:5514"], ["jtsk03", "epsg:8352"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +inv +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel"),
(["ijtsk03", "epsg:8353"], ["jtsk", "epsg:5513"], "+proj=pipeline +step +inv +proj=krovak +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +step +proj=hgridshift +grids=sk_gku_JTSK03_to_JTSK.tif +step +proj=krovak +axis=wsu +lat_0=49.5 +lon_0=24.8333333333333 +alpha=30.2881397527778 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel")
]

# OSGB grids
osgb1 = [
    ["S","T"],
    ["N","O"],
    ["H"]
]
osgb2 = [
    ["V","W","X","Y","Z"],
    ["Q","R","S","T","U"],
    ["L","M","N","O","P"],
    ["F","G","H","J","K"],
    ["A","B","C","D","E"]
]

yy = -1
for al in osgb1:
    xx = 4
    for a in al:
        y = yy
        for bl in osgb2:
            x = xx
            for b in bl:
                x_0 = x * 100000
                y_0 = y * 100000
                param = f"+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0={x_0} +y_0={y_0} +ellps=airy +nadgrids=OSTN15_NTv2_OSGBtoETRS.gsb +datum=OSGB36 +units=m +no_defs"
                proj_specs.append(([f"OSGB:{a}{b}"], ["output"], param, f"OSGB:{a}{b}"))
                x -= 1
            y -= 5
        xx -= 5
    yy -= 5

# join identical projections
proj_defs = {}
new_proj_specs = []
for prj in proj_specs:
    ids, opts, params, prjname = prj
    if params in proj_defs:
        px = proj_defs[params]
        orig_prj = list(new_proj_specs[px])
        # add identifiers
        for _id in ids:
            if _id not in orig_prj[0]:
                orig_prj[0].append(_id)
        if len(orig_prj[3]) == 0:
            orig_prj[3] = prjname
        if len(orig_prj[3]) == 0:
            orig_prj[3] = prjname
        new_proj_specs[px] = tuple(orig_prj)
    else:
        proj_defs[params] = len(new_proj_specs)
        new_proj_specs.append(prj)

proj_specs = new_proj_specs

# create parsing table
proj_parse = [["local","TTCS_LOCAL"]]
proj_enum = []
added_enums = set()
for prj in proj_specs:
    ids, opts, params, prjname = prj
    id0 = ids[0].upper()
    enm = "TTCS_" + re.sub(r'[\:\-]', '_', id0)
    if enm not in added_enums:
        proj_enum.append(enm)
        added_enums.add(enm)
    for _id in ids:
        proj_parse.append([_id.upper(), enm])

def escape(s):
    return s.replace('"','\\"')

proj_parse_sorted = sorted(proj_parse, key=lambda x: x[0])

# write thcsdata.h
with open("thcsdata.h", "w") as fid:
    fid.write("""/**
 * @file thcsdata.h
 * Coordinate systems data.
 *
 * THIS FILE IS GENERATED AUTOMATICALLY, DO NOT MODIFY IT !!!
 */
       
#ifndef thcsdata_h
#define thcsdata_h
 
#include "thstok.h"
 
#include <map>

/**
* Add default CS transformations.
*/
void thcs_add_default_transformations();
	
/**
 * CS tokens.
 */
""")

    fid.write("enum {\n  TTCS_UNKNOWN = -2,\n  TTCS_LOCAL = -1,\n")
    for e in proj_enum:
        fid.write(f"  {e},\n")
    fid.write("};\n\n")

    fid.write("""/**
 * CS data structure.
 */
typedef struct {
  bool dms, output, swap;
  const char * params; const char * prjname;
} thcsdata;

extern const thstok thtt_cs[];
extern const thcsdata thcsdata_table[];
#endif
""")

# write thcsdata.cxx
with open("thcsdata.cxx", "w") as fid:
    fid.write("""/**
 * @file thcsdata.cxx
 * Coordinate systems data.
 *
 * THIS FILE IS GENERATED AUTOMATICALLY, DO NOT MODIFY IT !!!
 */
       
#include "thcsdata.h"
#include "thcs.h"

""")

    fid.write("""
/**
 * CS parsing table.
 */
""")

    fid.write("const thstok thtt_cs[] = {\n")
    for e in proj_parse_sorted:
        fid.write(f'  {{"{e[0]}", {e[1]}}},\n')
    fid.write('  {NULL, TTCS_UNKNOWN}\n};\n\n')

    fid.write("""
/**
 * CS data table.
 */
""")

    fid.write(f"const thcsdata thcsdata_table[{len(proj_specs)}] = {{\n")
    for p in proj_specs:
        ids, opts, params, prjname = p
        o_dms = "true" if "dms" in opts else "false"
        o_output = "true" if "output" in opts else "false"
        o_swap = "true" if "swap" in opts else "false"
        fid.write(f'  {{{o_dms}, {o_output}, {o_swap}, "{params}", "{prjname}"}},\n')
    fid.write("};\n\n")

    fid.write("void thcs_add_default_transformations() {\n")
    for p in proj_transformations:
        f = " ".join(p[0])
        t = " ".join(p[1])
        tr = p[2]
        fid.write(f'thcs_add_cs_trans("{escape(f)}", "{escape(t)}", "{escape(tr)}");\n')
    fid.write("}\n\n\n")

print("Files thcsdata.h and thcsdata.cxx have been generated.")
