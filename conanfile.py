#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os, platform


class LibnameConan(ConanFile):
    name = "gnu-m4"
    version = "1.4.18"
    description = "GNU M4 is an implementation of the traditional Unix macro processor."
    url = "https://github.com/helmesjo/conan-gnu-m4"
    homepage = "https://www.gnu.org/software/m4/m4.html"
    author = "helmesjo <helmesjo@gmail.com>"
    license = "GPLv3"
    exports = ["LICENSE.md"]
    
    settings = "os", "arch", "build_type"
    options = {"fPIC": [True, False]}
    default_options = "fPIC=True"
    
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    
    requires = ()

    def requirements(self):
        if tools.os_info.is_windows:
            self.requires.add("cygwin_installer/2.9.0@bincrafters/stable")

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "http://ftp.gnu.org/gnu/m4/"
        extracted_dir = "m4-{}".format(self.version)
        tools.get("{}/{}.tar.gz".format(source_url, extracted_dir))
        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

        # Extract the License/s from the header to a file
        with tools.chdir(self.source_subfolder):
            tmp = tools.load("src/m4.h")
            license_contents = tmp[2:tmp.find("*/", 1)] # The license begins with a C comment /* and ends with */
            license_filename = "license-{}".format(self.name)
            tools.save(license_filename, license_contents)

    def configure_autotools(self):
        env_build = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        if self.settings.os != "Windows":
            env_build.fpic = self.options.fPIC
        
        if tools.os_info.is_windows:
            env_build.subsystem = "cygwin"

        return env_build

    def build(self):
        with tools.chdir(self.source_subfolder):
            env_build = self.configure_autotools()
            env_build.configure()
            env_build.make()

    def package(self):
        self.copy("license*", dst="licenses", ignore_case=True, src=self.source_subfolder)
        
        with tools.chdir(self.source_subfolder):
            env_build = self.configure_autotools()
            env_build.install()

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
