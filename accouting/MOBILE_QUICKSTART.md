# Mobile App - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Requirements (2 min)

```bash
pip install kivy buildozer
```

### Step 2: Test on Computer (1 min)

```bash
cd c:\Users\al12918\source\mine\0527\accouting
python mobile_app.py
```

Window opens showing the mobile app interface. Test adding bills.

### Step 3: Build Android APK (10-15 min, first time only)

```bash
buildozer android debug
```

**Wait for completion.** APK created at: `bin/billmanager-1.0-debug.apk`

### Step 4: Install on Phone

**Option A: Using USB Cable (Recommended)**
```bash
adb install bin/billmanager-1.0-debug.apk
```

**Option B: Manual**
1. Copy APK to phone via USB
2. Open file manager on phone
3. Tap APK to install

### Step 5: Done!

Open "Bill Manager" app on your phone. It works completely offline!

---

## Common Issues & Fixes

### "buildozer: command not found"
```bash
pip install buildozer --upgrade
```

### "Java not found"
- Download Java from: https://www.oracle.com/java/technologies/downloads/
- Restart terminal after installation

### "Android SDK not found"
- Download Android Studio: https://developer.android.com/studio
- Set environment variable:
  ```bash
  setx ANDROID_SDK_ROOT "C:\Android\Sdk"
  ```

### APK Installation Fails
```bash
# Enable Unknown Sources on phone:
# Settings → Security → Unknown Sources (toggle ON)

# Then try again:
adb install bin/billmanager-1.0-debug.apk
```

### App Crashes on Startup
Check if all backend files exist in same folder:
- ✓ database.py
- ✓ models.py
- ✓ calculator.py
- ✓ validators.py
- ✓ mobile_app.py

---

## What You Get

✅ Standalone mobile app (no server needed)
✅ Works completely offline
✅ Data stored locally on phone
✅ Same features as web version
✅ Touch-friendly interface
✅ Fast and lightweight

---

## Next Steps

1. **Test on phone** - Add some bills
2. **Customize** - Edit colors/layout in `mobile_app.py`
3. **Share** - Send APK to friends
4. **Publish** - Upload to Google Play Store (optional)

---

## File Sizes

- APK: ~50-80 MB
- Installed: ~100-150 MB
- Database: < 1 MB

---

## Uninstall

```bash
adb uninstall org.billmanager
```

Or manually: Settings → Apps → Bill Manager → Uninstall

---

## Questions?

See `MOBILE_README.md` for detailed documentation.
