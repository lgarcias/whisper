// frontend/src/app/lib/api.ts
export type TranscriptionJob = {
  job_id: string;
  status: "queued" | "processing" | "finished" | "error" | string;
};

export async function createTranscription(file: File): Promise<TranscriptionJob> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/api/transcriptions", { method: "POST", body: form });
  if (!res.ok) throw new Error("Failed to create transcription");
  return res.json() as Promise<TranscriptionJob>;
}

export async function getStatus(id: string): Promise<TranscriptionJob> {
  const res = await fetch(`/api/transcriptions/${id}`);
  if (!res.ok) throw new Error("Failed to get status");
  return res.json() as Promise<TranscriptionJob>;
}
