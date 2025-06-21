# 🎨 Logo Setup Guide for Kaiwhakarite Rawa

## 📋 Overview

This guide shows you how to add your custom logo to the **Kaiwhakarite Rawa** Resource Management System. Your logo will appear in:

- 🔐 **Login Screen** - Main branding area
- 🏠 **Dashboard Header** - Navigation bar
- 📱 **Browser Tab** - Favicon
- 📄 **Reports & Documents** - Letterhead
- 📧 **Email Templates** - Branding

---

## 🎯 Step 1: Prepare Your Logo Files

### Required Logo Formats:

1. **📱 Main Logo (SVG/PNG)**
   - **Recommended:** SVG format (scalable)
   - **Alternative:** High-resolution PNG (300+ DPI)
   - **Size:** 200x60 pixels (approx)
   - **Background:** Transparent or white

2. **🌐 Favicon (ICO/PNG)**
   - **Format:** ICO or PNG
   - **Size:** 32x32 pixels minimum
   - **Background:** Transparent

3. **📄 Square Logo (PNG/SVG)**
   - **Format:** PNG or SVG
   - **Size:** 64x64 pixels
   - **Use:** Dashboard icons, small displays

### 📁 File Naming Convention:
```
logo-main.svg          # Primary logo
logo-square.png        # Square version
favicon.ico            # Browser favicon
logo-white.svg         # White version (for dark backgrounds)
```

---

## 🔧 Step 2: Add Logo Files to Project

### Frontend (React) Logos:

1. **Create logo directory:**
   ```bash
   mkdir client/public/images
   mkdir client/src/assets/images
   ```

2. **Add your logo files:**
   ```bash
   # Copy your files to:
   client/public/images/logo-main.svg
   client/public/images/logo-square.png
   client/public/favicon.ico
   client/src/assets/images/logo-white.svg
   ```

### Backend (Python) Logos:

1. **Create static directory:**
   ```bash
   mkdir server/static/images
   ```

2. **Add logo files:**
   ```bash
   # Copy your files to:
   server/static/images/logo-main.svg
   server/static/images/logo-letterhead.png
   ```

---

## 🎨 Step 3: Update Frontend Components

### A. Update Login Screen Logo

Edit `client/src/App.js` - LoginPage component:

```javascript
// Replace the SVG icon with your logo
<div className="mx-auto h-20 w-20 bg-emerald-600 rounded-full flex items-center justify-center mb-6">
  <img 
    src="/images/logo-main.svg" 
    alt="Kaiwhakarite Rawa Logo"
    className="h-12 w-12"
  />
</div>
```

### B. Update Dashboard Header Logo

Edit `client/src/App.js` - Dashboard component:

```javascript
// Replace the header logo section
<div className="flex items-center">
  <div className="h-10 w-10 bg-emerald-600 rounded-lg flex items-center justify-center mr-3">
    <img 
      src="/images/logo-square.png" 
      alt="Logo"
      className="h-8 w-8"
    />
  </div>
  <div>
    <h1 className="text-xl font-bold text-gray-900">Your Organization Name</h1>
    <p className="text-sm text-gray-500">Resource Management System</p>
  </div>
</div>
```

### C. Update Browser Favicon

Edit `client/public/index.html`:

```html
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/images/logo-square.png" />
```

---

## 🏢 Step 4: Customize Organization Details

### A. Update System Names

Edit `client/src/App.js` and replace:

```javascript
// Change system title
<h2 className="text-4xl font-bold text-gray-900 mb-2">Your Organization Name</h2>
<p className="text-lg text-gray-600 mb-2">Resource Management System</p>
<p className="text-sm text-emerald-600 font-medium">Taputapu Whakahaere Rauemi</p>
```

### B. Update Welcome Messages

Find and customize the welcome messages for each role:

```javascript
// Admin welcome
title: 'Welcome, Administrator',
subtitle: 'Nau mai, Kaiwhakahaere',
description: 'You have full system access to manage all resources, users, and settings.'

// Manager welcome  
title: 'Welcome, Manager',
subtitle: 'Nau mai, Kaiwhakahaere',
description: 'You can manage inventory, approve bookings, and oversee user activities.'

// User welcome
title: 'Welcome, User', 
subtitle: 'Nau mai, Kaiwhakamahi',
description: 'You can browse inventory, make bookings, and manage your profile.'
```

---

## 🎨 Step 5: Color Scheme Customization

### A. Update Primary Colors

Edit `client/src/index.css` or add to `tailwind.config.js`:

```css
:root {
  --primary-color: #your-brand-color;
  --secondary-color: #your-secondary-color;
}

/* Or update Tailwind config */
module.exports = {
  theme: {
    extend: {
      colors: {
        'brand': {
          50: '#your-light-shade',
          500: '#your-main-color',
          600: '#your-darker-shade',
        }
      }
    }
  }
}
```

### B. Replace Emerald Colors

Find and replace throughout the codebase:
- `emerald-600` → `brand-600`
- `emerald-500` → `brand-500`
- `emerald-50` → `brand-50`

---

## 📄 Step 6: Backend Logo Integration

### A. Update Email Templates

Create `server/templates/email_template.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{subject}}</title>
</head>
<body>
    <div style="max-width: 600px; margin: 0 auto;">
        <header style="text-align: center; padding: 20px;">
            <img src="{{base_url}}/static/images/logo-main.svg" 
                 alt="Organization Logo" 
                 style="height: 60px;">
            <h1>Your Organization Name</h1>
        </header>
        <div style="padding: 20px;">
            {{content}}
        </div>
    </div>
</body>
</html>
```

### B. Update PDF Reports

Edit report generation functions in `server/utils/` to include your logo.

---

## 🚀 Step 7: Quick Implementation

### Copy-Paste Logo Update (React)

1. **Add your logo to:** `client/public/images/logo.svg`

2. **Update App.js with this simple replacement:**

```javascript
// Find this line in LoginPage:
<svg className="h-12 w-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">

// Replace entire div with:
<img src="/images/logo.svg" alt="Logo" className="h-12 w-12" />

// Find this line in Dashboard:  
<svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">

// Replace entire div with:
<img src="/images/logo.svg" alt="Logo" className="h-6 w-6" />
```

---

## 🎯 Example: Complete Logo Implementation

Here's a working example using a custom logo:

```javascript
// LoginPage logo section
<div className="mx-auto h-20 w-20 bg-white rounded-full flex items-center justify-center mb-6 shadow-lg">
  <img 
    src="/images/your-logo.svg" 
    alt="Your Organization"
    className="h-16 w-16 object-contain"
  />
</div>

// Dashboard header
<div className="flex items-center">
  <img 
    src="/images/your-logo.svg" 
    alt="Logo"
    className="h-10 w-auto mr-3"
  />
  <div>
    <h1 className="text-xl font-bold text-gray-900">Your Organization</h1>
    <p className="text-sm text-gray-500">Kaiwhakarite Rawa</p>
  </div>
</div>
```

---

## 🔍 Testing Your Logo

1. **Start the frontend:** `npm start` in the `client` folder
2. **Check these pages:**
   - ✅ Login screen - Logo appears correctly
   - ✅ Dashboard header - Logo fits well
   - ✅ Browser tab - Favicon shows
   - ✅ All user roles - Consistent branding

---

## 🛠️ Troubleshooting

### Logo Not Showing?
- ✅ Check file path is correct
- ✅ Ensure file is in `public` folder (not `src`)
- ✅ Clear browser cache
- ✅ Check browser console for errors

### Logo Too Big/Small?
- 🎯 Adjust `className` dimensions (`h-8 w-8`, `h-12 w-12`)
- 🎯 Use `object-contain` or `object-cover`
- 🎯 Set specific width: `style={{width: '150px'}}`

### Poor Quality?
- 📱 Use SVG format for crisp scaling
- 📱 Ensure high-resolution PNG (300+ DPI)
- 📱 Optimize images before upload

---

## 🎉 Final Result

Your **Kaiwhakarite Rawa** system will now feature:

- 🏢 **Your organization's branding** throughout the interface
- 🎨 **Consistent visual identity** across all user roles
- 📱 **Professional appearance** that reflects your organization
- 🌐 **Custom favicon** in browser tabs
- 📄 **Branded reports and communications**

---

**🚀 Ready to showcase your branded Resource Management System!** 