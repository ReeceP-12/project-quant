cmake_minimum_required(VERSION 3.20)
project(project_quant_core LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)  # lets editors (VS Code, etc.) get accurate IntelliSense

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

# --- Executable -------------------------------------------------------
# Placeholder target so the project configures and builds out of the box.
# Replace/extend as real sources land in src/.
add_executable(project_quant_core
    src/main.cpp
)

target_include_directories(project_quant_core PRIVATE include)

# --- Warnings -----------------------------------------------------------
if(MSVC)
    target_compile_options(project_quant_core PRIVATE /W4)
else()
    target_compile_options(project_quant_core PRIVATE -Wall -Wextra -Wpedantic)
endif()

# --- Future dependencies -------------------------------------------------
# gRPC + Protobuf (order/control plane) and ZeroMQ (market data plane) will
# be added here via find_package()/FetchContent once proto/ has real
# schemas to generate from. See docs/decisions/0002-grpc-zeromq-ipc.md.
