# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dd4hep(CMakePackage):
    """DD4hep is a software framework for providing a complete solution for
       full detector description (geometry, materials, visualization, readout,
       alignment, calibration, etc.) for the full experiment life cycle
       (detector concept development, detector optimization, construction,
       operation). It offers a consistent description through a single source
       of detector information for simulation, reconstruction, analysis, etc.
       It distributed under the LGPLv3 License."""

    homepage = "https://dd4hep.web.cern.ch/dd4hep/"
    url      = "https://github.com/AIDASoft/DD4hep/archive/v01-12-01.tar.gz"
    git      = "https://github.com/AIDASoft/DD4hep.git"

    maintainers = ['vvolkl', 'drbenmorgan']

    version('master', branch='master')
    version('1.12.1', sha256='85e8c775ec03c499ce10911e228342e757c81ce9ef2a9195cb253b85175a2e93')
    version('1.12.0', sha256='133a1fb8ce0466d2482f3ebb03e60b3bebb9b2d3e33d14ba15c8fbb91706b398')
    version('1.11.2', sha256='96a53dd26cb8df11c6dae54669fbc9cc3c90dd47c67e07b24be9a1341c95abc4')
    version('1.11.1', sha256='d7902dd7f6744bbda92f6e303ad5a3410eec4a0d2195cdc86f6c1167e72893f0')
    version('1.11.0', sha256='25643296f15f9d11ad4ad550b7c3b92e8974fc56f1ee8e4455501010789ae7b6')
    version('1.10.0', sha256='1d6b5d1c368dc8bcedd9c61b7c7e1a44bad427f8bd34932516aff47c88a31d95')

    # Workarounds for various TBB issues in DD4hep v1.11
    # See https://github.com/AIDASoft/DD4hep/pull/613 .
    patch('tbb-workarounds.patch', when='@1.11.0')
    patch('tbb2.patch', when='@1.12.1')

    variant('xercesc', default=False, description="Enable 'Detector Builders' based on XercesC")
    variant('geant4', default=False, description="Enable the simulation part based on Geant4")
    variant('testing', default=False, description="Enable and build tests")

    depends_on('cmake @3.12:', type='build')
    depends_on('boost @1.49:')
    depends_on('root @6.08: +gdml +math +opengl +python +x')
    extends('python')
    depends_on('xerces-c', when='+xercesc')
    depends_on('geant4@10.2.2:', when='+geant4')

    def cmake_args(self):
        spec = self.spec
        cxxstd = spec['root'].variants['cxxstd'].value
        # root can be built with cxxstd=11, but dd4hep requires 14
        if cxxstd == "11":
            cxxstd = "14"
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(cxxstd),
            "-DDD4HEP_USE_XERCESC={0}".format(spec.satisfies('+xercesc')),
            "-DDD4HEP_USE_GEANT4={0}".format(spec.satisfies('+geant4')),
            "-DBUILD_TESTING={0}".format(spec.satisfies('+testing')),
            "-DBOOST_ROOT={0}".format(spec['boost'].prefix),
            "-DBoost_NO_BOOST_CMAKE=ON",
            "-DPYTHON_EXECUTABLE={0}".format(spec['python'].command.path),
        ]
        return args

    def url_for_version(self, version):
        # dd4hep releases are dashes and padded with a leading zero
        # the patch version is omitted when 0
        # so for example v01-12-01, v01-12 ...
        major = (str(version[0]).zfill(2))
        minor = (str(version[1]).zfill(2))
        patch = (str(version[2]).zfill(2))
        if version[2] == 0:
            url = "https://github.com/AIDASoft/DD4hep/archive/v%s-%s.tar.gz" % (major, minor)
        else:
            url = "https://github.com/AIDASoft/DD4hep/archive/v%s-%s-%s.tar.gz" % (major, minor, patch)
        return url
