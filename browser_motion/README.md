# Frame-exact HTML/CSS/Canvas → MP4 motion graphics

Original independently written browser renderer (not copied from third-party skills). Uses `puppeteer-core`, local Chrome/Edge/Chromium, and FFmpeg.

```powershell
cd browser_motion
npm.cmd install
npm.cmd run smoke
npm.cmd run preview
```

Every frame calls `window.renderAt(frame/fps)`, waits for Urdu fonts, screenshots the browser Canvas, and streams PNG frames into FFmpeg H.264 with CRF 18. It's **deterministic** and renderable on Windows or Linux. No video or web UI is screen-recorded in real time. The source HTML is editable.

The example shows an illustrative land-parcel model and reported file comparison. It's not real land mapping. The motion graphics should be composited into real video at narrated cues via FFmpeg or Remotion. Use Blender for actual photoreal 3D shots.

External inspiration to install separately: /motion by abhimahamkali (upstream repo lacks a visible explicit license; never vendor as our own code); JakeB-5/motion-graphic-skill and haidrrrry/claude-remotion-skill are MIT-licensed alternatives. Always respect source licenses, publisher terms and assets.

```powershell
npx skills add abhimahamkali/claude-motion-skill -g
npx skills add JakeB-5/motion-graphic-skill --skill motion-graphic
```

External skills must be installed deliberately in an appropriate AI agent runtime. They do not become executable inside the ChatGPT chat environment merely because SKILL.md exists.
