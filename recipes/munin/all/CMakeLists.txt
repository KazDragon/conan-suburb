cmake_minimum_required(VERSION 3.2 FATAL_ERROR)
project(munin_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_subdirectory(source_subfolder)

