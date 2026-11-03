"""Company Research Job — Apify Actor.

Thin wrapper around the Mekong Trade Intelligence Company Research Job
(https://api.mekongtradeintel.com/companyresearch/). The buyer pays on
Apify via pay-per-event; the Actor executes the job through a dedicated
channel key (env MTI_CHANNEL_KEY, set as a secret by the Actor owner)
and pushes the finished research as one dataset item.

Charge policy: the pay-per-event charge happens ONLY after the job has
completed and its result has been pushed to the dataset. A failed job
fails the run and is never charged.
"""

import asyncio
import os

import httpx
from apify import Actor

JOB_URL = "https://api.mekongtradeintel.com/companyresearch/"
EVENT_NAME = "company-research"
JOB_TIMEOUT_S = 900  # a full job (web + footprint + briefing) can take minutes


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        company = str(actor_input.get("company") or "").strip()
        domain = str(actor_input.get("domain") or "").strip()
        geo = str(actor_input.get("geo") or "").strip()

        if not company:
            await Actor.fail("Input 'company' is required.")
            return

        channel_key = os.environ.get("MTI_CHANNEL_KEY", "").strip()
        if not channel_key:
            await Actor.fail("Actor is not configured (missing channel key).")
            return

        payload = {"company": company}
        if domain:
            payload["domain"] = domain
        if geo:
            payload["geo"] = geo

        Actor.log.info(f"Running company research job for: {company}")

        async with httpx.AsyncClient(timeout=JOB_TIMEOUT_S, trust_env=False) as client:
            resp = await client.post(
                JOB_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "X-Channel-Key": channel_key,
                    "User-Agent": "ApifyActor-CompanyResearchJob/1.0",
                },
            )

        if resp.status_code != 200:
            await Actor.fail(
                f"Research job failed with HTTP {resp.status_code}: {resp.text[:300]}"
            )
            return

        result = resp.json()

        # One dataset item per job: the full stitched report.
        item = {
            "company": company,
            "domain": domain or None,
            "geo": geo or None,
            "generated_at": result.get("generated_at"),
            "research_summary": result.get("research_summary"),
            "footprint": result.get("footprint"),
            "briefing": result.get("briefing"),
            "web": result.get("web"),
            "partial_failures": result.get("partial_failures"),
            "source_service": result.get("service"),
        }
        await Actor.push_data(item)
        Actor.log.info("Research job completed and pushed to dataset.")

        # Charge only after successful delivery.
        try:
            await Actor.charge(event_name=EVENT_NAME, count=1)
            Actor.log.info(f"Charged 1 x '{EVENT_NAME}' event.")
        except Exception as exc:  # billing must never mask a delivered result
            Actor.log.warning(f"Charge call failed (result already delivered): {exc}")


if __name__ == "__main__":
    asyncio.run(main())
