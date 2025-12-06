# Misfits Carnival Manager 🎪

A comprehensive Firebase-powered carnival management system for tracking events, clubs, tasks, and revenue in real-time.

## 🚀 Features

- **🔥 Firebase Integration** - Real-time database with live collaboration
- **🎭 Carnival Management** - Create and manage multiple carnivals
- **🏢 Club Registration** - Track clubs with different commission types
- **📋 Task Tracking** - Assign and monitor tasks across teams
- **💰 Revenue Analytics** - Real-time revenue tracking and reporting
- **👥 Team Collaboration** - Multi-user real-time synchronization
- **📱 Responsive Design** - Works on all devices

## 🌐 Live Application

**Production URL:** [http://13.201.15.180](http://13.201.15.180)

## 📁 Project Structure

```
misfits-carnival-manager/
├── index.html                      # 🎯 Production application (v2.1.14)
├── deploy_to_production.sh         # 🚀 Deployment script
├── README.md                       # 📖 This file
├── .gitignore                      # Git configuration
├── .claude/                        # Claude configuration
└── archive/                        # 📦 Archived old files
    ├── old-versions/              # Previous HTML versions
    ├── old-scripts/               # Old deployment scripts
    ├── old-docs/                  # Old documentation
    ├── python-scripts/            # Legacy Python scripts
    └── debug-files/               # Debug and test files
```

## 🛠 Setup & Installation

### Prerequisites
- Modern web browser with JavaScript enabled
- Firebase account (for database)
- AWS EC2 instance (for deployment)

### Local Development
1. Start a local web server:
   ```bash
   python3 -m http.server 8000
   ```
2. Open browser to `http://localhost:8000`
3. Firebase will automatically initialize
4. Start creating carnivals and managing tasks

### Production Deployment
```bash
chmod +x deploy_to_production.sh
./deploy_to_production.sh
```

## 🔥 Firebase Configuration

The application is configured with:
- **Database:** Real-time database for live collaboration
- **Auto-clearing:** localStorage cleared on each load to ensure Firebase-only mode
- **Real-time sync:** Changes appear instantly across all users
- **Offline support:** Graceful fallback when Firebase is unavailable

## 🎯 Core Operations

### Creating Carnivals
1. Click "Add Carnival" button
2. Fill in carnival details (name, description, dates)
3. Carnival is automatically saved to Firebase

### Managing Clubs
1. Navigate to "Clubs" tab
2. Register clubs with commission details
3. Assign clubs to specific carnivals

### Task Tracking
1. Create tasks for carnivals or clubs
2. Assign team members and set priorities
3. Update task status in real-time

### Revenue Analytics
1. Track revenue by carnival and club
2. View real-time analytics dashboard
3. Export revenue reports

## 👥 Team Collaboration

- **Multi-tab sync:** Changes sync across browser tabs
- **Real-time updates:** See team member changes instantly
- **Conflict resolution:** Firebase handles concurrent edits
- **Status indicators:** Visual feedback for sync status

## 🔧 Technical Stack

- **Frontend:** HTML5, CSS3 (Tailwind), Vanilla JavaScript
- **Backend:** Firebase Realtime Database
- **Deployment:** AWS EC2 with Nginx
- **Version Control:** Git with GitHub

## 📊 Database Structure

```javascript
{
  carnivals: {
    id: { name, description, startDate, endDate }
  },
  clubs: {
    id: { name, activity, commissionType, carnivals[] }
  },
  tasks: {
    carnivalId: {
      carnivalTasks: [],
      clubs: { clubId: [tasks] }
    }
  },
  revenue: {
    entries by date and club
  }
}
```

## 🚀 Deployment Details

- **Server:** AWS EC2 (13.201.15.180)
- **Web Server:** Nginx
- **SSL:** Ready for HTTPS configuration
- **Domain:** carnival.misfits.net.in (configurable)

## 🔒 Security Features

- **Firebase Security Rules:** Controlled database access
- **Input Validation:** Client-side validation for all forms
- **XSS Protection:** Secure HTML rendering
- **CORS Handling:** Proper cross-origin resource sharing

## 📈 Performance

- **Real-time updates:** < 100ms sync time
- **Offline support:** Works without internet
- **Lazy loading:** Efficient data fetching
- **Compression:** Gzip enabled for faster loading

## 🐛 Troubleshooting

### Firebase Connection Issues
- Check browser console for error messages
- Verify internet connection
- Clear browser cache and localStorage

### Deployment Issues
- Verify AWS EC2 key permissions
- Check server connectivity
- Review nginx configuration

## 📝 Version History

### v2.1.14 (Current) - Enhanced UX & Revenue Fix
- ✅ Toast notifications for club registration
- ✅ Real-time revenue data fetching from Firebase
- ✅ Auto-fetch revenue when opening Revenue Tracking tab
- ✅ Firebase real-time listener for revenue changes
- ✅ Improved project structure with archived old files

### v2.1.10 - Data Contamination Fix
- Fixed calculation issues
- Improved data persistence

### Earlier Versions
- See `archive/old-versions/` for previous versions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📧 Support

For issues or questions, please create an issue in this repository or contact the development team.

## 📄 License

This project is proprietary to Misfits organization. All rights reserved.

---

**🎪 Built for Misfits Carnival Program Management**