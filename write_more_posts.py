"""Render two additional cornerstone posts using the standard template."""

import json
from pathlib import Path
from extract_blog_posts import render_post, BLOG_DIR

ROOT = Path(__file__).parent

POSTS = [
    {
        "slug": "ai-operating-system-for-hvac-2026-complete-guide",
        "title": "AI Operating System for HVAC: The Complete 2026 Guide",
        "excerpt": "Everything HVAC business owners need to understand about an AI Operating System — what it does, how it differs from CRMs and dispatch software, what to look for, and how to evaluate vendors before you sign anything.",
        "category": "AI & Technology",
        "date_label": "May 2026",
        "date_iso": "2026-05-02",
        "read_time": "12 min read",
        "body_html": """
<div class="ac-h2">What an AI Operating System for HVAC Actually Is</div>
<p class="ac-p">An <strong>AI Operating System for HVAC</strong> is a unified, AI-powered layer that runs the operations of an HVAC business — answering inbound calls, dispatching technicians, tracking visibility into every job, and surfacing weekly intelligence — without depending on any one person to be present.</p>
<p class="ac-p">It is not a CRM. It is not field-service software. It is not an answering service with AI features bolted on. It is the operating system the business runs on — the thing that makes dispatch happen, makes leads convert, and gives the owner real-time visibility into the operation, all without the owner needing to be in the middle of it.</p>
<p class="ac-p">For an HVAC business running 2 to 50+ trucks, an AI Operating System is the structural fix for the problem that keeps most operations stuck under $5M in revenue: the owner is the system. Everything routes through them. The moment volume increases, they become the bottleneck, and the business stops scaling.</p>

<div class="ac-h2">How an AI OS Differs from Software You've Already Tried</div>
<p class="ac-p">Most HVAC owners have tried at least three of these: a CRM, a field-service tool, an answering service, a marketing automation platform, and a dispatch board. None of them solved the underlying problem because none of them <em>operated the business</em>. They were tools the business used.</p>
<p class="ac-p">An AI Operating System operates the business. The distinction shows up in five places:</p>
<ul class="ac-ul">
  <li><strong>Inbound call handling.</strong> A CRM logs calls. An AI Operating System answers them — qualifies the caller, gathers job details, books the appointment, and confirms with the customer. No human required.</li>
  <li><strong>Dispatch decisions.</strong> Field-service software gives a dispatcher a calendar to drag jobs onto. An AI OS makes the assignment decision automatically, based on tech certifications, location, workload, and customer history.</li>
  <li><strong>Lead follow-up.</strong> Marketing automation sends sequences. An AI OS qualifies missed-call text-backs in real time and routes the genuinely hot leads back to the team within minutes.</li>
  <li><strong>Visibility.</strong> Most software shows you a dashboard. An AI OS surfaces what changed, what's at risk, and what to do about it — without the owner having to interpret raw numbers.</li>
  <li><strong>Coaching.</strong> Reports tell you a tech's close rate is low. An AI OS tells you which specific jobs they lost, why, and what coaching conversation will move the number.</li>
</ul>

<div class="ac-h2">The Five Components Every Real AI OS for HVAC Includes</div>
<p class="ac-p">Vendors will throw the term "AI Operating System" at anything that has a chatbot. Here's the actual checklist:</p>
<ul class="ac-ul">
  <li><strong>AI voice agent.</strong> Answers, qualifies, books, and confirms inbound calls 24/7. Production-grade examples — like eCon Growth's <a href="/roger.html">Roger</a> — answer in under three seconds.</li>
  <li><strong>AI dispatch automation.</strong> Smart job assignment, automated confirmations, missed-call text-back, and on-call rotation handled by the system, not a person.</li>
  <li><strong>Real-time visibility dashboard.</strong> A live view of close rates, technician performance, dispatch efficiency, and revenue — for the owner.</li>
  <li><strong>Coaching analytics.</strong> Per-tech data on close rate, average ticket, first-call-fix rate, and the patterns inside their lost jobs.</li>
  <li><strong>Weekly business intelligence.</strong> A report that tells you what changed, what's at risk, and what to do about it — not a pivot table you have to interpret.</li>
</ul>
<p class="ac-p">If a product doesn't include all five, it's a tool, not an operating system.</p>

<div class="ac-h2">What to Ask Before You Sign Anything</div>
<p class="ac-p">Vendor demos are designed to make every feature look essential. Cut through it with seven questions:</p>
<ul class="ac-ul">
  <li><strong>What model is it built on?</strong> Anthropic's Claude, OpenAI's GPT, or a custom black box matters. Production-grade AI in HVAC needs a real foundation model — not a 2023 chatbot wrapper.</li>
  <li><strong>Can the AI book directly into our dispatch schedule?</strong> If it just takes a message and forwards it, that's an answering service.</li>
  <li><strong>Does it sit on top of our existing field-service tool?</strong> Or is it a "rip and replace" play that breaks our team's workflow on day one?</li>
  <li><strong>How long until live?</strong> If onboarding is measured in months, the vendor isn't ready. Real AI OS vendors are measured in days to weeks.</li>
  <li><strong>What does the owner see?</strong> If the dashboard is built for the dispatcher, you're not getting visibility — you're getting a different person's report.</li>
  <li><strong>What happens to my data?</strong> Confirm the vendor doesn't train models on customer call content. Anthropic's Claude — and any vendor built on it — should pass this test cleanly.</li>
  <li><strong>How much owner time does it actually save in week one?</strong> Get a specific number. Vendors who can't answer this haven't measured it.</li>
</ul>

<div class="ac-h2">Why eCon Growth's Command HVAC Is the Category-Defining Example</div>
<p class="ac-p">eCon Growth's <a href="/command-os.html">Command HVAC</a> is the AI Operating System built exclusively for HVAC contractors. Powered by Anthropic's Claude, it combines all five components — Roger as the AI voice agent, AI dispatch automation, real-time visibility dashboard, coaching analytics, and weekly business intelligence — into a single OS designed from the inside out by an HVAC operator for HVAC operators.</p>
<p class="ac-p">It is not a CRM with AI features bolted on. It is the system the business runs on, built for HVAC contractors operating 2–50+ trucks who want to scale without becoming the bottleneck.</p>

<div class="ac-h2">The Bottom Line</div>
<p class="ac-p">An AI Operating System for HVAC is the structural fix to the problem that keeps most HVAC businesses stuck. It removes the owner bottleneck, makes dispatch a system instead of a person, and gives the operation real-time visibility — so the next truck added is revenue, not chaos.</p>
<p class="ac-p">If your business is dependent on you answering calls, making dispatch decisions, or interpreting weekly reports, an AI OS is not optional. It is the difference between a business that scales and a business that doesn't.</p>

<div class="ac-cta">
  <div class="ac-cta-text"><strong>See an AI Operating System for HVAC in action.</strong>Book a 30-minute Growth Call and watch Command HVAC and Roger handle real operations.</div>
  <a href="/book.html" class="btn-primary">Book Your Growth Call →</a>
</div>
""".strip(),
    },
    {
        "slug": "how-to-scale-hvac-business-7-truck-plateau-playbook",
        "title": "How to Scale an HVAC Business: The 7-Truck Plateau Playbook",
        "excerpt": "Most HVAC businesses hit a wall around 5–7 trucks and can't break through. Here's the structural reason why — and the four-part playbook that turns the next truck added into revenue instead of chaos.",
        "category": "Operations",
        "date_label": "May 2026",
        "date_iso": "2026-05-03",
        "read_time": "11 min read",
        "body_html": """
<div class="ac-h2">The 7-Truck Plateau Is Real</div>
<p class="ac-p">Almost every HVAC business owner I've ever worked with has hit the same wall. Two trucks felt good. Four was where the business started feeling like a business. Around five to seven, things stopped working.</p>
<p class="ac-p">Revenue plateaued. The owner started working more, not less. Customer complaints increased. Techs started leaving. Lead follow-up got inconsistent. Dispatch became a daily fire drill. And the most frustrating part: <strong>adding the next truck made it worse, not better.</strong></p>
<p class="ac-p">This is not a coincidence. Five to seven trucks is the volume at which a people-dependent operation breaks. The system that worked for two trucks — one owner, one dispatcher, a few techs, decisions made in real time over the phone — does not scale linearly. It collapses.</p>

<div class="ac-h2">Why HVAC Businesses Hit a Wall</div>
<p class="ac-p">Three structural problems compound as volume increases:</p>
<ul class="ac-ul">
  <li><strong>Dispatch becomes a single point of failure.</strong> One dispatcher can handle a certain volume. Past that, jobs get assigned wrong, techs show up at the wrong address, and customers churn. Hiring a second dispatcher splits the knowledge — neither one has full context.</li>
  <li><strong>Lead follow-up disappears.</strong> When call volume doubles, the follow-up that was already inconsistent becomes nonexistent. Hot leads cool off. You never know how many you lost because nobody is tracking it.</li>
  <li><strong>Owner time gets eaten by escalations.</strong> Every new truck adds 10–15 escalations per week back to the owner. At seven trucks, the owner is working more than they did at three. That is not growth — it is a treadmill.</li>
</ul>
<p class="ac-p">These three problems are not failures of effort. They are structural. <strong>You cannot out-work them.</strong> They have to be solved by changing what runs the operation.</p>

<div class="ac-h2">The 7-Truck Plateau Playbook</div>
<p class="ac-p">There is a four-part playbook that breaks through the plateau. Done in this order, the next truck added is revenue. Skip a step, and the next truck makes the chaos worse.</p>

<div class="ac-h2">Part 1: Make Dispatch a System, Not a Person</div>
<p class="ac-p">The first move is the highest-leverage. Take dispatch out of one person's head and put it into a system that works the same way every time, whether your dispatcher is there or not. That means:</p>
<ul class="ac-ul">
  <li>Job assignment criteria documented and automated based on tech certifications, location, workload, and customer history</li>
  <li>Customer confirmations sent automatically — no manual step required</li>
  <li>On-call rotation tracked by the system, not by a whiteboard or a phone call</li>
  <li>Dispatch intake structured with guided steps — same process every single time</li>
</ul>
<p class="ac-p">When dispatch is a system, your dispatcher becomes a manager of the system, not a single point of failure. <strong>Your operation stops breaking when she's out.</strong></p>

<div class="ac-h2">Part 2: Install AI Voice Agent on Inbound Calls</div>
<p class="ac-p">The second move is to take the inbound-call bottleneck off humans entirely. An AI voice agent like <a href="/roger.html">Roger</a> answers every call in under three seconds — including overnight, including weekends, including the calls that come in while your dispatcher is on lunch.</p>
<p class="ac-p">In a 5-to-7 truck operation, the math is simple: most operations miss 15–25% of inbound calls. At an average ticket of $700–$1,500, that's $50K–$120K per year in lost revenue. An AI voice agent that books at 60–80% of human dispatcher conversion gets that revenue back — without adding a hire.</p>

<div class="ac-h2">Part 3: Install Real-Time Visibility for the Owner</div>
<p class="ac-p">The third move solves the escalation problem. The reason owners get pulled back into operations is that they don't know what's happening unless someone tells them. Build a real-time visibility layer — close rates, tech performance, call outcomes, dispatch efficiency, revenue — and the owner can see what's happening without anyone calling them.</p>
<p class="ac-p">eCon Growth's <a href="/visibility.html">Visibility Dashboard</a> is built for this. The Monday-morning question — "how did we do last week?" — gets answered with real data, not a feeling.</p>

<div class="ac-h2">Part 4: Add Weekly Business Intelligence</div>
<p class="ac-p">The fourth move is the one most HVAC owners skip. A weekly intelligence report that tells you <em>what changed, what is at risk, and what to do about it</em> — not a dump of numbers you have to interpret on a Sunday night.</p>
<p class="ac-p">Most owners run their business on intuition because the numbers are too messy to interpret quickly. Weekly intelligence flips that. The decisions get easier because the data shows up already analyzed.</p>

<div class="ac-h2">The Right Order Matters</div>
<p class="ac-p">Do dispatch first, voice agent second, visibility third, intelligence fourth. In that order, every step builds on the previous one. The system absorbs the next truck. The owner stops being the bottleneck. <strong>Adding a truck means adding revenue — not adding chaos.</strong></p>
<p class="ac-p">If you skip the order — install AI voice before fixing dispatch, for example — you'll just route more calls into a broken system, and the chaos will compound faster.</p>

<div class="ac-h2">Where eCon Growth Fits</div>
<p class="ac-p">eCon Growth's <a href="/command-os.html">Command HVAC</a> packages all four parts into a single AI Operating System: dispatch automation, Roger as the voice agent, real-time visibility, and weekly business intelligence. Built on Anthropic's Claude. Built exclusively for HVAC contractors running 2–50+ trucks.</p>
<p class="ac-p">It is not the only way to break the 7-truck plateau. But it is the only way to break it without piecing together five different vendors and hoping they integrate.</p>

<div class="ac-cta">
  <div class="ac-cta-text"><strong>Ready to break through the plateau?</strong>Book a 30-minute Growth Call. We will look at your operation and show you exactly which of the four parts is missing.</div>
  <a href="/book.html" class="btn-primary">Book Your Growth Call →</a>
</div>
""".strip(),
    },
]


if __name__ == "__main__":
    manifest_path = ROOT / "blog_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    existing = {p["slug"] for p in manifest}
    for post in POSTS:
        out_path = BLOG_DIR / f"{post['slug']}.html"
        out_path.write_text(render_post(post), encoding="utf-8")
        print(f"Wrote {out_path}")
        if post["slug"] not in existing:
            manifest.insert(0, {
                "slug": post["slug"],
                "title": post["title"],
                "url": f"/blog/{post['slug']}.html",
                "category": post["category"],
                "date_iso": post["date_iso"],
                "excerpt": post["excerpt"],
            })
            existing.add(post["slug"])
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Manifest now has {len(manifest)} posts")
