"""Inject product/service/person JSON-LD into key pages.

Idempotent: skips files that already contain the marker comment for the schema.
"""

from pathlib import Path

ROOT = Path(__file__).parent

MARKER = "<!-- eg:product-schema -->"

SCHEMAS = {
    "command-os.html": '''<!-- eg:product-schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Command HVAC",
  "alternateName": "Command OS",
  "applicationCategory": "BusinessApplication",
  "applicationSubCategory": "HVAC Operations Software",
  "operatingSystem": "Web, Cloud",
  "description": "Command HVAC is the AI Operating System for HVAC businesses with 2–50+ trucks. Built on Anthropic's Claude, it includes Roger (24/7 AI voice agent), AI dispatch automation, real-time visibility dashboards, coaching analytics, and weekly business intelligence reports.",
  "url": "https://econ-growth.com/command-os.html",
  "image": "https://econ-growth.com/assets/images/favicon.png",
  "creator": {
    "@type": "Organization",
    "name": "eCon Growth",
    "url": "https://econ-growth.com/"
  },
  "featureList": [
    "AI dispatch automation",
    "24/7 AI voice agent (Roger)",
    "Real-time visibility dashboard",
    "Coaching analytics",
    "Weekly business intelligence reports",
    "Missed-call text-back automation"
  ],
  "audience": {
    "@type": "BusinessAudience",
    "audienceType": "HVAC contractors with 2–50+ trucks"
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "url": "https://econ-growth.com/book.html",
    "availability": "https://schema.org/InStock"
  }
}
</script>
''',

    "roger.html": '''<!-- eg:product-schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Roger — AI Voice Agent for HVAC",
  "serviceType": "AI Voice Agent / AI Answering Service",
  "description": "Roger is a 24/7 AI voice agent built for HVAC contractors. He answers every inbound call in under three seconds, qualifies the caller, books the appointment directly into the dispatch schedule, and confirms with the customer. Powered by Anthropic's Claude.",
  "url": "https://econ-growth.com/roger.html",
  "provider": {
    "@type": "Organization",
    "name": "eCon Growth",
    "url": "https://econ-growth.com/"
  },
  "areaServed": {
    "@type": "Country",
    "name": "United States"
  },
  "audience": {
    "@type": "BusinessAudience",
    "audienceType": "HVAC business owners running 2–50+ trucks"
  },
  "category": "AI Voice Agent for HVAC Contractors",
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "url": "https://econ-growth.com/book.html",
    "availability": "https://schema.org/InStock"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Roger",
  "applicationCategory": "BusinessApplication",
  "applicationSubCategory": "AI Voice Agent",
  "operatingSystem": "Web, Cloud, Telephony",
  "description": "AI voice agent for HVAC. Answers, qualifies, books, and confirms every inbound call 24/7.",
  "url": "https://econ-growth.com/roger.html",
  "creator": {
    "@type": "Organization",
    "name": "eCon Growth",
    "url": "https://econ-growth.com/"
  }
}
</script>
''',

    "visibility.html": '''<!-- eg:product-schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "eCon Growth Visibility Dashboard",
  "applicationCategory": "BusinessApplication",
  "applicationSubCategory": "HVAC Business Intelligence",
  "operatingSystem": "Web, Cloud",
  "description": "Real-time visibility dashboard for HVAC operations. Tracks close rates, technician performance, call outcomes, dispatch efficiency, and revenue across every part of the business — in one screen.",
  "url": "https://econ-growth.com/visibility.html",
  "creator": {
    "@type": "Organization",
    "name": "eCon Growth",
    "url": "https://econ-growth.com/"
  },
  "audience": {
    "@type": "BusinessAudience",
    "audienceType": "HVAC business owners running 2–50+ trucks"
  }
}
</script>
''',

    "about.html": '''<!-- eg:product-schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Kristopher Cravens",
  "jobTitle": "Founder & CEO",
  "worksFor": {
    "@type": "Organization",
    "name": "eCon Growth",
    "url": "https://econ-growth.com/"
  },
  "description": "Founder of eCon Growth. Ten years inside HVAC operations — every role, every truck, every shift. Built Command HVAC from the inside out for HVAC business owners running 2–50+ trucks.",
  "url": "https://econ-growth.com/about.html",
  "image": "https://econ-growth.com/kris-photo.jpg",
  "sameAs": [
    "https://www.linkedin.com/company/econ-growthoffical/"
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AboutPage",
  "name": "About eCon Growth",
  "url": "https://econ-growth.com/about.html",
  "mainEntity": {
    "@type": "Organization",
    "name": "eCon Growth",
    "url": "https://econ-growth.com/"
  }
}
</script>
''',
}


def inject(filename, payload):
    fp = ROOT / filename
    html = fp.read_text(encoding="utf-8")
    if MARKER in html:
        return f"{filename}: marker present, skipped"
    if "</head>" not in html:
        return f"{filename}: no </head>, skipped"
    new_html = html.replace("</head>", payload + "</head>", 1)
    fp.write_text(new_html, encoding="utf-8")
    return f"{filename}: injected"


if __name__ == "__main__":
    for filename, payload in SCHEMAS.items():
        print(inject(filename, payload))
