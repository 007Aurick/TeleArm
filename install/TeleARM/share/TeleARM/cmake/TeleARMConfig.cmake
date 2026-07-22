# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_TeleARM_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED TeleARM_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(TeleARM_FOUND FALSE)
  elseif(NOT TeleARM_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(TeleARM_FOUND FALSE)
  endif()
  return()
endif()
set(_TeleARM_CONFIG_INCLUDED TRUE)

# output package information
if(NOT TeleARM_FIND_QUIETLY)
  message(STATUS "Found TeleARM: 0.0.0 (${TeleARM_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'TeleARM' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${TeleARM_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(TeleARM_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${TeleARM_DIR}/${_extra}")
endforeach()
