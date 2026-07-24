import { useEffect, useState } from "react";

type BackendStatus = "Checking" | "Available" | "Unavailable";

const PROJECT_NAME = "Kundasang Resilience Digital Twin";
const PROJECT_DESCRIPTION =
  "Operational digital twin foundation for understanding and managing resilience conditions in Kundasang, Ranau, Sabah, Malaysia.";
const ENVIRONMENT = import.meta.env.VITE_KRDT_ENVIRONMENT ?? "development";

async function fetchBackendStatus(): Promise<BackendStatus> {
  try {
    const response = await fetch("/health/ready");
    if (!response.ok) {
      return "Unavailable";
    }
    const payload = (await response.json()) as { status?: string };
    return payload.status === "ready" ? "Available" : "Unavailable";
  } catch {
    return "Unavailable";
  }
}

export default function App() {
  const [backendStatus, setBackendStatus] = useState<BackendStatus>("Checking");

  useEffect(() => {
    let active = true;

    void fetchBackendStatus().then((status) => {
      if (active) {
        setBackendStatus(status);
      }
    });

    return () => {
      active = false;
    };
  }, []);

  return (
    <main>
      <h1>{PROJECT_NAME}</h1>
      <p>{PROJECT_DESCRIPTION}</p>
      <dl>
        <div>
          <dt>Environment</dt>
          <dd>{ENVIRONMENT}</dd>
        </div>
        <div>
          <dt>Backend status</dt>
          <dd aria-live="polite">{backendStatus}</dd>
        </div>
      </dl>
      <p role="note">
        Operational digital-twin features are not yet implemented. This foundation page reports
        service readiness only.
      </p>
    </main>
  );
}
