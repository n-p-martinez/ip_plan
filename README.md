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
