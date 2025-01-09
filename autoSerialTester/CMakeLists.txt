cmake_minimum_required(VERSION 3.10)
project(SerialPort)

# Specify C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add include directory
include_directories(${PROJECT_SOURCE_DIR}/include)

# Add source files for the library
set(LIBRARY_SOURCES
    src/serial_port.cpp
)

# Add source files for the executable
set(EXECUTABLE_SOURCES
    src/main.cpp
)

# Create the library
add_library(serial_port STATIC ${LIBRARY_SOURCES})

# Set output directory for executables
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# Create the executable
add_executable(serial_port_demo ${EXECUTABLE_SOURCES})

# Link the executable with the library
target_link_libraries(serial_port_demo PRIVATE serial_port)

# Windows-specific configurations
if(WIN32)
    target_link_libraries(serial_port_demo PRIVATE kernel32)
endif()

if(MSVC)
    # Set the subsystem to console for Visual Studio
    target_link_options(serial_port_demo PRIVATE /SUBSYSTEM:CONSOLE)
endif()
