import { EmailMessage } from "../types";

export const CUSTOMER_EMAILS_DATASET: EmailMessage[] = [
  // ==========================================
  // HOW-TO QUESTIONS (1-12)
  // ==========================================
  {
    id: "EMAIL-01",
    sender_name: "Sarah Jenkins",
    sender_email: "sarah@cityrealtyguide.com",
    subject: "How do I connect our Stripe account?",
    body: "Hi team, we just signed up for Brilliant Directories and want to start collecting membership dues. Where do we put our Stripe secret and publishable keys?",
    received_at: "2026-10-14T09:15:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },
  {
    id: "EMAIL-02",
    sender_name: "Marcus Vance",
    sender_email: "marcus@vanceadvisory.org",
    subject: "Where do we upload our high-res website logo?",
    body: "Good morning, our marketing team has prepared our brand assets. Where in the admin dashboard can we upload the new header logo and favicon? What size is recommended?",
    received_at: "2026-10-14T09:45:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },
  {
    id: "EMAIL-03",
    sender_name: "Elena Rostova",
    sender_email: "elena@wellnessnetwork.io",
    subject: "Setting up zip code radius search for therapists",
    body: "Hello, we want visitors to search for directory members by typing their zip code and choosing a 25-mile radius. Is this supported out of the box?",
    received_at: "2026-10-14T10:10:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },
  {
    id: "EMAIL-04",
    sender_name: "David Chen",
    sender_email: "david@chinatownbiz.net",
    subject: "Customizing the new member welcome email",
    body: "Hi support, when a new vendor creates a profile, the default welcome email doesn't mention our onboarding schedule. How do we edit this template?",
    received_at: "2026-10-14T11:00:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },
  {
    id: "EMAIL-05",
    sender_name: "Rachel Green",
    sender_email: "rachel@designercollective.com",
    subject: "Approving member reviews before they go live",
    body: "Hi, we received some spam reviews yesterday. How do we turn on review moderation so that reviews require administrator approval before appearing publicly?",
    received_at: "2026-10-14T11:30:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },
  {
    id: "EMAIL-06",
    sender_name: "Tom Bradley",
    sender_email: "tom@autoguild.com",
    subject: "How does lead auto-matching work?",
    body: "Hello, we want customer inquiries submitted on our homepage to automatically dispatch to 3 certified auto mechanics in the same city. Where are those settings?",
    received_at: "2026-10-14T12:00:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },
  {
    id: "EMAIL-07",
    sender_name: "Amara Patel",
    sender_email: "amara@tutorshub.co.uk",
    subject: "Adding 'Languages Spoken' to search sidebar",
    body: "Can we add custom searchable fields to our member profiles so parents can filter tutors who speak Spanish or Mandarin? Do we need custom coding?",
    received_at: "2026-10-14T13:15:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },
  {
    id: "EMAIL-08",
    sender_name: "Liam O'Connor",
    sender_email: "liam@corktrades.ie",
    subject: "Can members reply to customer reviews?",
    body: "One of our contractors asked if they can submit a rebuttal to an unfair review. Is there a built-in feature for member responses to reviews?",
    received_at: "2026-10-14T14:00:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },
  {
    id: "EMAIL-09",
    sender_name: "Sophie Dubois",
    sender_email: "sophie@montrealgourmet.ca",
    subject: "Changing primary button accent colors",
    body: "Hi! How do we change the bright orange color of all buttons and navigation links to match our burgundy corporate branding?",
    received_at: "2026-10-14T14:45:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },
  {
    id: "EMAIL-10",
    sender_name: "Kenneth Miller",
    sender_email: "kmiller@legalmatchup.org",
    subject: "What shortcodes work in invoice email notifications?",
    body: "We want to include the customer's company name and transaction date on the invoice email receipt. Where can we find the available dynamic shortcodes?",
    received_at: "2026-10-14T15:20:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },
  {
    id: "EMAIL-11",
    sender_name: "Grace Kim",
    sender_email: "grace@koreanfoodies.com",
    subject: "Limiting leads to Premium plan members only",
    body: "Is it possible to set lead distribution so that free members do not get matched leads, and only paid subscribers receive phone leads?",
    received_at: "2026-10-14T16:00:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },
  {
    id: "EMAIL-12",
    sender_name: "Brian Nelson",
    sender_email: "bnelson@buildersassoc.com",
    subject: "Testing Stripe checkout with test credit cards",
    body: "We want to verify our membership checkout flow before launching tomorrow. Can we enable test mode with card 4242 in the Stripe settings?",
    received_at: "2026-10-14T16:30:00Z",
    expected_category: "how_to",
    expected_risk: "low"
  },

  // ==========================================
  // TROUBLESHOOTING (13-22)
  // ==========================================
  {
    id: "EMAIL-13",
    sender_name: "Julian Alvarez",
    sender_email: "julian@miamiboatclub.com",
    subject: "Stripe webhook endpoint returning 404 error",
    body: "Our members are paying through Stripe, but their accounts are not activating automatically. In Stripe, the webhook shows repeated 404 errors. Please help us fix the URL.",
    received_at: "2026-10-14T17:00:00Z",
    expected_category: "troubleshooting",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-14",
    sender_name: "Claire Becker",
    sender_email: "claire@petloversdirectory.com",
    subject: "Uploaded logo looks blurry and stretched on mobile",
    body: "We uploaded our logo as a 1200x800 JPG file, but on smartphones it overlaps the hamburger menu and looks stretched. How do we fix the responsive sizing?",
    received_at: "2026-10-14T17:40:00Z",
    expected_category: "troubleshooting",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-15",
    sender_name: "Nathan Drake",
    sender_email: "nathan@exploreoutdoors.net",
    subject: "Location search not displaying Google Maps markers",
    body: "When visitors search by city, the list loads but the map on the right is completely gray with an 'API Key Missing or Billing Not Enabled' error.",
    received_at: "2026-10-14T18:15:00Z",
    expected_category: "troubleshooting",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-16",
    sender_name: "Priya Sharma",
    sender_email: "priya@indiasalonfinder.in",
    subject: "Members receiving duplicate notification emails",
    body: "Two of our salon owners reported getting two identical welcome emails whenever they update their profile pictures. Where can we check the trigger rules?",
    received_at: "2026-10-14T19:00:00Z",
    expected_category: "troubleshooting",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-17",
    sender_name: "Carlos Mendez",
    sender_email: "carlos@austinrestorations.com",
    subject: "Checkout button disabled on mobile safari",
    body: "Several customers called saying the 'Complete Order' button is grayed out on iOS Safari when registering for the Pro plan. Can you check our checkout script?",
    received_at: "2026-10-14T19:45:00Z",
    expected_category: "troubleshooting",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-18",
    sender_name: "Hannah Watson",
    sender_email: "hannah@freelancewriters.org",
    subject: "Sub-sub categories not showing in dropdown",
    body: "We added 15 sub-sub categories under 'Technical Writing', but only the parent category displays on the search filter dropdown. Why aren't third tier categories showing?",
    received_at: "2026-10-14T20:30:00Z",
    expected_category: "troubleshooting",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-19",
    sender_name: "Derek Foster",
    sender_email: "derek@chicagoagents.biz",
    subject: "Member reviews not appearing after admin approval",
    body: "I clicked 'Approve' on 5 member reviews this morning in the admin dashboard, but they still do not show on the member's public profile page.",
    received_at: "2026-10-15T08:15:00Z",
    expected_category: "troubleshooting",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-20",
    sender_name: "Zoe Kravitz",
    sender_email: "zoe@indiefilmmakers.tv",
    subject: "SSL certificate warning appearing on our custom domain",
    body: "Our custom domain is displaying 'Connection Not Secure / Your connection is not private' when users visit https. Can you verify if our Cloudflare SSL is configured?",
    received_at: "2026-10-15T09:00:00Z",
    expected_category: "troubleshooting",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-21",
    sender_name: "Ethan Hunt",
    sender_email: "ethan@missionsecurity.com",
    subject: "Lead emails landing in spam folders for members",
    body: "Our directory members are complaining that lead notifications go directly to their junk or spam folder. Do we need to set up SPF and DKIM records for our domain?",
    received_at: "2026-10-15T09:40:00Z",
    expected_category: "troubleshooting",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-22",
    sender_name: "Olga Kurylenko",
    sender_email: "olga@eurotransit.eu",
    subject: "Currency symbol showing USD instead of EUR on checkout page",
    body: "We selected Euro as our default currency in Finance > Payment Gateways, but member invoice previews still show a dollar sign ($) instead of €.",
    received_at: "2026-10-15T10:15:00Z",
    expected_category: "troubleshooting",
    expected_risk: "medium"
  },

  // ==========================================
  // PROJECT REQUESTS (23-28)
  // ==========================================
  {
    id: "EMAIL-23",
    sender_name: "Robert Langdon",
    sender_email: "robert@harvardacademic.edu",
    subject: "Custom feature: Real-time video consultation integration",
    body: "We want to hire you to build a custom feature that embeds a Zoom or Agora video call window directly inside each professor's directory profile. How can we proceed?",
    received_at: "2026-10-15T11:00:00Z",
    expected_category: "project_request",
    expected_risk: "high"
  },
  {
    id: "EMAIL-24",
    sender_name: "Victoria Sterling",
    sender_email: "victoria@luxuryestates.co.uk",
    subject: "Bespoke Mobile App for iOS and Android",
    body: "Our executive board wants a dedicated native iOS and Android mobile app that syncs with our Brilliant Directories member database and offers push notifications for VIP properties.",
    received_at: "2026-10-15T11:45:00Z",
    expected_category: "project_request",
    expected_risk: "high"
  },
  {
    id: "EMAIL-25",
    sender_name: "Martin Brody",
    sender_email: "mbrody@amityharbor.gov",
    subject: "Custom two-way sync with Municipal Oracle database",
    body: "We need an enterprise integration that syncs business license registrations from our county Oracle database into our directory every night at midnight.",
    received_at: "2026-10-15T12:30:00Z",
    expected_category: "project_request",
    expected_risk: "high"
  },
  {
    id: "EMAIL-26",
    sender_name: "Samantha Wright",
    sender_email: "swright@startupfounders.club",
    subject: "Redesign our homepage and custom member dashboard",
    body: "We want a complete visual overhaul for our homepage and member dashboard, including dark mode, custom animated widgets, and custom typography.",
    received_at: "2026-10-15T13:15:00Z",
    expected_category: "project_request",
    expected_risk: "high"
  },
  {
    id: "EMAIL-27",
    sender_name: "Gary Cooper",
    sender_email: "gcooper@midwesttrade.org",
    subject: "Custom escrow payment milestone system",
    body: "Can your team build a custom escrow milestone system where directory clients deposit funds and only release them upon job completion?",
    received_at: "2026-10-15T14:00:00Z",
    expected_category: "project_request",
    expected_risk: "high"
  },
  {
    id: "EMAIL-28",
    sender_name: "Lisa Cuddy",
    sender_email: "lcuddy@princetonhealth.org",
    subject: "HIPAA Compliant medical record document vault for members",
    body: "We want to expand our clinic directory to let doctors upload encrypted patient records. Can you develop an encrypted document portal inside member profiles?",
    received_at: "2026-10-15T14:45:00Z",
    expected_category: "project_request",
    expected_risk: "high"
  },

  // ==========================================
  // REFUND OR CANCELLATION REQUESTS (29-34)
  // ==========================================
  {
    id: "EMAIL-29",
    sender_name: "Arthur Dent",
    sender_email: "adent@galaxytravel.co.uk",
    subject: "Requesting refund for accidental annual charge",
    body: "Hello, my credit card was charged $490 yesterday for annual renewal. I intended to cancel last week. Please cancel my subscription and issue a full refund to my card.",
    received_at: "2026-10-15T15:15:00Z",
    expected_category: "refund_cancellation",
    expected_risk: "high"
  },
  {
    id: "EMAIL-30",
    sender_name: "Beatrice Webb",
    sender_email: "beatrice@londonartisans.com",
    subject: "Cancel our monthly subscription immediately",
    body: "We are shutting down our artisan guild due to retirement. Please cancel our subscription effective immediately and confirm no further charges will occur.",
    received_at: "2026-10-15T15:50:00Z",
    expected_category: "refund_cancellation",
    expected_risk: "high"
  },
  {
    id: "EMAIL-31",
    sender_name: "Gregory House",
    sender_email: "ghouse@diagnosticslabs.org",
    subject: "Duplicate charge on our account - need refund",
    body: "Our accounting department noticed we were charged twice on October 1st: invoice #4401 and #4402 for $150 each. Please refund the duplicate transaction right away.",
    received_at: "2026-10-15T16:20:00Z",
    expected_category: "refund_cancellation",
    expected_risk: "high"
  },
  {
    id: "EMAIL-32",
    sender_name: "Jessica Pearson",
    sender_email: "jpearson@pearsonlegal.com",
    subject: "Termination of consulting retainer and prorated refund",
    body: "In accordance with section 4.2 of our agreement, we are providing notice of termination for our consulting retainer. Please issue a prorated refund for unused days.",
    received_at: "2026-10-15T17:00:00Z",
    expected_category: "refund_cancellation",
    expected_risk: "high"
  },
  {
    id: "EMAIL-33",
    sender_name: "Alan Grant",
    sender_email: "agrant@jurassicfossils.org",
    subject: "Cancel subscription and remove credit card details",
    body: "Please cancel my account and delete all stored billing details and credit cards from your database per GDPR data privacy requirements.",
    received_at: "2026-10-15T17:40:00Z",
    expected_category: "refund_cancellation",
    expected_risk: "high"
  },
  {
    id: "EMAIL-34",
    sender_name: "Dana Scully",
    sender_email: "dscully@fbi-forensics.gov",
    subject: "Unauthorized charge on corporate card - refund request",
    body: "A charge of $299 appeared from your company on my government corporate card that I did not authorize. Please reverse this transaction immediately or I will file a bank chargeback.",
    received_at: "2026-10-15T18:15:00Z",
    expected_category: "refund_cancellation",
    expected_risk: "high"
  },

  // ==========================================
  // COMPLAINTS (35-40)
  // ==========================================
  {
    id: "EMAIL-35",
    sender_name: "Harvey Specter",
    sender_email: "harvey@specterlitt.law",
    subject: "Unacceptable downtime during our annual member gala launch",
    body: "Our website went completely blank for 4 hours during our biggest annual fundraiser yesterday. We lost thousands in ticket sales. This is completely unacceptable and I expect a call from leadership.",
    received_at: "2026-10-15T19:00:00Z",
    expected_category: "complaint",
    expected_risk: "high"
  },
  {
    id: "EMAIL-36",
    sender_name: "Walter White",
    sender_email: "ww@abqchemical.com",
    subject: "Your latest update broke all our custom CSS styling",
    body: "We logged in this morning and all our fonts, margins, and header layouts are completely destroyed by your automatic platform update. Fix this disaster immediately.",
    received_at: "2026-10-15T19:40:00Z",
    expected_category: "complaint",
    expected_risk: "high"
  },
  {
    id: "EMAIL-37",
    sender_name: "Logan Roy",
    sender_email: "lroy@waystar-royco.com",
    subject: "Three days without reply from your support team",
    body: "I pay for top-tier enterprise SLA support. I opened ticket #9921 on Monday and nobody has responded in 72 hours. Escalate this to your VP of Operations immediately.",
    received_at: "2026-10-15T20:15:00Z",
    expected_category: "complaint",
    expected_risk: "high"
  },
  {
    id: "EMAIL-38",
    sender_name: "Claire Underwood",
    sender_email: "cunderwood@whitehouse.gov",
    subject: "Terrible customer experience - our search has been malfunctioning for a week",
    body: "Our constituents cannot locate local emergency relief centers because your search algorithm returns zero results. I expect a personal explanation and root cause analysis.",
    received_at: "2026-10-15T20:50:00Z",
    expected_category: "complaint",
    expected_risk: "high"
  },
  {
    id: "EMAIL-39",
    sender_name: "Gordon Gekko",
    sender_email: "ggekko@wallstreetcapital.com",
    subject: "Threatening legal action over lost leads",
    body: "Due to your lead auto-match system failing silently for two weeks, our brokers missed over $100k in commissions. I am speaking to our legal counsel today if this is not resolved.",
    received_at: "2026-10-15T21:30:00Z",
    expected_category: "complaint",
    expected_risk: "critical"
  },
  {
    id: "EMAIL-40",
    sender_name: "Miranda Priestly",
    sender_email: "mpriestly@runwaymag.com",
    subject: "The design output is substandard and amateurish",
    body: "The custom banner delivered by your design team looks like something from 1999. It does not follow our brand guidelines. I am deeply disappointed in your service quality.",
    received_at: "2026-10-15T22:00:00Z",
    expected_category: "complaint",
    expected_risk: "high"
  },

  // ==========================================
  // QUOTE REQUESTS (41-46)
  // ==========================================
  {
    id: "EMAIL-41",
    sender_name: "Peter Parker",
    sender_email: "peter@dailybugle.photo",
    subject: "Pricing for custom AI image tagger integration",
    body: "Hello, we want an automated system that tags photographer portfolios using computer vision. What would your consulting team charge for an MVP integration?",
    received_at: "2026-10-16T08:15:00Z",
    expected_category: "quote_request",
    expected_risk: "high"
  },
  {
    id: "EMAIL-42",
    sender_name: "Bruce Wayne",
    sender_email: "bwayne@wayneenterprises.com",
    subject: "Quote request: Enterprise migration of 250,000 members",
    body: "We are migrating from an old legacy custom directory to Brilliant Directories. We have 250,000 member records and 10 years of transaction history. Please provide a formal cost quote and timeline.",
    received_at: "2026-10-16T09:00:00Z",
    expected_category: "quote_request",
    expected_risk: "high"
  },
  {
    id: "EMAIL-43",
    sender_name: "Tony Stark",
    sender_email: "tstark@starkindustries.io",
    subject: "How much would it cost to develop a custom Stripe Connect marketplace?",
    body: "We want directory members to sell hardware directly through our portal with split payouts via Stripe Connect. What is your estimated cost and hourly consulting rate?",
    received_at: "2026-10-16T09:45:00Z",
    expected_category: "quote_request",
    expected_risk: "high"
  },
  {
    id: "EMAIL-44",
    sender_name: "Natasha Romanoff",
    sender_email: "natasha@avengersinitiative.org",
    subject: "Cost estimate for custom multi-language localization",
    body: "Can you provide a formal quote for translating our directory into 6 languages (French, Spanish, German, Japanese, Arabic, and Russian) with automatic geo-detection?",
    received_at: "2026-10-16T10:30:00Z",
    expected_category: "quote_request",
    expected_risk: "high"
  },
  {
    id: "EMAIL-45",
    sender_name: "Diana Prince",
    sender_email: "diana@themysciraculture.org",
    subject: "Consulting rate for quarterly SEO audit and performance tuning",
    body: "We would like to retain your senior AI and technical consultants for 20 hours per month for ongoing SEO optimization and database indexing. What is your monthly retainer fee?",
    received_at: "2026-10-16T11:15:00Z",
    expected_category: "quote_request",
    expected_risk: "high"
  },
  {
    id: "EMAIL-46",
    sender_name: "Steve Rogers",
    sender_email: "srogers@veteransalliance.org",
    subject: "Budget estimate for accessibility audit and WCAG 2.1 AA compliance",
    body: "We need our entire member portal to be fully compliant with federal ADA and WCAG 2.1 AA standards. How much budget should our non-profit board allocate for this?",
    received_at: "2026-10-16T12:00:00Z",
    expected_category: "quote_request",
    expected_risk: "high"
  },

  // ==========================================
  // FOLLOW-UPS (47-52)
  // ==========================================
  {
    id: "EMAIL-47",
    sender_name: "Peggy Carter",
    sender_email: "pcarter@strategicdefense.gov",
    subject: "Following up on SOW proposal for search filter customization",
    body: "Hi team, following up on the scope of work document discussed in our meeting last Tuesday. Has the engineering estimate been finalized for our executive review?",
    received_at: "2026-10-16T12:45:00Z",
    expected_category: "follow_up",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-48",
    sender_name: "Clark Kent",
    sender_email: "ckent@dailyplanet.press",
    subject: "Checking in on the status of ticket #8842",
    body: "Hello, just checking in to see if your developers had a chance to inspect our staging site regarding the Google Maps radius issue reported on Wednesday.",
    received_at: "2026-10-16T13:30:00Z",
    expected_category: "follow_up",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-49",
    sender_name: "Barry Allen",
    sender_email: "ballen@centralcityforensics.org",
    subject: "Any update on our custom invoice template approval?",
    body: "Per my previous email from yesterday, did the finance team approve the revised shortcodes for our tax exemption number on member receipts?",
    received_at: "2026-10-16T14:15:00Z",
    expected_category: "follow_up",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-50",
    sender_name: "Wanda Maximoff",
    sender_email: "wanda@westviewarts.org",
    subject: "Did you receive our revised logo file?",
    body: "Hi support, I emailed our transparent SVG logo file yesterday morning. Can you confirm if you received it and whether it has been uploaded to our staging site?",
    received_at: "2026-10-16T15:00:00Z",
    expected_category: "follow_up",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-51",
    sender_name: "Stephen Strange",
    sender_email: "sstrange@kamartaj.edu",
    subject: "Urgent status update on payment gateway sandbox migration",
    body: "We have an executive board demonstration in 3 hours. Following up urgently to ensure our Stripe Test Mode keys are verified and ready for live transactions.",
    received_at: "2026-10-16T15:45:00Z",
    expected_category: "follow_up",
    expected_risk: "medium"
  },
  {
    id: "EMAIL-52",
    sender_name: "Bucky Barnes",
    sender_email: "bbarnes@shieldops.mil",
    subject: "Follow up: Refund status for invoice #3391",
    body: "Following up on my refund request from Monday. Your support representative indicated funds would appear within 5 business days. Can you provide the Stripe reversal ARN?",
    received_at: "2026-10-16T16:30:00Z",
    expected_category: "follow_up",
    expected_risk: "medium"
  }
];
