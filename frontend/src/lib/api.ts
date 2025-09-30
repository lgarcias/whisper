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
  // Ahora el backend devuelve 'result' ya parseado
  type TranscriptionResult = { text: string; [key: string]: unknown };
  const data = await r.json() as { result?: TranscriptionResult; text_path?: string };
  return {
    text: data.result?.text ?? "",
    raw: data.result,
    text_path: data.text_path,
  };
}
