export type TranscriptionJob = { job_id: string; status: string };

export async function createTranscription(file: File) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/api/transcriptions", { method: "POST", body: form });
  if (!res.ok) {
    const txt = await res.text().catch(() => "");
    throw new Error(`Failed to create transcription: ${res.status} ${res.statusText} — ${txt}`);
  }
  return res.json() as Promise<TranscriptionJob>;
}

export async function getTranscriptionStatus(id: string) {
  const res = await fetch(`/api/transcriptions/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Status ${res.status}`);
  return res.json() as Promise<{ status: string }>;
}

export async function getTranscriptionResult(id: string) {
  const r = await fetch(`/api/transcriptions/${id}/result`, { cache: "no-store" });
  if (!r.ok) throw new Error(await r.text());
  // Tu backend devuelve `json` como string → parseamos
  const data = await r.json() as { json?: string; text_path?: string };
  const parsed = data.json ? JSON.parse(data.json) : null;
  return {
    text: parsed?.text ?? "",
    raw: parsed,
    text_path: data.text_path,
  };
}
