[app]

# Application title
title = Bill Manager

# Package name
package.name = billmanager

# Package domain
package.domain = org.billmanager

# Source directory
source.dir = .

# Source includes (include all Python files)
source.include_exts = py,png,jpg,kv,atlas,db

# Version
version = 1.0

# Requirements
requirements = python3,kivy

# Permissions (Android)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Features
android.features = android.hardware.screen.portrait

# Orientation
orientation = portrait

# Icon and presplash (optional)
# icon.filename = %(source.dir)s/data/icon.png
# presplash.filename = %(source.dir)s/data/presplash.png

# Android-specific settings
[app:android]

# Android SDK version
android.api = 33

# Android NDK version
android.ndk = 25.1.8937393

# Android build tools version
android.build_tools = 33.0.0

# Use gradle instead of ant (more reliable)
android.gradle_dependencies =

# Skip gradle wrapper
android.skip_update = False

# Skip SDK update (use pre-installed SDK)
android.skip_sdk_update = True

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warnings
warn_on_root = 1
