import json

def create_plan(event_type, name, location, event_date, guests, budget, theme, preferences, api_key=""):
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"""
            Create a practical event plan as valid JSON only.
            Event: {event_type}; Name: {name}; Location: {location};
            Date: {event_date}; Guests: {guests}; Budget INR: {budget};
            Theme: {theme}; Preferences: {preferences}.
            Return keys: concept (string), ideas (list of 5 strings),
            budget (list of objects with Category and Amount (INR)),
            timeline (list of objects with Task and Deadline),
            vendors (list of objects with Vendor and Booked).
            Keep budget amounts within the total budget.
            """
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
            text = response.text.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            result = json.loads(text)
            if sum(float(x["Amount (INR)"]) for x in result["budget"]) > budget:
                raise ValueError("AI budget exceeds total")
            return result
        except Exception:
            pass

    allocations = [
        ("Venue", .25), ("Food & Catering", .30),
        ("Decoration", .15), ("Photography", .10),
        ("Entertainment", .10), ("Miscellaneous", .10)
    ]
    budget_rows = [
        {"Category": category, "Amount (INR)": round(budget * share)}
        for category, share in allocations
    ]

    tasks = [
        ("Finalize event concept and budget", 30),
        ("Book venue", 25),
        ("Confirm catering and menu", 20),
        ("Book photographer and entertainment", 15),
        ("Send invitations", 10),
        ("Confirm guest count and vendors", 5),
        ("Final venue inspection", 2),
        ("Event day coordination", 0)
    ]
    timeline = [
        {"Task": task, "Deadline": f"{event_date} ({days} days before)"}
        for task, days in tasks
    ]
    vendors = [
        {"Vendor": vendor, "Booked": False}
        for vendor in ["Venue", "Caterer", "Decorator", "Photographer",
                       "Entertainment", "Sound & Lighting", "Transport"]
    ]

    return {
        "concept": f"{name} is a {theme.lower()} {event_type.lower()} celebration in {location} for approximately {guests} guests on {event_date}. The plan focuses on a memorable experience while staying within your ₹{budget:,.0f} budget.",
        "ideas": [
            f"Create a welcoming {theme.lower()} entrance.",
            "Set up a memorable photo booth for guests.",
            "Prepare a personalized invitation and event welcome board.",
            "Offer a menu with options suited to your guests.",
            f"Plan music and activities for approximately {guests} guests."
        ],
        "budget": budget_rows,
        "timeline": timeline,
        "vendors": vendors
    }
