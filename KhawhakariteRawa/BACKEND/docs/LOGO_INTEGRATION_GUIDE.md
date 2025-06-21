# Logo Integration Guide

## Steps to Add Your Logo

1. **Save the Logo Image**
   - Save your beautiful Kaiwhakarite Rawa logo image as `logo.png`
   - Place it in the `client/public/assets/` directory
   - The path should be: `client/public/assets/logo.png`

2. **Logo Requirements**
   - Format: PNG (recommended) or SVG
   - Size: Recommended 200x200px or larger (will be scaled automatically)
   - Background: Transparent preferred
   - Quality: High resolution for crisp display

3. **Already Integrated Features**
   - ✅ Login page logo display (20x20 size)
   - ✅ Sidebar logo display (10x10 size)  
   - ✅ Fallback to "KR" text if logo fails to load
   - ✅ Responsive design for different screen sizes

4. **Fallback System**
   - If the logo image fails to load, the system will automatically show a green "KR" badge
   - This ensures the interface always looks professional

## Quick Setup Command

```bash
# Create the assets directory if it doesn't exist
mkdir -p client/public/assets

# Copy your logo file to the correct location
# (Replace 'path/to/your/logo.png' with actual path)
cp path/to/your/logo.png client/public/assets/logo.png
```

## Verification

After adding the logo:
1. Restart your React development server
2. Visit http://localhost:3000
3. You should see your logo on the login page and in the sidebar
4. If you see "KR" instead, check that the file path is correct

## Logo Locations in Code

The logo is referenced in:
- `client/src/pages/Auth/Login.js` - Login page header
- `client/src/components/Layout/Layout.js` - Sidebar (both mobile and desktop)

Both locations include error handling to show the "KR" fallback if needed. 