"""
Pre-seeded Brilliant Directories Solution Center documentation and screenshots.
Seeds realistic categories, folders, markdown tables, step-by-step settings, and UI screenshots.
"""
from app.database import db
from retrieval.chunker import chunker
from retrieval.embedder import embedder
from multimodal.image_analyzer import image_analyzer

SEED_ARTICLES = [
    {
        "url": "https://support.brilliantdirectories.com/support/solutions/articles/1200003401-how-to-connect-stripe-payment-gateway",
        "title": "How to Connect Stripe Payment Gateway",
        "category": "Payments & E-Commerce",
        "folder": "Payment Gateways",
        "clean_text": """## Overview
Brilliant Directories allows website owners to collect one-time payments and recurring membership subscriptions directly through Stripe. Connecting Stripe takes less than 5 minutes and uses secure API keys.

## Step-by-Step Setup
1. In your Admin Dashboard, navigate to **Finance > Payment Gateways**.
2. Select **Stripe** from the list of supported payment providers.
3. Log into your Stripe Dashboard and navigate to **Developers > API Keys**.
4. Copy your **Publishable Key** and **Secret Key**.
5. Paste both keys into the designated fields in your Brilliant Directories admin panel.
6. Under **Webhook Settings**, copy the Brilliant Directories webhook endpoint URL: `https://yourdomain.com/stripe_webhook.php`.
7. In Stripe, create a new webhook endpoint listening for `invoice.payment_succeeded`, `invoice.payment_failed`, and `customer.subscription.deleted`.
8. Click **Save Changes** and run a test transaction in Test Mode before switching live.

## Important Notes on Currencies and Fees
| Setting | Recommended Value | Notes |
| Default Currency | USD / EUR / GBP | Must match your Stripe account payout currency |
| Test Mode | Enabled initially | Allows simulated transactions using test card 4242 |
| Webhook Signing Secret | Required for live | Prevents replay attacks and unauthorized postbacks |
""",
        "images": [
            {
                "image_url": "https://support.brilliantdirectories.com/assets/screenshots/stripe_gateway_settings.png",
                "alt_text": "Admin panel screen showing Stripe Publishable Key, Secret Key inputs and Test Mode toggle switch",
                "context": "Paste both keys into the designated fields in your Brilliant Directories admin panel and toggle Test Mode."
            }
        ]
    },
    {
        "url": "https://support.brilliantdirectories.com/support/solutions/articles/1200003402-refunds-and-membership-cancellation-policy",
        "title": "Handling Member Refunds and Subscription Cancellations",
        "category": "Payments & E-Commerce",
        "folder": "Billing & Refunds",
        "clean_text": """## Cancellation and Refund Principles
Brilliant Directories software does not automatically issue bank refunds when a member cancels their account from their dashboard. Instead, subscription status is set to 'Cancelled at Period End' to avoid interrupting active listings until the current billing cycle expires.

## How Administrators Issue a Refund
1. Navigate to **Finance > Transaction History**.
2. Search for the member by Name, Email, or Transaction ID.
3. Click the **Actions** dropdown next to the payment record and select **Issue Refund**.
4. Choose whether to perform a **Full Refund** or a **Partial Refund**.
5. When issuing a refund through the admin panel, Brilliant Directories instructs Stripe to return funds to the customer's original payment method (typically 5-10 business days).
6. Note: Platform transaction fees charged by third-party processors are generally non-refundable.

## Member Self-Service Cancellation
Members can cancel recurring billing by visiting their account settings under **Manage Account > Change Plan > Stop Recurring Billing**. This immediately disables renewal without deleting profile data.
""",
        "images": [
            {
                "image_url": "https://support.brilliantdirectories.com/assets/screenshots/transaction_refund_modal.png",
                "alt_text": "Refund modal showing Full Refund radio button, Partial Amount input, and Confirm Refund action button",
                "context": "Click the Actions dropdown next to the payment record and select Issue Refund."
            }
        ]
    },
    {
        "url": "https://support.brilliantdirectories.com/support/solutions/articles/1200004501-configuring-member-search-results-and-filters",
        "title": "Configuring Member Search Results & Custom Filters",
        "category": "Search & Navigation",
        "folder": "Search Settings",
        "clean_text": """## Overview of Member Search Capabilities
Brilliant Directories comes equipped with a comprehensive built-in search engine for directory listings. Directory owners can enable radius-based location searches, keyword matching, and multi-tier category dropdowns without writing custom code.

## Available Built-in Filter Settings
You can customize search filters by navigating to **Settings > General Settings > Search Settings Tab**:
1. **Keyword Search Target**: Choose whether keyword searches inspect Member Name, Company Name, Biography, or Custom Skills tags.
2. **Location Search Type**: Options include Zip/Postal Code radius (miles or kilometers), City, State/Province, or Country dropdown.
3. **Category Filtering**: Enable 3-tier hierarchical category selection (Top Category > Sub-Category > Sub-Sub-Category).
4. **Facet Filters (Sidebar)**: Toggle checkboxes for 'Verified Members Only', 'Offers Coupons', and 'Has Member Reviews'.

## Custom Fields in Search
If you require custom filters (e.g. 'Years in Business' or 'Languages Spoken'):
- Open **Toolbox > Form Manager**.
- Edit the **Listing - Additional Details** form and add the custom fields.
- Mark the field as **Searchable: Yes**. Brilliant Directories will automatically render that field in the search sidebar.
""",
        "images": [
            {
                "image_url": "https://support.brilliantdirectories.com/assets/screenshots/search_settings_filters.png",
                "alt_text": "Search Settings tab highlighting Keyword Target, Radius Distance Slider, and Facet Checkboxes",
                "context": "Navigate to Settings > General Settings > Search Settings Tab and toggle facet checkboxes."
            }
        ]
    },
    {
        "url": "https://support.brilliantdirectories.com/support/solutions/articles/1200004502-member-review-and-rating-system",
        "title": "Member Review and Rating System Settings",
        "category": "Members & Interactions",
        "folder": "Reviews & Ratings",
        "clean_text": """## Member Reviews Architecture
The review system allows visitors and verified clients to rate directory members on a 1 to 5 star scale with written feedback.

## Moderation & Approval Workflow
1. Navigate to **My Members > Member Reviews**.
2. Review settings include:
   - **Auto-Approve Reviews**: Off by default. When Off, reviews remain in 'Pending Review' status until an admin approves them.
   - **Require Member Verification**: Only logged-in visitors or confirmed email addresses can submit a review.
   - **Member Rebuttal**: Allows directory members to post an official public response to reviews.
3. Email alerts can be configured in **Email > Email Notifications** to alert administrators whenever a 1-star or 2-star rating is submitted.
""",
        "images": [
            {
                "image_url": "https://support.brilliantdirectories.com/assets/screenshots/member_review_moderation.png",
                "alt_text": "Member reviews queue showing Approve button, Reject button, and Star Rating breakdown",
                "context": "Navigate to My Members > Member Reviews to approve or reject pending member reviews."
            }
        ]
    },
    {
        "url": "https://support.brilliantdirectories.com/support/solutions/articles/1200005601-customizing-website-logo-branding-and-design",
        "title": "How to Upload Website Logo and Brand Assets",
        "category": "Design & Appearance",
        "folder": "Branding",
        "clean_text": """## Setting Up Your Brand Identity
Brilliant Directories provides a real-time Design Settings editor to control logos, colors, typography, and headers.

## Uploading Logo and Favicon
1. Go to **Settings > Design Settings > Brand Images**.
2. Click **Upload Website Logo**. Recommended dimensions: 400px width by 120px height in PNG (transparent) or SVG format.
3. Click **Upload Favicon**. Recommended size: 32x32px or 64x64px ICO or PNG.
4. Under the **Primary Colors** tab, configure your primary accent color, button hover color, and footer background.
5. Click **Save Changes** at the bottom-right. Changes take effect on the live website immediately without requiring cache clears.
""",
        "images": [
            {
                "image_url": "https://support.brilliantdirectories.com/assets/screenshots/brand_images_uploader.png",
                "alt_text": "Brand Images panel with Website Logo file uploader and Favicon preview container",
                "context": "Go to Settings > Design Settings > Brand Images and upload transparent PNG logo."
            }
        ]
    },
    {
        "url": "https://support.brilliantdirectories.com/support/solutions/articles/1200005602-managing-automated-email-templates",
        "title": "Managing Automated Email Notification Templates",
        "category": "Email & Communication",
        "folder": "Email Templates",
        "clean_text": """## Built-in System Email Templates
Brilliant Directories includes over 50 pre-designed email templates for membership signups, invoice receipts, password resets, and contact inquiries.

## Customizing an Email Template
1. Navigate to **Emails > Email Templates**.
2. Search for the template you wish to modify (e.g. `welcome-new-member` or `payment-receipt`).
3. Click **Actions > Edit**.
4. Use the WYSIWYG editor to adjust subject line, greeting, and body content.
5. Dynamic shortcodes are available:
   - `%user_first_name%`: Recipient's first name
   - `%user_email%`: Recipient's registered email
   - `%website_name%`: Your directory site name
   - `%invoice_total%`: Total payment charged
6. Click **Save Changes**. You can click **Send Test Email** to preview formatting before sending to real customers.
""",
        "images": [
            {
                "image_url": "https://support.brilliantdirectories.com/assets/screenshots/email_template_editor.png",
                "alt_text": "Email Template WYSIWYG editor with subject line field, shortcode picker, and Send Test Email button",
                "context": "Navigate to Emails > Email Templates and click Actions > Edit to customize notification emails."
            }
        ]
    },
    {
        "url": "https://support.brilliantdirectories.com/support/solutions/articles/1200006701-automated-lead-generation-and-matching",
        "title": "Automated Lead Generation and Matching Settings",
        "category": "Leads & Inquiries",
        "folder": "Lead System",
        "clean_text": """## How the Lead Matching Engine Works
The Brilliant Directories Lead Generation module automatically captures inquiries from visitors and matches them to relevant directory members based on category and geographic radius.

## Key Lead Routing Configurations
1. Navigate to **Leads > Lead Settings**.
2. **Auto-Match Mode**:
   - `Instant Dispatch`: Sends lead email immediately to matching members.
   - `Admin Moderation`: Requires administrator to review lead quality before distribution.
3. **Max Matches per Lead**: Specify how many members can purchase or claim a single lead (e.g. 1 to 5 members).
4. **Member Tier Access**: Configure whether leads are offered exclusively to Premium membership plans before standard plans.
""",
        "images": [
            {
                "image_url": "https://support.brilliantdirectories.com/assets/screenshots/lead_matching_rules.png",
                "alt_text": "Lead settings screen showing Auto-Match dropdown, Max Matches number input, and Price per Lead setting",
                "context": "Navigate to Leads > Lead Settings to configure Auto-Match mode and Member Tier Access."
            }
        ]
    }
]

def seed_knowledge_base():
    """Seeds the SQLite knowledge base with realistic Brilliant Directories solution center articles."""
    print("Seeding Knowledge Brain database with solution articles...")
    for item in SEED_ARTICLES:
        url = item["url"]
        title = item["title"]
        category = item["category"]
        folder = item["folder"]
        clean_text = item["clean_text"]
        
        # Check / upsert article
        db.upsert_article(
            url=url,
            title=title,
            category=category,
            folder=folder,
            content_hash=f"seed_{hash(clean_text)}",
            raw_html=f"<html><body><h1>{title}</h1>{clean_text}</body></html>",
            clean_text=clean_text
        )

        # Chunk and embed
        article_dict = {
            "url": url,
            "title": title,
            "category": category,
            "folder": folder,
            "clean_text": clean_text,
            "sections": []
        }
        # Parse basic sections
        for sec_raw in clean_text.split("## "):
            if not sec_raw.strip():
                continue
            lines = sec_raw.strip().split("\n")
            heading = lines[0].strip()
            content = "\n".join(lines[1:]).strip()
            article_dict["sections"].append({"heading": heading, "content": content})

        chunks = chunker.chunk_article(article_dict)
        for ch in chunks:
            ch["embedding"] = embedder.embed_text(ch["text"])
        db.store_chunks(url, chunks)

        # Images
        for img in item.get("images", []):
            analysis = image_analyzer.analyze_screenshot(
                image_url=img["image_url"],
                alt_text=img["alt_text"],
                context_text=img["context"],
                article_title=title
            )
            db.store_image(
                article_url=url,
                image_url=analysis["image_url"],
                alt_text=analysis["alt_text"],
                vision_desc=analysis["description"],
                ui_elements=analysis["ui_elements"],
                uncertainty=analysis["uncertainty_score"]
            )

    counts = db.get_counts()
    print(f"Seed complete! Active Articles: {counts['active_articles']}, Total Chunks: {counts['total_chunks']}")

if __name__ == "__main__":
    seed_knowledge_base()
