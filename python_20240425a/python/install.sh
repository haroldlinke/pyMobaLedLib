#!/bin/sh

# This script adds a menu item, icons and mime type for pyProggen for the current
# user. It will just create and copy a desktop file to the user's dir.
# If called with the "-u" option, it will undo the changes.

# Resource name to use (including vendor prefix)
RESOURCE_NAME=hlinke-pyProgGen

# Get absolute path from which this script file was executed
# (Could be changed to "pwd -P" to resolve symlinks to their target)
SCRIPT_PATH=$( cd $(dirname $0) ; pwd )
cd "${SCRIPT_PATH}"

# Default mode is to install.
UNINSTALL=false

# If possible, get location of the desktop folder. Default to ~/Desktop
XDG_DESKTOP_DIR="${HOME}/Desktop"


# Install by simply copying desktop file
simple_install_f() {

  # Create a temp dir accessible by all users
  TMP_DIR=`mktemp --directory`

  # Create *.desktop file using the existing template file
  sed -e "s,<BINARY_LOCATION>,${SCRIPT_PATH}/pyProg_Generator_MobaLedLib.py,g" \
      -e "s,<ICON_NAME>,${SCRIPT_PATH}/lib/pyproggen.png,g" "${SCRIPT_PATH}/lib/desktop.template" > "${TMP_DIR}/${RESOURCE_NAME}.desktop"

  mkdir -p "${HOME}/.local/share/applications"
  cp "${TMP_DIR}/${RESOURCE_NAME}.desktop" "${HOME}/.local/share/applications/"

  # Copy desktop icon if desktop dir exists (was found)
  if [ -d "${XDG_DESKTOP_DIR}" ]; then
   cp "${TMP_DIR}/${RESOURCE_NAME}.desktop" "${XDG_DESKTOP_DIR}/"
   # Altering file permissions to avoid "Untrusted Application Launcher" error on Ubuntu
   chmod u+x "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop"
  fi

  # Add symlink for pyProgGen so it's in users path
  echo "" # Ensure password request message is on new line
  if ! ln -s ${SCRIPT_PATH}/pyProgGen /usr/local/bin/pyProgGen; then
      echo "Adding symlink failed. Hope that's OK. If not then rerun as root with sudo."
  fi

  # Clean up temp dir
  rm "${TMP_DIR}/${RESOURCE_NAME}.desktop"
  rmdir "${TMP_DIR}"

}

# Uninstall by simply removing desktop files (fallback), incl. old one
simple_uninstall_f() {

  # delete legacy cruft .desktop file
  if [ -f "${HOME}/.local/share/applications/pyProgGen.desktop" ]; then
    rm "${HOME}/.local/share/applications/pyProgGen.desktop"
  fi

  # delete another legacy .desktop file
  if [ -f "${HOME}/.local/share/applications/hlinke-pyProgGen.desktop" ]; then
    rm "${HOME}/.local/share/applications/hlinke-pyProgGen.desktop"
  fi

  if [ -f "${HOME}/.local/share/applications/${RESOURCE_NAME}.desktop" ]; then
    rm "${HOME}/.local/share/applications/${RESOURCE_NAME}.desktop"
  fi

  if [ -f "${HOME}/.local/share/metainfo/${RESOURCE_NAME}.appdata.xml" ]; then
    rm "${HOME}/.local/share/metainfo/${RESOURCE_NAME}.appdata.xml"
  fi

  if [ -f "${XDG_DESKTOP_DIR}/pyProgGen.desktop" ]; then
    rm "${XDG_DESKTOP_DIR}/pyProgGen.desktop"
  fi

  if [ -f "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop" ]; then
    rm "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop"
  fi

  # Remove symlink for pyProgGen
  echo "" # Ensure password request message is on new line
  if ! rm /usr/local/bin/pyProgGen; then
      echo "Removing symlink failed. Hope that's OK. If not then rerun as root with sudo."
  fi

}

# Update desktop file and mime databases (if possible)
updatedbs_f() {

  if [ -d "${HOME}/.local/share/applications" ]; then
    if command -v update-desktop-database > /dev/null; then
      update-desktop-database "${HOME}/.local/share/applications"
    fi
  fi
}

# Shows a description of the available options
display_help_f() {
  printf "\nThis script will add a pyProgGen desktop shortcut, menu item\n"
  printf " for the current user.\n"
  printf "\nOptional arguments are:\n\n"
  printf "\t-u, --uninstall\t\tRemoves shortcut, menu item and icons.\n\n"
  printf "\t-h, --help\t\tShows this help again.\n\n"
}

# Check for provided arguments
while [ $# -gt 0 ] ; do
  ARG="${1}"
  case $ARG in
      -u|--uninstall)
        UNINSTALL=true
        shift
      ;;
      -h|--help)
        display_help_f
        exit 0
      ;;
      *)
        printf "\nInvalid option -- '${ARG}'\n"
        display_help_f
        exit 1
      ;;
  esac
done

if [ ${UNINSTALL} = true ]; then
  printf "Removing desktop shortcut and menu item for pyProgGen..."
  simple_uninstall_f
else
  printf "Adding desktop shortcut and menu item for pyProgGen..."
  simple_uninstall_f
  simple_install_f
fi
updatedbs_f
printf " done!\n"

exit 0
