#!/bin/bash

###############################################################################
#
# build.sh
#
# Author: dgrubb
# Date: 23/02/2016
#
# Creates an installable .deb package for the TofuDoorbell project.
#
###############################################################################

# Project details
readonly PROJECT="TofuDoorbell"
readonly MAJOR_VERSION=0
readonly MINOR_VERSION=0
readonly PACKAGE_VERSION=1
readonly VERSION="$MAJOR_VERSION.$MINOR_VERSION.$PACKAGE_VERSION"

# Build configurations
readonly STAGING_DIR=`pwd`
readonly BUILD_DIR="$STAGING_DIR/${PROJECT}_${VERSION}" # Equivalent to / on target
readonly INSTALL_DIR="$BUILD_DIR/opt/tofu"
readonly CONTROL_INSTALL_DIR="$BUILD_DIR/DEBIAN"

# Build files
readonly CONTROL_FILE="$STAGING_DIR/control"

# Source files
readonly SOURCE_DIR="$STAGING_DIR/.."
readonly APPLICATION_FILE="tofu-doorbell.py"
readonly APPLICATION_PATH="$SOURCE_DIR/$APPLICATION_FILE"
readonly VERSION_FILE="$INSTALL_DIR/tofuversion/tofuversion.py"

# Source directories
readonly TOFUAUDIO_DIR="$SOURCE_DIR/tofuaudio"
readonly TOFUGPIO_DIR="$SOURCE_DIR/tofugpio"
readonly TOFUVERSION_DIR="$SOURCE_DIR/tofuversion"

###############################################################################

do_clean=y
do_validate_dirs=y
do_install_source_files=y
do_generate_control_file=y
do_build_package=y

###############################################################################

msg() {
    echo "[$(date +%Y-%m-%dT%H:%s%z)]: $@" >&2
}

###############################################################################

generate_control_file() {
    msg "Generating control file"
    sed "s/%VERSION_NUM/$VERSION/g" $CONTROL_FILE > $CONTROL_INSTALL_DIR/control
}

###############################################################################

build_package() {
    msg "Building .deb package"
    dpkg-deb --build $BUILD_DIR
}

###############################################################################

clean() {
    msg "Cleaning build directory"
    rm -r $BUILD_DIR
    rm *.deb
}

###############################################################################

validate_dirs() {
    if [ ! -d "$BUILD_DIR" ];then
        msg "Creating build directory: $BUILD_DIR"
        mkdir -p $BUILD_DIR
    fi

    if [ ! -d "$INSTALL_DIR" ];then
        msg "Creating install directory: $INSTALL_DIR"
        mkdir -p $INSTALL_DIR
    fi

    if [ ! -d "$CONTROL_INSTALL_DIR" ];then
        msg "Creating control file install directory: $CONTROL_INSTALL_DIR"
        mkdir -p $CONTROL_INSTALL_DIR
    fi
}

###############################################################################

install_source_files() {
    msg "Installing source files"

    # Install standalone files
    cp -v $APPLICATION_PATH $INSTALL_DIR
    chmod +x $INSTALL_DIR/$APPLICATION_FILE

    # Install directories of content
    cp -vr $TOFUAUDIO_DIR $INSTALL_DIR
    cp -vr $TOFUGPIO_DIR $INSTALL_DIR
    cp -vr $TOFUVERSION_DIR $INSTALL_DIR

    # Ammend version numbers
    sed -i "s/%TOFU_VERSION%/$VERSION/g" $VERSION_FILE
}

###############################################################################
# Start execution
###############################################################################

# Warning: remove all previous build artifacts
if [ $# -gt 0 ]; then
    if [ $1 = "clean" ]; then
        clean
        exit 0
    fi
fi

msg "Building package: $PROJECT $VERSION"

if [ $do_clean = "y" ]; then
    clean
fi

if [ $do_validate_dirs = "y" ]; then
    validate_dirs
fi

if [ $do_install_source_files = "y" ]; then
    install_source_files
fi

if [ $do_generate_control_file = "y" ]; then
    generate_control_file
fi

if [ $do_build_package = "y" ]; then
    build_package
fi

exit 0

###############################################################################
# End execution
###############################################################################
