"use client";

import { useEffect, useState } from "react";
import { getStatus, type TranscriptionJob } from "../../../lib/api";

export default function JobPage({ params }: { params: { id: string } }) {
  const { id } = params;
  const [status, setStatus] = useState<string>("loading");

  useEffect(() => {
    let timer: ReturnType<typeof setInterval> | null = null;

    async function tick() {
      try {
        const s: TranscriptionJob = await getStatus(id);
        setStatus(s.status); // ← solo la string, no el objeto
      } catch (e) {
        console.error(e);
        setStatus("error");
      }
    }

    tick();
    timer = setInterval(tick, 2000);

    return () => {
      if (timer !== null) clearInterval(timer);
    };
  }, [id]);

  return (
    <div>
      <h1>Job {id}</h1>
      <p>Status: {status}</p>
    </div>
  );
}
