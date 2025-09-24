export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://api:8000";

export async function GET(_req: Request, ctx: { params: Promise<{ id: string }> }) {
  const { id } = await ctx.params;                //obtein id from params
  const upstream = await fetch(`${API_BASE}/transcriptions/${id}`);
  const text = await upstream.text();
  return new Response(text, {
    status: upstream.status,
    headers: { "content-type": upstream.headers.get("content-type") || "application/json" },
  });
}