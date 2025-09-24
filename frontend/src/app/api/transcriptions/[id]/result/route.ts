export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://api:8000";

export async function GET(_req: Request, ctx: { params: Promise<{ id: string }> }) {
  const { id } = await ctx.params;                // ← wait for the params promise to resolve
  const r = await fetch(`${API_BASE}/transcriptions/${id}/result`);
  const text = await r.text();
  return new Response(text, {
    status: r.status,
    headers: { "content-type": r.headers.get("content-type") || "application/json" },
  });
}
