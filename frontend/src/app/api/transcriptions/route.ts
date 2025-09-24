import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://api:8000";

export async function POST(req: Request) {
  try {
    const inForm = await req.formData();
    const file = inForm.get("file") as File | null;
    if (!file) return NextResponse.json({ error: "Missing file" }, { status: 400 });

    const fd = new FormData();
    fd.append("file", file, (file as any).name ?? "audio.wav");

    const upstream = await fetch(`${API_BASE}/transcriptions`, { method: "POST", body: fd });
    const text = await upstream.text();
    return new Response(text, {
      status: upstream.status,
      headers: { "content-type": upstream.headers.get("content-type") || "application/json" },
    });
  } catch (e: any) {
    return NextResponse.json({ error: "Proxy error", detail: e?.message ?? String(e) }, { status: 500 });
  }
}
