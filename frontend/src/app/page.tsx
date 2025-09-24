"use client";
import { useState } from "react";
import { createTranscription, getTranscriptionStatus, getTranscriptionResult } from "@/lib/api";

export default function Home() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("");
  const [text, setText] = useState<string>("");

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const file = (e.currentTarget.elements.namedItem("file") as HTMLInputElement)?.files?.[0];
    if (!file) return;
    const job = await createTranscription(file);
    setJobId(job.job_id);
    setStatus(job.status);

    // Poll cada 2s hasta finished/failed
    const interval = setInterval(async () => {
      const s = await getTranscriptionStatus(job.job_id);
      setStatus(s.status);
      if (s.status === "finished") {
        clearInterval(interval);
        const r = await getTranscriptionResult(job.job_id);
        setText(r.text ?? JSON.stringify(r));
      }
      if (s.status === "failed") clearInterval(interval);
    }, 2000);
  }

  return (
    <main style={{ padding: 24 }}>
      <h1>Whisper Website</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" name="file" accept="audio/*" />
        <button type="submit">Subir</button>
      </form>
      {jobId && (
        <div style={{ marginTop: 12 }}>
          <div>Job: {jobId}</div>
          <div>Status: {status}</div>
          {text && (
            <>
              <h3>Resultado</h3>
              <pre style={{ whiteSpace: "pre-wrap" }}>{text}</pre>
            </>
          )}
        </div>
      )}
    </main>
  );
}
