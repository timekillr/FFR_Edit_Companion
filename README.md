# FFR Edit Companion

Android and local browser companions for [FFR Edit](https://github.com/timekillr/FFR_Edit), a Decky save editor for Final Fantasy Resonance. Initial version 0.1.0. Saves and backups stay on the Steam Deck/Linux machine. The companion requires the plugin; it does not edit saves stored on Android.

## Install and pair

1. Install `FFR_Edit_Companion.apk` from [Releases](https://github.com/timekillr/FFR_Edit_Companion/releases/latest). Android 8.0+ is required.
2. In the Decky plugin, open Connection, enable Phone & web companion and create a code.
3. On the same home network, enter the machine's address (`192.168.x.x:52882`) and pairing code in the app. Compare the fingerprint with Decky, then approve pairing.
4. Open Saves, scan, select a slot and edit. Changes are staged until Save changes. Backup now and Restore work against the machine's backup archive.

The APK is a debug-signed development build for sideloading, not Play Store signed. Until a stable release-signing key is configured, a later CI build can require uninstalling the previous APK and pairing again.

For a web browser, use the HTTPS address shown in Decky. The plugin serves the companion directly on your LAN; no internet hosting or port forwarding is needed. Compare the certificate SHA-256 fingerprint with Decky before accepting the local certificate. Web clients use a secure HttpOnly cookie; Android uses certificate pinning and an encrypted Android Keystore credential. Pairings are remembered, independently revocable, and survive app restart.

Connection has manual Reconnect/Disconnect. Automatic read retries stop after ten seconds. Writes are never automatically retried. Concurrent edits are rejected if another client or Steam changes the save. Game-running checks, automatic/manual backups and restore validation happen in the plugin, regardless of client.

## Build

JDK 17 and Android SDK 37.0/build-tools 36.0.0:

```sh
./gradlew :app:testDebugUnitTest :app:assembleDebug
```

The web UI is `app/src/main/assets/` (identical to plugin web UI except Android uses its native pinned transport instead of browser-bridge.js). `web/` is a standalone distributable copy for bundling with the plugin; it must be served by the plugin's same-origin HTTPS endpoint, not opened as a file or hosted on a separate public origin.

The release workflow produces a sideloadable APK and web ZIP after tests. A real device and in-game save-load test is still required for the initial release. Use a spare save slot initially.

## Credits

GPL-3.0-only, adapted from timekillr's Value Forge Companion HTTPS/pairing shell. The backend port uses Jesús Seijas's MIT FFR Save Editor; see the plugin repository's original licenses and notices. No game art is bundled. Unofficial, not endorsed by Square Enix.
