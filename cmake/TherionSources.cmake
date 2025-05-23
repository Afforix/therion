set(THERION_HEADERS
    ${CMAKE_BINARY_DIR}/thcsdata.h
    ${CMAKE_BINARY_DIR}/thchencdata.h
    ${CMAKE_BINARY_DIR}/thlangdata.h
    ${CMAKE_BINARY_DIR}/thlangdatafields.h
    ${CMAKE_BINARY_DIR}/thmpost.h
    ${CMAKE_BINARY_DIR}/thsymbolsetlist.h
    ${CMAKE_BINARY_DIR}/thsymbolsets.h
    ${CMAKE_BINARY_DIR}/thtex.h
    ${CMAKE_BINARY_DIR}/thversion.h
    ${CMAKE_SOURCE_DIR}/th2ddataobject.h
    ${CMAKE_SOURCE_DIR}/tharea.h
    ${CMAKE_SOURCE_DIR}/thattr.h
    ${CMAKE_SOURCE_DIR}/thbezier.h
    ${CMAKE_SOURCE_DIR}/thbuffer.h
    ${CMAKE_SOURCE_DIR}/thcmdline.h
    ${CMAKE_SOURCE_DIR}/thcomment.h
    ${CMAKE_SOURCE_DIR}/thconfig.h
    ${CMAKE_SOURCE_DIR}/thcs.h
    ${CMAKE_SOURCE_DIR}/thdata.h
    ${CMAKE_SOURCE_DIR}/thdatabase.h
    ${CMAKE_SOURCE_DIR}/thdataleg.h
    ${CMAKE_SOURCE_DIR}/thdataobject.h
    ${CMAKE_SOURCE_DIR}/thdatareader.h
    ${CMAKE_SOURCE_DIR}/thdatastation.h
    ${CMAKE_SOURCE_DIR}/thdate.h
    ${CMAKE_SOURCE_DIR}/thdb1d.h
    ${CMAKE_SOURCE_DIR}/thdb2d.h
    ${CMAKE_SOURCE_DIR}/thdb2dab.h
    ${CMAKE_SOURCE_DIR}/thdb2dcp.h
    ${CMAKE_SOURCE_DIR}/thdb2dji.h
    ${CMAKE_SOURCE_DIR}/thdb2dlp.h
    ${CMAKE_SOURCE_DIR}/thdb2dmi.h
    ${CMAKE_SOURCE_DIR}/thdb2dprj.h
    ${CMAKE_SOURCE_DIR}/thdb2dpt.h
    ${CMAKE_SOURCE_DIR}/thdb2dxm.h
    ${CMAKE_SOURCE_DIR}/thdb2dxs.h
    ${CMAKE_SOURCE_DIR}/thdb3d.h
    ${CMAKE_SOURCE_DIR}/thdouble.h
    ${CMAKE_SOURCE_DIR}/thendscrap.h
    ${CMAKE_SOURCE_DIR}/thendsurvey.h
    ${CMAKE_SOURCE_DIR}/thepsparse.h
    ${CMAKE_SOURCE_DIR}/therion.h
    ${CMAKE_SOURCE_DIR}/thexception.h
    ${CMAKE_SOURCE_DIR}/thexpdb.h
    ${CMAKE_SOURCE_DIR}/thexpmap.h
    ${CMAKE_SOURCE_DIR}/thexpmodel.h
    ${CMAKE_SOURCE_DIR}/thexport.h
    ${CMAKE_SOURCE_DIR}/thexporter.h
    ${CMAKE_SOURCE_DIR}/thexpshp.h
    ${CMAKE_SOURCE_DIR}/thexpsys.h
    ${CMAKE_SOURCE_DIR}/thexptable.h
    ${CMAKE_SOURCE_DIR}/thexpuni.h
    ${CMAKE_SOURCE_DIR}/thfilehandle.h
    ${CMAKE_SOURCE_DIR}/thgeomag.h
    ${CMAKE_SOURCE_DIR}/thgeomagdata.h
    ${CMAKE_SOURCE_DIR}/thgrade.h
    ${CMAKE_SOURCE_DIR}/thchenc.h
    ${CMAKE_SOURCE_DIR}/thimport.h
    ${CMAKE_SOURCE_DIR}/thinfnan.h
    ${CMAKE_SOURCE_DIR}/thinit.h
    ${CMAKE_SOURCE_DIR}/thinput.h
    ${CMAKE_SOURCE_DIR}/thjoin.h
    ${CMAKE_SOURCE_DIR}/thlang.h
    ${CMAKE_SOURCE_DIR}/thlayout.h
    ${CMAKE_SOURCE_DIR}/thlayoutclr.h
    ${CMAKE_SOURCE_DIR}/thlayoutln.h
    ${CMAKE_SOURCE_DIR}/thlegenddata.h
    ${CMAKE_SOURCE_DIR}/thlibrary.h
    ${CMAKE_SOURCE_DIR}/thline.h
    ${CMAKE_SOURCE_DIR}/thlocale.h
    ${CMAKE_SOURCE_DIR}/thlog.h
    ${CMAKE_SOURCE_DIR}/thlogfile.h
    ${CMAKE_SOURCE_DIR}/thlookup.h
    ${CMAKE_SOURCE_DIR}/thmap.h
    ${CMAKE_SOURCE_DIR}/thmapstat.h
    ${CMAKE_SOURCE_DIR}/thmbuffer.h
    ${CMAKE_SOURCE_DIR}/thobjectid.h
    ${CMAKE_SOURCE_DIR}/thobjectname.h
    ${CMAKE_SOURCE_DIR}/thobjectsrc.h
    ${CMAKE_SOURCE_DIR}/thparse.h
    ${CMAKE_SOURCE_DIR}/thpdf.h
    ${CMAKE_SOURCE_DIR}/thpdfdata.h
    ${CMAKE_SOURCE_DIR}/thpdfdbg.h
    ${CMAKE_SOURCE_DIR}/thperson.h
    ${CMAKE_SOURCE_DIR}/thpic.h
    ${CMAKE_SOURCE_DIR}/thpoint.h
    ${CMAKE_SOURCE_DIR}/thproj.h
    ${CMAKE_SOURCE_DIR}/thscan.h
    ${CMAKE_SOURCE_DIR}/thscrap.h
    ${CMAKE_SOURCE_DIR}/thscrapen.h
    ${CMAKE_SOURCE_DIR}/thscrapis.h
    ${CMAKE_SOURCE_DIR}/thscraplo.h
    ${CMAKE_SOURCE_DIR}/thscraplp.h
    ${CMAKE_SOURCE_DIR}/thselector.h
    ${CMAKE_SOURCE_DIR}/thsketch.h
    ${CMAKE_SOURCE_DIR}/thsurface.h
    ${CMAKE_SOURCE_DIR}/thsurvey.h
    ${CMAKE_SOURCE_DIR}/thsvg.h
    ${CMAKE_SOURCE_DIR}/thsvxctrl.h
    ${CMAKE_SOURCE_DIR}/thsymbolset.h
    ${CMAKE_SOURCE_DIR}/thtexenc.h
    ${CMAKE_SOURCE_DIR}/thtexfonts.h
    ${CMAKE_SOURCE_DIR}/thtf.h
    ${CMAKE_SOURCE_DIR}/thtfangle.h
    ${CMAKE_SOURCE_DIR}/thtflength.h
    ${CMAKE_SOURCE_DIR}/thtfpwf.h
    ${CMAKE_SOURCE_DIR}/thtmpdir.h
    ${CMAKE_SOURCE_DIR}/thtrans.h
    ${CMAKE_SOURCE_DIR}/thwarp.h
    ${CMAKE_SOURCE_DIR}/thwarpp.h
    ${CMAKE_SOURCE_DIR}/thwarppdef.h
    ${CMAKE_SOURCE_DIR}/thwarppme.h
    ${CMAKE_SOURCE_DIR}/thwarppt.h
)

# TODO rename these files to .h
set_source_files_properties(
    ${CMAKE_BINARY_DIR}/thchencdata.cxx
    ${CMAKE_SOURCE_DIR}/thlibrarydata.cxx
    PROPERTIES HEADER_FILE_ONLY TRUE)

set(THERION_SOURCES
    ${CMAKE_BINARY_DIR}/thcsdata.cxx
    ${CMAKE_BINARY_DIR}/thchencdata.cxx
    ${CMAKE_BINARY_DIR}/thmpost.cxx
    ${CMAKE_BINARY_DIR}/thsymbolsets.cxx
    ${CMAKE_BINARY_DIR}/thtex.cxx
    ${CMAKE_SOURCE_DIR}/th2ddataobject.cxx
    ${CMAKE_SOURCE_DIR}/tharea.cxx
    ${CMAKE_SOURCE_DIR}/thattr.cxx
    ${CMAKE_SOURCE_DIR}/thbezier.cxx
    ${CMAKE_SOURCE_DIR}/thbuffer.cxx
    ${CMAKE_SOURCE_DIR}/thcmdline.cxx
    ${CMAKE_SOURCE_DIR}/thcomment.cxx
    ${CMAKE_SOURCE_DIR}/thconfig.cxx
    ${CMAKE_SOURCE_DIR}/thcs.cxx
    ${CMAKE_SOURCE_DIR}/thdata.cxx
    ${CMAKE_SOURCE_DIR}/thdatabase.cxx
    ${CMAKE_SOURCE_DIR}/thdataleg.cxx
    ${CMAKE_SOURCE_DIR}/thdataobject.cxx
    ${CMAKE_SOURCE_DIR}/thdatareader.cxx
    ${CMAKE_SOURCE_DIR}/thdatastation.cxx
    ${CMAKE_SOURCE_DIR}/thdate.cxx
    ${CMAKE_SOURCE_DIR}/thdb1d.cxx
    ${CMAKE_SOURCE_DIR}/thdb2d.cxx
    ${CMAKE_SOURCE_DIR}/thdb2d00.cxx
    ${CMAKE_SOURCE_DIR}/thdb2dab.cxx
    ${CMAKE_SOURCE_DIR}/thdb2dcp.cxx
    ${CMAKE_SOURCE_DIR}/thdb2dji.cxx
    ${CMAKE_SOURCE_DIR}/thdb2dlp.cxx
    ${CMAKE_SOURCE_DIR}/thdb2dmi.cxx
    ${CMAKE_SOURCE_DIR}/thdb2dprj.cxx
    ${CMAKE_SOURCE_DIR}/thdb2dpt.cxx
    ${CMAKE_SOURCE_DIR}/thdb2dxm.cxx
    ${CMAKE_SOURCE_DIR}/thdb2dxs.cxx
    ${CMAKE_SOURCE_DIR}/thdb3d.cxx
    ${CMAKE_SOURCE_DIR}/thendscrap.cxx
    ${CMAKE_SOURCE_DIR}/thendsurvey.cxx
    ${CMAKE_SOURCE_DIR}/thepsparse.cxx
    ${CMAKE_SOURCE_DIR}/therion.cxx
    ${CMAKE_SOURCE_DIR}/thexception.cxx
    ${CMAKE_SOURCE_DIR}/thexpdb.cxx
    ${CMAKE_SOURCE_DIR}/thexpmap.cxx
    ${CMAKE_SOURCE_DIR}/thexpmodel.cxx
    ${CMAKE_SOURCE_DIR}/thexport.cxx
    ${CMAKE_SOURCE_DIR}/thexporter.cxx
    ${CMAKE_SOURCE_DIR}/thexpshp.cxx
    ${CMAKE_SOURCE_DIR}/thexpsys.cxx
    ${CMAKE_SOURCE_DIR}/thexptable.cxx
    ${CMAKE_SOURCE_DIR}/thexpuni.cxx
    ${CMAKE_SOURCE_DIR}/thgeomag.cxx
    ${CMAKE_SOURCE_DIR}/thgrade.cxx
    ${CMAKE_SOURCE_DIR}/thchenc.cxx
    ${CMAKE_SOURCE_DIR}/thimport.cxx
    ${CMAKE_SOURCE_DIR}/thinfnan.cxx
    ${CMAKE_SOURCE_DIR}/thinit.cxx
    ${CMAKE_SOURCE_DIR}/thinput.cxx
    ${CMAKE_SOURCE_DIR}/thjoin.cxx
    ${CMAKE_SOURCE_DIR}/thlang.cxx
    ${CMAKE_SOURCE_DIR}/thlayout.cxx
    ${CMAKE_SOURCE_DIR}/thlayoutclr.cxx
    ${CMAKE_SOURCE_DIR}/thlayoutln.cxx
    ${CMAKE_SOURCE_DIR}/thlegenddata.cxx
    ${CMAKE_SOURCE_DIR}/thlibrary.cxx
    ${CMAKE_SOURCE_DIR}/thlibrarydata.cxx
    ${CMAKE_SOURCE_DIR}/thline.cxx
    ${CMAKE_SOURCE_DIR}/thlocale.cxx
    ${CMAKE_SOURCE_DIR}/thlog.cxx
    ${CMAKE_SOURCE_DIR}/thlogfile.cxx
    ${CMAKE_SOURCE_DIR}/thlookup.cxx
    ${CMAKE_SOURCE_DIR}/thmap.cxx
    ${CMAKE_SOURCE_DIR}/thmapstat.cxx
    ${CMAKE_SOURCE_DIR}/thmbuffer.cxx
    ${CMAKE_SOURCE_DIR}/thobjectid.cxx
    ${CMAKE_SOURCE_DIR}/thobjectname.cxx
    ${CMAKE_SOURCE_DIR}/thobjectsrc.cxx
    ${CMAKE_SOURCE_DIR}/thparse.cxx
    ${CMAKE_SOURCE_DIR}/thpdf.cxx
    ${CMAKE_SOURCE_DIR}/thpdfdata.cxx
    ${CMAKE_SOURCE_DIR}/thpdfdbg.cxx
    ${CMAKE_SOURCE_DIR}/thperson.cxx
    ${CMAKE_SOURCE_DIR}/thpic.cxx
    ${CMAKE_SOURCE_DIR}/thpoint.cxx
    ${CMAKE_SOURCE_DIR}/thproj.cxx
    ${CMAKE_SOURCE_DIR}/thscan.cxx
    ${CMAKE_SOURCE_DIR}/thscrap.cxx
    ${CMAKE_SOURCE_DIR}/thscrapen.cxx
    ${CMAKE_SOURCE_DIR}/thscrapis.cxx
    ${CMAKE_SOURCE_DIR}/thscraplo.cxx
    ${CMAKE_SOURCE_DIR}/thscraplp.cxx
    ${CMAKE_SOURCE_DIR}/thselector.cxx
    ${CMAKE_SOURCE_DIR}/thsketch.cxx
    ${CMAKE_SOURCE_DIR}/thsurface.cxx
    ${CMAKE_SOURCE_DIR}/thsurvey.cxx
    ${CMAKE_SOURCE_DIR}/thsvg.cxx
    ${CMAKE_SOURCE_DIR}/thsvxctrl.cxx
    ${CMAKE_SOURCE_DIR}/thsymbolset.cxx
    ${CMAKE_SOURCE_DIR}/thtexfonts.cxx
    ${CMAKE_SOURCE_DIR}/thtf.cxx
    ${CMAKE_SOURCE_DIR}/thtfangle.cxx
    ${CMAKE_SOURCE_DIR}/thtflength.cxx
    ${CMAKE_SOURCE_DIR}/thtfpwf.cxx
    ${CMAKE_SOURCE_DIR}/thtmpdir.cxx
    ${CMAKE_SOURCE_DIR}/thtrans.cxx
    ${CMAKE_SOURCE_DIR}/thwarp.cxx
    ${CMAKE_SOURCE_DIR}/thwarpp.cxx
    ${CMAKE_SOURCE_DIR}/thwarppme.cxx
    ${CMAKE_SOURCE_DIR}/thwarppt.cxx
)
