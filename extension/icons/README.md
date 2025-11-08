# Extension Icons

This folder should contain the extension icons in the following sizes:

- `icon16.png` - 16x16 pixels (toolbar, extension management)
- `icon32.png` - 32x32 pixels (extension management)
- `icon48.png` - 48x48 pixels (extension management)
- `icon128.png` - 128x128 pixels (Chrome Web Store)

## Creating Icons

You can create icons using any graphics software. The recommended design:

### Design Guidelines

- **Colors**: Use the extension's color scheme (purple #7c3aed, pink #ec4899)
- **Symbol**: Brain emoji 🧠 or similar AI/security themed icon
- **Style**: Modern, flat design with gradient
- **Background**: Transparent or gradient matching the theme

### Quick Generation

Use an online tool like:
- https://favicon.io/
- https://realfavicongenerator.net/
- Design in Figma/Canva and export at required sizes

### Temporary Solution

For development/testing, you can use placeholder images or generate simple colored squares with the brain emoji.

### Example SVG (for conversion to PNG)

```svg
<svg width="128" height="128" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#7c3aed;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ec4899;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="24" fill="url(#grad)"/>
  <text x="64" y="80" font-size="64" text-anchor="middle">🧠</text>
</svg>
```

Convert this SVG to PNG at the required sizes using:
- https://cloudconvert.com/svg-to-png
- ImageMagick: `convert icon.svg -resize 16x16 icon16.png`
- Online tools: https://onlineconvertfree.com/convert-format/svg-to-png/
