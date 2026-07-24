import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "./App";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("App", () => {
  it("renders project identity", () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ status: "ready" }), { status: 200 }),
    );

    render(<App />);

    expect(
      screen.getByRole("heading", { name: "Kundasang Resilience Digital Twin" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Operational digital twin foundation for understanding/i),
    ).toBeInTheDocument();
  });

  it("shows Checking initially", () => {
    vi.spyOn(globalThis, "fetch").mockReturnValue(new Promise(() => undefined));

    render(<App />);

    expect(screen.getByText("Checking")).toBeInTheDocument();
  });

  it("shows Available when readiness succeeds", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ status: "ready" }), { status: 200 }),
    );

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Available")).toBeInTheDocument();
    });
  });

  it("shows Unavailable when readiness fails", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response("error", { status: 503 }));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Unavailable")).toBeInTheDocument();
    });
  });

  it("states operational features are not implemented", () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ status: "ready" }), { status: 200 }),
    );

    render(<App />);

    expect(
      screen.getByText(/Operational digital-twin features are not yet implemented/i),
    ).toBeInTheDocument();
  });

  it("does not render fabricated operational metrics", () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ status: "ready" }), { status: 200 }),
    );

    render(<App />);

    expect(screen.queryByText(/sensor readings/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/incident count/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/landslide/i)).not.toBeInTheDocument();
  });
});
