# YouTube private upload — setup and safety

The completed PPG film is currently hosted at GitHub Release ppg-410s-editorial-1080p60-review-20261017. It has NOT been uploaded to YouTube by this workflow as of the documentation date.

## Why vidIQ access is not enough

vidIQ can show the linked channel ID and edit owned-video metadata if available. Its media-import action imports videos into vidIQ hosting and is **not** a YouTube new-video upload. The GitHub Actions workflow cannot borrow/extract vidIQ's private OAuth tokens. A separate authorized official YouTube Data API OAuth connection is necessary.

The identified channel is Pakistan Property Group, ID UCdQu7MU5dHhaClhkCdG2BKg, @shahidhameed-b6k. Confirm this exact channel before uploading.

## Once-only OAuth configuration by the account owner

1. Open Google Cloud Console in your own account and create or select a project. Enable YouTube Data API v3.
2. Configure the authorized OAuth consent screen. Create an OAuth client that supports the local authorization flow appropriate to your app. Review Google's publishing/verification requirements; test-mode tokens can expire after a short period depending on scope and app status.
3. Authorize the YouTube channel owner via the official Google OAuth consent screen with the least scopes required. This implementation uses youtube.upload plus youtube.readonly for channel verification. Request offline access and capture the resulting refresh token **privately**; do not paste it into ChatGPT, GitHub source or logs.
4. In GitHub repo Settings → Secrets and variables → Actions, store YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET and YOUTUBE_REFRESH_TOKEN as encrypted repository secrets.
5. Review source legal claims, licenses, final narration, thumbnail, title, description, audience declaration and privacy. Publishing a video with real allegations requires editorial review; this workflow does not perform the editorial approval for you.
6. Go to Actions → YouTube — Verified PRIVATE Documentary Upload → Run workflow. Enter the exact Release tag, target channel ID, final title, source-cited description, made-for-kids classification and the approval phrase UPLOAD PRIVATE.
7. Workflow downloads EXACTLY one real MP4 from the approved GitHub Release, checks the OAuth channel owner ID, uploads via resumable videos.insert, forces privacyStatus=private and records the returned YouTube video ID in an artifact.
8. Verify playback and subtitles in YouTube Studio. To make PUBLIC later, explicitly approve the exact title/thumbnail/description/schedule and publish manually or through a separately approved access workflow.

**Never commit client secrets or an OAuth refresh token.** If credentials are absent, the job fails before uploading. No user password is needed.

## Important limitations

- The current code is a staged workflow and has not yet been tested with a real authorized YouTube OAuth token.
- A GitHub Release URL is not proof of a YouTube publication.
- YouTube uploads can have separate project verification, channel eligibility, audience rules, quota and copyright checks. Do not promise guaranteed instant public posting.
- If network fails after accepting file bytes but before the final response, inspect YouTube Studio before re-running, to avoid duplicate uploads. Keep the receipt as a checkpoint; the current resumable session is handled within one job, not safely across entirely new CI runs.
- Source content can require disclosure of synthetic media. Evaluate official YouTube policy and set this appropriately at upload/review; default private is not a substitute for truthful disclosure.

References:
- https://developers.google.com/youtube/data/reference/rest/v3/videos/insert
- https://developers.google.com/youtube/data/guides/using_resumable_upload_protocol
- https://developers.google.com/identity/protocols/oauth2

## Programmatic dry-run

A correctly assembled, approved private manifest references a real MP4:
{
  "video_path": "/path/to/verified-documentary.mp4",
  "channel_id": "UCdQu7MU5dHhaClhkCdG2BKg",
  "title": "Approved title",
  "description": "Approved sources and context",
  "tags": ["Documentary"],
  "made_for_kids": false,
  "privacyStatus": "private",
  "approved_for_publish": true
}

Validate dry run (no credentials and no upload):

    python production/youtube_private_upload.py --manifest private_upload_manifest.json --channel-id UCdQu7MU5dHhaClhkCdG2BKg

Actual upload adds --execute and is only valid with configured authorized OAuth secrets. Do not call it merely to preview media.
