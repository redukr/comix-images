import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "ok",
    services: {
      frontend: "running",
      backend: "check http://localhost:8000",
    },
  });
}
