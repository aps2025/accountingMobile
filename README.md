# Bill Manager - Offline Mobile App

A standalone offline mobile application for managing recurring bills. Built with Kivy framework, runs on Android and iOS without requiring an internet connection.

## 🌟 Features

- **Full Bill Management**: Add, edit, delete bills with offline functionality
- **Financial Analytics**: Real-time monthly and yearly total calculations
- **Frequency Conversion**: Automatic conversion between weekly, monthly, and yearly frequencies
- **Completely Offline**: No server needed, data stored locally on device
- **Mobile-Optimized**: Touch-friendly interface with portrait orientation
- **Cross-Platform**: Runs on Android, iOS, and desktop (Mac/Windows/Linux)

## 📱 Quick Start

### Prerequisites

- Python 3.6+
- For Android: Java JDK, Android SDK, Buildozer
- For iOS: macOS, Xcode, iOS SDK

### Installation

```bash
# Clone the repository
git clone https://github.com/aps2025/accountingMobile.git
cd accountingMobile/accounting

# Install dependencies
pip install -r requirements.txt
```

### Running the App

**Test on Desktop:**
```bash
cd accounting
python mobile_app.py
```

**Build for Android:**
```bash
cd accounting
buildozer android debug
```

**Build for iOS (Mac only):**
```bash
cd accounting
buildozer ios debug
```

## 📂 Project Structure

```
accountingMobile/
├── accounting/              # Main application code
│   ├── mobile_app.py       # Kivy mobile app
│   ├── database.py         # SQLite database management
│   ├── models.py           # Data models
│   ├── calculator.py       # Financial calculations
│   ├── validators.py       # Input validation
│   ├── buildozer.spec      # Build configuration
│   ├── requirements.txt    # Python dependencies
│   └── MOBILE_README.md    # Detailed mobile documentation
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 📖 Documentation

- [Mobile App Guide](accounting/MOBILE_README.md) - Detailed mobile app documentation
- [Quick Start Guide](accounting/MOBILE_QUICKSTART.md) - Quick setup instructions
- [Web Version Guide](accounting/WEB_README.md) - Web app documentation

## 🔧 Data Storage

- **Database**: SQLite stored locally on device
- **Location**: 
  - Android: `/data/data/org.billmanager/files/bills.db`
  - Desktop: `accounting/bills.db` (auto-created on first run)
- **Offline**: No internet connection required
- **Privacy**: All data stays on your device

## 🚀 Deployment

### Android Deployment

1. Install Android Studio and SDK
2. Install Java JDK
3. Install Buildozer: `pip install buildozer`
4. Build APK: `buildozer android debug`
5. Transfer APK to device and install

### iOS Deployment (Mac only)

1. Install Xcode
2. Build IPA: `buildozer ios debug`
3. Deploy using Xcode or TestFlight

### Desktop Deployment

Simply run: `python accounting/mobile_app.py`

## 🛠️ Development

### Modify the UI

Edit `accounting/mobile_app.py` to customize:
- Colors, layout, and fields
- Touch interactions and navigation

### Add New Features

Reuse backend modules:
```python
from models import BillRepository
from calculator import BillCalculator

repository = BillRepository()
calculator = BillCalculator(repository)
```

## 📝 License

Free to use and modify.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions:
1. Check the [troubleshooting section](accounting/MOBILE_README.md#troubleshooting)
2. Review [Kivy documentation](https://kivy.org/doc/stable/)
3. Check [Buildozer docs](https://buildozer.readthedocs.io/)
