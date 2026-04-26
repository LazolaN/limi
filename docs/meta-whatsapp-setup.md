# Meta WhatsApp Cloud API Setup — One-Farmer Pilot

You'll do this. ~30–45 minutes once. **No business verification needed** for a test cohort of ≤5 numbers.

---

## Step 1 — Create a Meta Developer account
1. Go to https://developers.facebook.com/
2. Sign up (use a personal Facebook account; you can switch to a Business Manager later)
3. Verify email + phone

## Step 2 — Create an App
1. **My Apps** → **Create App**
2. Use case: **Other**
3. App type: **Business**
4. App name: `Limi Pilot` (or anything)
5. Contact email: yours
6. Business Account: leave default; we'll attach later if you scale beyond pilot

## Step 3 — Add the WhatsApp product
1. From the app dashboard: **Add Product** → **WhatsApp** → **Set up**
2. You'll land on **WhatsApp → Getting Started**
3. Meta provisions a **free test phone number** (looks like a US +1 555... number)

## Step 4 — Capture the four secrets we need
On **WhatsApp → API Setup**, copy these. You'll paste them into Railway env vars later.

| Meta label | Goes into env var |
|---|---|
| Phone number ID | `WHATSAPP_PHONE_NUMBER_ID` |
| Temporary access token (24h) | `WHATSAPP_ACCESS_TOKEN` *(replace in Step 7)* |
| App Secret (App Settings → Basic → "App Secret" → Show) | `WHATSAPP_APP_SECRET` |
| Any random string you choose, e.g. `limi-pilot-9f3k2a` | `WHATSAPP_VERIFY_TOKEN` |

## Step 5 — Allowlist your test recipients
On the API Setup page → **To** dropdown → **Manage phone number list**.
Add up to 5 numbers that may receive messages from your test number:
1. Your number (for sanity testing)
2. Brother's number
3. (Optional) one more for fallback

Each number must verify with a code Meta sends them on WhatsApp.

## Step 6 — Sanity test the test number
Click **Send message** to fire the `hello_world` template at your number. If you receive it, the test number is live. If not, debug here before proceeding.

## Step 7 — Generate a long-lived access token
The 24-hour temporary token is fine for Step 6, but the pilot needs a System User token.
1. **Business Settings** → **Users → System Users** → **Add**
2. Name: `Limi Pilot Bot`, role: **Admin**
3. **Add Assets** → assign your WhatsApp app
4. **Generate New Token** → select your app → tick `whatsapp_business_messaging` and `whatsapp_business_management`
5. Token Expiration: **Never** (recommended for pilot)
6. Copy the token — this is the real `WHATSAPP_ACCESS_TOKEN`

## Step 8 — Hand off the secrets
Send Lazola (or paste into Railway directly):
- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_ACCESS_TOKEN` *(long-lived from Step 7)*
- `WHATSAPP_APP_SECRET`
- `WHATSAPP_VERIFY_TOKEN` *(whatever string you chose in Step 4)*

## Step 9 — Configure the webhook (we do this together once Railway is deployed)
1. Meta dashboard → **WhatsApp → Configuration → Webhook**
2. **Callback URL**: `https://<your-railway-app>.up.railway.app/webhook/whatsapp`
3. **Verify Token**: paste the same string as `WHATSAPP_VERIFY_TOKEN`
4. Click **Verify and Save** — Meta hits a GET on `/webhook/whatsapp` with `hub.challenge`; the app must echo it back
5. Subscribe to webhook fields: tick **`messages`** at minimum

---

## Limits & gotchas to know going in
- **Test number throughput**: max 250 conversations / 24h. Plenty for one farmer.
- **Allowlisted recipients only**: random numbers cannot message it. By design.
- **5-second response SLA**: Meta retries the webhook if you take >5s. We handle this with FastAPI BackgroundTasks — webhook returns 200 immediately, the LLM call + send happen async.
- **24-hour customer service window**: you can freely message a user for 24h after their last inbound message. After 24h silent, you'd need a pre-approved template. Irrelevant for our reactive bot.
- **Signature verification is non-negotiable**: every POST from Meta carries `X-Hub-Signature-256`. We HMAC-verify with `WHATSAPP_APP_SECRET`. If we skip this, anyone with the URL can post fake messages and burn Anthropic credits.

## When to upgrade to a real SA WhatsApp number (post-pilot)
- After ~50 successful conversations + decision to invite more farmers
- Requires Business Verification: company registration, utility bill on business address (1–2 weeks Meta processing)
- Replaces the test number; you can port your own SA WhatsApp Business number through a BSP (Turn.io, Clickatell, MessageBird) or directly via Meta
