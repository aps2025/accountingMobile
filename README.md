# Bill Manager - Offline Mobile App

A standalone offline mobile application for managing recurring bills. Built with Flutter framework, runs on Android and iOS without requiring an internet connection.

## 🌟 Features

- **Full Bill Management**: Add, edit, delete bills with offline functionality
- **Financial Analytics**: Real-time monthly and yearly total calculations
- **Frequency Conversion**: Automatic conversion between weekly, monthly, and yearly frequencies
- **Completely Offline**: No server needed, data stored locally on device
- **Mobile-Optimized**: Touch-friendly interface with Material Design
- **Cross-Platform**: Runs on Android, iOS, and desktop (Mac/Windows/Linux)

## 📱 Quick Start

### Prerequisites

- Flutter SDK 3.16.0 or higher
- For Android: Android Studio and SDK
- For iOS: macOS, Xcode, CocoaPods

### Installation

```bash
# Clone the repository
git clone https://github.com/aps2025/accountingMobile.git
cd accountingMobile/accounting_flutter

# Install dependencies
flutter pub get
```

### Running the App

**Test on Desktop:**
```bash
cd accounting_flutter
flutter run
```

**Build for Android:**
```bash
cd accounting_flutter
flutter build apk --release
```

**Build for iOS (Mac only):**
```bash
cd accounting_flutter
flutter build ios --release
```

## 📂 Project Structure

```
accountingMobile/
├── accounting_flutter/       # Flutter application
│   ├── lib/
│   │   ├── main.dart        # App entry point
│   │   ├── models/          # Data models
│   │   ├── database/        # SQLite database management
│   │   ├── services/        # Business logic (calculator, validators)
│   │   └── screens/         # UI screens
│   ├── pubspec.yaml         # Flutter dependencies
│   └── android/             # Android-specific files
├── accounting/              # Legacy Kivy version (deprecated)
├── .github/workflows/       # GitHub Actions CI/CD
│   ├── build-flutter-apk.yml # Flutter APK build
│   └── build-apk.yml        # Legacy Buildozer build (deprecated)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

##  Data Storage

- **Database**: SQLite stored locally on device using sqflite
- **Location**: 
  - Android: App's private data directory
  - Desktop: Local app directory
- **Offline**: No internet connection required
- **Privacy**: All data stays on your device

## 🚀 Deployment

### Android Deployment

1. Install Android Studio and SDK
2. Build APK: `flutter build apk --release`
3. Transfer APK to device and install

### iOS Deployment (Mac only)

1. Install Xcode and CocoaPods
2. Build IPA: `flutter build ios --release`
3. Deploy using Xcode or TestFlight

### GitHub Actions

The project includes automated APK building via GitHub Actions. Push to main branch to trigger automatic build.

## 🛠️ Development

### Modify the UI

Edit files in `lib/screens/` to customize:
- Colors, layout, and fields
- Touch interactions and navigation

### Add New Features

Reuse services:
```dart
import '../services/calculator.dart';
import '../database/database_helper.dart';

final calculator = BillCalculator();
final dbHelper = DatabaseHelper.instance;
```

## 📝 License

Free to use and modify.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions:
1. Check [Flutter documentation](https://flutter.dev/docs)
2. Review [sqflite documentation](https://pub.dev/packages/sqflite)
