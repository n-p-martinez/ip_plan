# 4K Pursuit

Personal training plan and log for the 2026-27 4 km individual pursuit season.

- **iPhone and Android (web app):** https://n-p-martinez.github.io/ip_plan/ — open in Safari (iPhone) or Chrome (Android), then Share → *Add to Home Screen* / ⋮ → *Install app*.
- **Android app (APK):** [latest build](https://github.com/n-p-martinez/ip_plan/releases/download/android/4K-Pursuit.apk).

Everything you log (sessions, RPE, minutes, notes, weight, changed sessions) is stored on the phone only. Use **Numbers → Your data → Export log** to back it up or send it for a plan review.

## Updating the plan

```
python3 build/build.py path/to/IP_Season_Plan_2026-27.xlsx
git commit -am "Plan update" && git push
```

`web/plan.json` is what installed apps download on launch, so plan changes reach both the web app and the APK without reinstalling. Changes to `build/app.template.html` (app code) rebuild the APK automatically.

The Android signing key in `android/ip4k.keystore` is a personal debug key, kept in the repo on purpose so every build installs over the previous one.

# Shopping List

A grocery checklist that works with no signal. It lives in this repo but is a separate app with its own data.

- **Web app:** https://n-p-martinez.github.io/ip_plan/shopping/ — Chrome → ⋮ → *Install app*.
- **Android app (APK):** [latest build](https://github.com/n-p-martinez/ip_plan/releases/download/shopping-android/Shopping-List.apk). In the Android app you can paste a recipe link (or Share → Shopping List from Chrome) to add its ingredients.
- **From Claude:** paste a `SHOPLIST:` code into *Import from Claude*.

App code is `web/shopping/index.html`; `shopping/` holds the Android wrapper. Pushing changes to either rebuilds the APK (`.github/workflows/shopping-android.yml`). The 4K Pursuit service worker skips `/shopping/` so the two apps never share cached pages.
