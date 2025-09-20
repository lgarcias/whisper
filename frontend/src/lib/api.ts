export async function createTranscription(file: File) {
  const fd = new FormData();
  fd.append("file", file);
  const r = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/transcriptions`, { method: "POST", body: fd });
  if (!r.ok) throw new Error(await r.text());
  return r.json() as Promise<{ job_id: string; status: string }>;
}
export async function getStatus(id: string) {
  const r = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/transcriptions/${id}`);
  if (!r.ok) throw new Error(await r.text());
  return r.json() as Promise<{ job_id: string; status: string }>;
}
export async function getResult(id: string) {
  const r = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/transcriptions/${id}/result`);
  if (r.status === 202) throw new Error("NotReady");
  if (!r.ok) throw new Error(await r.text());
  return r.json() as Promise<{ json: string; text_path: string; outdir?: string }>;
}
