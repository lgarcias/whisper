"use client";

import { useState } from "react";
import { createTranscription, type TranscriptionJob } from "../lib/api";

export default function Page() {
  const [file, setFile] = useState<File | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    // createTranscription devuelve { job_id, status }
    const res: TranscriptionJob = await createTranscription(file);
    setJobId(res.job_id); // ← extraemos la string correcta
  };

  return (
    <div>
      <h1>Upload audio</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="audio/*"
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setFile(e.target.files?.[0] ?? null)
          }
        />
        <button type="submit">Submit</button>
      </form>
      {jobId && <p>Job created: {jobId}</p>}
    </div>
  );
}
