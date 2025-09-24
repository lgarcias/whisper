export const runtime = "nodejs";
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://api:8000";

export async function GET() {
  try {
    const r = await fetch(`${API_BASE}/health`);
    const text = await r.text();
    return new Response(text, {
      status: r.status,
      headers: { "content-type": "application/json" },
    });
  } catch (e: any) {
    return new Response(
      JSON.stringify({ error: "upstream failed", detail: e?.message }),
      { status: 502 }
    );
  }
}
