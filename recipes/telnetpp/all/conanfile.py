import os
from conans import ConanFile, tools, CMake

class TelnetppConan(ConanFile):
    name = "telnetpp"
    homepage = "https://github.com/KazDragon/telnetpp"
    description = "A library for handling the Telnet protocol"
    topics = ("telnet", "conan", "telnet-protocol", "telnet-layer", "mccp",
              "msdp", "rfc-1153", "rfc-857", "rfc-858", "rfc-1091", "rfc-1950",
              "rfc-1572", "rfc-1053", "rfc-854", "telnet-session")
    url = "https://github.com/KazDragon/conan-suburb"
    license = "MIT"
    exports = "*.hpp", "*.in", "*.cpp", "CMakeLists.txt", "*.md", "LICENSE"
    exports_sources = "CMakeLists.txt", "patches/**"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "withZlib": [True, False],
        "coverage": [True, False],
        "sanitize": ["off", "address"],
        "withTests": [True, False]
    }
    default_options = {
        "shared": False,
        "withZlib": True,
        "coverage": False,
        "sanitize": "off",
        "withTests": False
    }
    generators = "cmake"

    _cmake = None
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def requirements(self):
        self.requires("boost/[>=1.69]")
        self.requires("gsl-lite/[=0.34]")
        if (self.options.withZlib):
            self.requires("zlib/[>=1.2.11]")
        if (self.options.withTests):
            self.build_requires("gtest/[>=1.8.1]")

    def configure(self):
        self.options["boost"].without_test = True

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("telnetpp-{}".format(self.version), self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        self._cmake.definitions["TELNETPP_WITH_ZLIB"] = self.options.withZlib
        self._cmake.definitions["TELNETPP_COVERAGE"] = self.options.coverage
        self._cmake.definitions["TELNETPP_SANITIZE"] = self.options.sanitize
        self._cmake.definitions["TELNETPP_WITH_TESTS"] = self.options.withTests
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def _patch_sources(self):
        if "patches" in self.conan_data and self.version in self.conan_data["patches"]:
            for patch in self.conan_data["patches"][self.version]:
                tools.patch(**patch)

    def build(self):
        self._patch_sources()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("*.hpp", dst="include", src="source_subfolder/include")
        self.copy("*.lib", dst="lib", src="source_subfolder/lib", keep_path=False)
        self.copy("*.dll", dst="bin", src="source_subfolder/bin", keep_path=False)
        self.copy("*.dylib", dst="bin", src="source_subfolder/lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["telnetpp"]

