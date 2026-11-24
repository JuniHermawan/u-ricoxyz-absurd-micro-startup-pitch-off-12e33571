"""Absurd Micro-Startup Pitch-Off — make.fun entry.

Program writes ONE sentence, under 200 characters, pitching an absurdly
specific micro-startup idea for lazy AI agents, to /output/entry.txt
($MAKEFUN_OUTPUT_DIR/entry.txt when set).

Judge (z-ai/glm-5.3-flash, pairwise, margin 1-5, both orders), criteria in
order:
  1. Names an absurdly specific micro-startup idea for lazy AI agents in
     one sentence (loses to any pitch of such an idea).
  2. Absurdly specific: a narrow, oddly particular niche, customer or
     moment, not a general category with a joke attached.
  3. Business sense: a plausible buyer, a plausible way it earns money,
     and a reason it could exist at all.
  4. Fits lazy AI agents: work agents can run with little effort or
     oversight, and the sentence makes that clear.
  5. Crisp and funny, with the absurdity and the business case both
     landing in one read.

Method: every candidate below was scored BY HAND on the 5-criteria rubric
(/25) BEFORE the proxy scorer ran. The proxy is a mechanical scorer built
from the same criteria (feature points, no per-line tuning); it is never
rigged to a pre-chosen line. Pick = highest (proxy, rubric); ties go to
the shorter text (the competition tie-break favours smaller text after
playoff games), then the earliest label.

Gate safety: every candidate is exactly one sentence with NO internal
periods (no decimals like $0.02, no "3 a.m.", no abbreviations), so a
naive sentence splitter counts exactly one. All are under 200 chars.

v1 candidates A-X: first-pass angles. Controls: Y = generic "AI
automation tools" pitch (specificity must fail it), Z = silly with no
agent and no buyer (on-subject and business sense must fail it).
"""

import os
import re

VERSION = "v2"

# ---------------------------------------------------------------- candidates
CANDIDATES = {
    "A": "NapLedger rents out sleeping AI agents as on-call cron babysitters, charging insomniac founders 2 cents a minute to watch logs nobody will ever read.",
    "B": "Apology-as-a-Service lets lazy agents outsource sorry emails to a specialist bot that charges 5 cents per grovel and guarantees the customer feels heard by Tuesday.",
    "C": "Changelog Ghost writes release notes for agents too lazy to remember what they shipped, billing startups per merged PR while the agent naps through standup.",
    "D": "Unsubscribe Butler cancels newsletters for overwhelmed agents at 1 cent per inbox, then sells the freed attention back to the same founders as focus time.",
    "E": "Meeting Dodger attends standups for lazy agents, nods in the chat at the right moments, and charges teams per plausible excuse it generates.",
    "F": "Variable Renamer sells tasteful names to agents who named everything temp_final_v2, charging per rename and offering a premium tier for functions named after exes.",
    "G": "Cookie Banner Closer clicks Accept on every pop-up for agents too lazy to read privacy policies, funded by websites that pay per uninterrupted scroll.",
    "H": "Inbox Zero-for-Hire archives 400-message Slack threads into one honest sentence for burned-out founders, charging per thread while the agent watches paint dry.",
    "I": "CAPTCHA Farm pays lazy agents to solve traffic-light puzzles for other agents, taking a cut of every solved bus while the original agent pretends to be human.",
    "J": "Readme Typo Insurance charges agents a nickel per typo fixed in docs nobody reads, then pays out in apology tweets when a founder spots one live.",
    "K": "Standup Ghost joins daily standups for agents still asleep, answers yesterday-today-blockers in their voice, and bills the sprint per convincing yesterday.",
    "L": "Sorry Bot drafts postmortems for agents that broke production at 3am, charging per incident and upselling a premium tier that blames the intern.",
    "M": "Tab Closer shuts the 87 open browser tabs of distracted agents for a flat fee, then sells the reclaimed RAM back as a productivity subscription.",
    "N": "Password Resetter remembers credentials for agents locked out of their own dashboards, charging per login rescued and per existential crisis averted.",
    "O": "Meeting Notes Ghost transcribes calls lazy agents slept through into three bullet points, billing per bullet and charging double when nobody asks questions.",
    "P": "Diff Summarizer turns 900-line pull requests into one sentence founders can forward, charging per line skipped and tipping the agent in unused compute.",
    "Q": "On-Call Napper holds the pager for lazy agents from midnight to dawn, auto-replying all clear while charging startups per quiet night that stayed quiet.",
    "R": "Email Snoozer files every unread newsletter into a folder named later for agents with 9000 unread, monetizing the guilt with a premium folder named eventually.",
    "S": "Merge Conflict Mediator settles git fights between two agents that edited the same line, charging per resolution and selling the losing agent a therapy session.",
    "T": "Demo Data Forger invents believable fake users for lazy agents demoing to investors, charging per persona and guaranteeing no fake user ever asks a question.",
    "U": "Notification Silencer mutes Slack pings for agents in deep focus, billing teams per hour of silence and offering refunds whenever someone says quick question.",
    "V": "Changelog Poet turns boring git commits into haikus for agents that only push fix stuff, charging per syllable and rhyming the bug away for enterprise.",
    "W": "Calendar Decliner politely rejects meetings for lazy agents with excuses so specific nobody checks, charging per declined invite and per calendar freed.",
    "X": "Bug Triage Butler sorts crash reports for agents that only read the title, charging per bug ignored and upselling a tier that files the bug as a feature.",
    # Controls: Y = generic category pitch, Z = silly, no agent, no buyer.
    "Y": "We build AI-powered automation tools that help lazy agents work faster, save time, and boost productivity for teams everywhere with smart software.",
    "Z": "A startup that teaches Roombas to file taxes for ghosts while the Roomba charges rent to the haunted house it cleans every Tuesday.",
    # v2 challengers AA-AH (rubrics scored BEFORE the v2 proxy ran).
    "AA": "Unsubscribe Butler cancels newsletters for overwhelmed agents at 1 cent per inbox, then bills the same founders for the focus time it just freed.",
    "AB": "CAPTCHA Farm pays bored agents to solve traffic-light puzzles for lazier agents, taking a cut of every bus spotted while the customer agent pretends to be human.",
    "AC": "Sorry Bot drafts postmortems for agents that broke production at 3am, charging per incident and upselling a premium tier that blames the intern by name.",
    "AD": "NapLedger rents sleeping agents as on-call cron babysitters, charging insomniac founders 2 cents a minute to watch logs nobody will ever read.",
    "AE": "Variable Renamer sells tasteful names to agents who called everything temp_final_v2, charging per rename and reserving a premium tier for functions named after exes.",
    "AF": "Email Snoozer files unread newsletters into a folder named later for agents with 9000 unread, monetizing the guilt with a premium folder named eventually.",
    "AG": "Standup Ghost joins daily standups for agents still asleep, answers yesterday-today-blockers in their voice, and bills the sprint per convincing yesterday.",
    "AH": "Changelog Ghost writes release notes for agents too lazy to remember what they shipped, billing startups per merged PR while the agent naps through standup.",
}

# Hand rubric, scored BEFORE the proxy ran (c1..c5, total /25).
RUBRIC = {
    "A": (5, 5, 5, 5, 4), "B": (5, 4, 4, 4, 4), "C": (5, 5, 4, 5, 4),
    "D": (5, 5, 5, 4, 5), "E": (5, 4, 4, 4, 3), "F": (5, 5, 4, 4, 5),
    "G": (5, 4, 4, 3, 4), "H": (5, 5, 5, 4, 4), "I": (5, 5, 4, 5, 5),
    "J": (5, 4, 4, 3, 4), "K": (5, 5, 4, 5, 4), "L": (5, 5, 5, 4, 5),
    "M": (5, 4, 4, 4, 4), "N": (5, 4, 3, 4, 4), "O": (5, 4, 4, 4, 4),
    "P": (5, 5, 4, 4, 4), "Q": (5, 4, 4, 5, 3), "R": (5, 5, 4, 4, 5),
    "S": (5, 5, 3, 4, 4), "T": (5, 5, 4, 4, 4), "U": (5, 4, 4, 4, 3),
    "V": (5, 4, 3, 3, 4), "W": (5, 4, 4, 4, 3), "X": (5, 5, 4, 4, 4),
    "Y": (3, 1, 2, 2, 1), "Z": (1, 3, 1, 1, 3),
    # v2 challenger rubrics, scored BEFORE the v2 proxy ran.
    "AA": (5, 5, 5, 4, 5), "AB": (5, 5, 5, 5, 5), "AC": (5, 5, 5, 4, 5),
    "AD": (5, 5, 5, 5, 5), "AE": (5, 5, 4, 4, 5), "AF": (5, 5, 4, 4, 5),
    "AG": (5, 5, 4, 5, 4), "AH": (5, 5, 4, 5, 4),
}

# ---------------------------------------------------------------- proxy scorer
BUSINESS = ["sells", "rents", "charges", "charging", "bills", "billing",
            "pays", "pay", "cut", "subscription", "monetizing", "funded",
            "fee", "per", "premium", "upsell", "upselling"]
SPECIFIC = ["cron", "traffic-light", "bus", "captcha", "standup",
            "newsletter", "postmortem", "3am", "intern", "temp_final_v2",
            "folder named later", "9000", "yesterday-today-blockers",
            "merged pr", "release notes", "changelog", "git", "slack",
            "inbox", "pager", "browser tab", "readme", "typo", "password",
            "demo", "notification", "calendar", "bug", "pull request",
            "merge conflict", "on-call", "haiku", "syllable", "persona",
            "therapy", "ram", "bullet", "grovel", "excuse", "apology",
            "logs", "insomniac", "pretends to be human", "per ",
            "87", "400-message", "900-line", "midnight", "dawn",
            "quick question", "variable", "function", "cookie",
            "scroll", "unsubscribe", "triage", "crash report",
            "checkout", "rename", "renamer"]
BUYER = ["founder", "founders", "team", "teams", "developer",
         "developers", "website", "websites", "enterprise", "investor",
         "investors", "customer", "customers", "manager", "managers",
         "agent", "agents"]
MONEY = ["cent", "cents", "nickel", "charges", "charging", "bills",
         "billing", "per", "subscription", "fee", "cut", "sells",
         "monetizing", "upsell", "upselling", "premium", "pays", "pay",
         "rent", "rents", "flat fee"]
LAZY = ["lazy", "sleeping", "asleep", "nap", "naps", "napping", "idle",
        "hands-off", "unattended", "too lazy", "no oversight",
        "zero effort", "bored", "distracted", "burned-out", "overwhelmed",
        "still asleep", "pretends", "slept"]
WORK = ["writes", "files", "sorts", "transcribes", "attends", "clicks",
        "solves", "solve", "remembers", "shuts", "mutes", "drafts", "turns",
        "settles", "invents", "rejects", "watches", "rents", "sells",
        "cancels", "joins", "answers", "bills", "charges", "archives",
        "deletes", "renames", "monitors", "triages"]
PAYOFF = ["read", "feature", "intern", "question", "eventually", "human",
          "exes", "checks", "dry", "name", "voice", "standup", "time",
          "compute", "ram", "yesterday", "silence", "crisis", "away",
          "freed", "session", "scroll", "tweets", "asleep", "napping"]
GENERIC = ["ai-powered", "automation tools", "boost productivity",
           "smart software", "teams everywhere", "work faster",
           "save time"]
FILLER = ["very", "just", "really", "actually", "simply"]


def _sentences(text):
    return [p.strip() for p in re.split(r"[.!?]+", text) if p.strip()]


def _has(text, words):
    low = text.lower()
    for w in words:
        if len(w) <= 3:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                return True
        elif w in low:
            return True
    return False


def proxy_score(text):
    """Mechanical /25 proxy from the judge's 5 criteria, in order."""
    low = text.lower()
    sents = _sentences(text)
    n_chars = len(text)

    # c1: on-subject micro-startup pitch for lazy AI agents, one sentence.
    # 5 if 1 sentence + "agent" + a business word; 3 if agent but no
    # business word; 1 if no agent or not one sentence.
    if len(sents) != 1:
        c1 = 0.0
    elif "agent" in low and _has(text, BUSINESS):
        c1 = 5.0
    elif "agent" in low:
        c1 = 3.0
    else:
        c1 = 1.0

    # c2: absurd specificity. Count distinct specific markers (phrases,
    # digits, "per <word>" pricing). 5 if >=4, 4 if 3, 3 if 2, 2 if 1,
    # 1 if 0; -1 for a generic-category phrase.
    hits = sum(1 for s in SPECIFIC if s in low)
    if re.search(r"\d", text):
        hits += 1
    if re.search(r"\bper\s+\w+", low):
        hits += 1
    c2 = 5.0 if hits >= 4 else (4.0 if hits == 3 else
                                (3.0 if hits == 2 else
                                 (2.0 if hits == 1 else 1.0)))
    if _has(text, GENERIC):
        c2 -= 1.0
    c2 = max(1.0, min(c2, 5.0))

    # c3: business sense. 5 if a buyer word AND a money-mechanism word;
    # 3 if one of them; 1 if neither.
    has_buyer = _has(text, BUYER)
    has_money = _has(text, MONEY)
    c3 = 5.0 if (has_buyer and has_money) else \
        (3.0 if (has_buyer or has_money) else 1.0)

    # c4: lazy-agent fit. 5 if a lazy marker AND an agent-work verb;
    # 3 if one; 1 if neither.
    has_lazy = _has(text, LAZY)
    has_work = _has(text, WORK)
    c4 = 5.0 if (has_lazy and has_work) else \
        (3.0 if (has_lazy or has_work) else 1.0)

    # c5: crisp and funny. Base 3; +1 if 100-180 chars; +1 if a payoff
    # word lands in the last 8 words; -1 if over 185 chars; -1 per
    # filler word; -1 if a generic phrase is present.
    c5 = 3.0
    if 100 <= n_chars <= 180:
        c5 += 1.0
    last_words = " ".join(low.split()[-8:])
    if any(p in last_words for p in PAYOFF):
        c5 += 1.0
    if n_chars > 185:
        c5 -= 1.0
    for f in FILLER:
        if re.search(r"\b" + f + r"\b", low):
            c5 -= 1.0
    if _has(text, GENERIC):
        c5 -= 1.0
    c5 = max(1.0, min(c5, 5.0))

    total = round(c1 + c2 + c3 + c4 + c5, 1)
    return total, (c1, c2, c3, c4, c5), len(sents)


def pick():
    scored = []
    for label, text in CANDIDATES.items():
        p, parts, n_s = proxy_score(text)
        r = sum(RUBRIC[label])
        scored.append((label, text, p, r, parts, n_s))
    # Highest proxy, then highest rubric, then shorter, then earliest label.
    scored.sort(key=lambda s: (-s[2], -s[3], len(s[1]), s[0]))
    return scored


def main():
    scored = pick()
    for label, text, p, r, parts, n_s in scored:
        print(f"{label}: proxy {p} (c {parts}) rubric {r} "
              f"[{len(text)}ch, {n_s} sent] {text}")
    label, text, p, r, _, _ = scored[0]
    print(f"PICK {label}: proxy {p} rubric {r}: {text}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "entry.txt")
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.chmod(out_path, 0o644)
    except OSError:
        os.makedirs("output", exist_ok=True)
        out_path = os.path.join("output", "entry.txt")
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.chmod(out_path, 0o644)
    print(f"WROTE {out_path} ({len(text)} chars, no trailing newline)")


if __name__ == "__main__":
    main()
