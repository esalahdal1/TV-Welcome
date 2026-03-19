[app]
title = TV Welcome
package.name = tv_guest_welcome
package.domain = com.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0
requirements = python3,kivy,requests,urllib3,charset-normalizer,idna

orientation = landscape
fullscreen = 1
android.permissions = INTERNET,WAKE_LOCK,RECEIVE_BOOT_COMPLETED

# (Optional) Android-specific settings
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

# For TV support
android.manifest.intent_filters = [{"action": "android.intent.action.MAIN", "category": ["android.intent.category.LAUNCHER", "android.intent.category.LEANBACK_LAUNCHER"]}]

[buildozer]
log_level = 2
warn_on_root = 1
